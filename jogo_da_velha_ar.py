import threading
import time

import cv2
import numpy as np


BRANCO = (255, 255, 255)
VERDE = (0, 220, 80)
VERDE_ESCURO = (0, 150, 50)
VERMELHO = (0, 0, 255)
AZUL = (255, 80, 0)
AMARELO = (0, 220, 255)
PRETO = (25, 25, 25)

JANELA_NOME = "Jogo da Velha AR - QR Code"
TAMANHO_TABULEIRO = 3.5
TEMPO_CONFIRMACAO = 3.0
TOLERANCIA_PERDA_MARCADOR = 0.65
COOLDOWN_JOGADA = 0.8


class CameraThread:
    """Captura frames em uma thread separada para reduzir travamentos da leitura."""

    def __init__(self, camera_id):
        self.cap = cv2.VideoCapture(camera_id)
        self.lock = threading.Lock()
        self.frame = None
        self.ret = False
        self.running = False
        self.thread = None

    def is_opened(self):
        return self.cap.isOpened()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        return self

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()

            with self.lock:
                self.ret = ret
                if ret:
                    self.frame = frame

            time.sleep(0.001)

    def read(self):
        with self.lock:
            if self.frame is None:
                return False, None

            return self.ret, self.frame.copy()

    def release(self):
        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=1)

        self.cap.release()


class EstadoJogo:
    def __init__(self):
        self.reset()

    def reset(self):
        self.tabuleiro_pts = None
        self.celulas = [[None for _ in range(3)] for _ in range(3)]
        self.jogador_atual = "X"
        self.candidato = None
        self.candidato_inicio = 0
        self.candidato_visto_em = 0
        self.ultima_confirmacao = 0
        self.vencedor = None
        self.empate = False
        self.linha_vencedora = None

    def atualizar_tabuleiro(self, pts):
        self.tabuleiro_pts = pts.astype(np.float32)

    def registrar_candidato(self, simbolo, linha, coluna, agora):
        if self.vencedor or self.empate:
            return

        if simbolo != self.jogador_atual:
            return

        if self.celulas[linha][coluna] is not None:
            return

        novo_candidato = (simbolo, linha, coluna)

        if novo_candidato != self.candidato:
            self.candidato = novo_candidato
            self.candidato_inicio = agora

        self.candidato_visto_em = agora

        tempo_estavel = agora - self.candidato_inicio
        pode_confirmar = agora - self.ultima_confirmacao >= COOLDOWN_JOGADA

        if tempo_estavel >= TEMPO_CONFIRMACAO and pode_confirmar:
            self.confirmar_jogada(simbolo, linha, coluna, agora)

    def expirar_candidato(self, agora):
        if self.candidato is None:
            return

        if agora - self.candidato_visto_em > TOLERANCIA_PERDA_MARCADOR:
            self.candidato = None
            self.candidato_inicio = 0
            self.candidato_visto_em = 0

    def confirmar_jogada(self, simbolo, linha, coluna, agora):
        self.celulas[linha][coluna] = simbolo
        self.ultima_confirmacao = agora
        self.candidato = None
        self.candidato_inicio = 0
        self.candidato_visto_em = 0

        self.vencedor, self.linha_vencedora = verificar_vitoria(self.celulas)
        self.empate = self.vencedor is None and all(
            self.celulas[linha][coluna] is not None
            for linha in range(3)
            for coluna in range(3)
        )

        if self.vencedor is None and not self.empate:
            self.jogador_atual = "O" if simbolo == "X" else "X"

    def progresso_candidato(self, agora):
        if self.candidato is None:
            return 0

        return min((agora - self.candidato_inicio) / TEMPO_CONFIRMACAO, 1.0)


def listar_cameras(max_cameras=10):
    cameras_disponiveis = []

    print("Procurando cameras disponiveis...")

    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)

        if cap.isOpened():
            ret, _ = cap.read()

            if ret:
                cameras_disponiveis.append(i)
                print(f"[{i}] Camera disponivel")

        cap.release()

    return cameras_disponiveis


def selecionar_camera():
    cameras = listar_cameras()

    if not cameras:
        print("Nenhuma camera encontrada.")
        exit()

    print("\nSelecione a camera que deseja usar:")

    for cam in cameras:
        print(f"{cam} - Camera {cam}")

    while True:
        escolha = input("\nDigite o numero da camera: ")

        if escolha.isdigit() and int(escolha) in cameras:
            return int(escolha)

        print("Opcao invalida. Tente novamente.")


def interpolar(p1, p2, t):
    return (p1 + (p2 - p1) * t).astype(np.float32)


def mascarar_area(frame, pts, cor=BRANCO):
    cv2.fillConvexPoly(frame, pts.astype(np.int32), cor)


def calcular_tabuleiro_virtual(pts_marcador):
    pts_marcador = pts_marcador.astype(np.float32)
    centro = np.mean(pts_marcador, axis=0)
    largura = np.linalg.norm(pts_marcador[0] - pts_marcador[1])
    altura = np.linalg.norm(pts_marcador[1] - pts_marcador[2])
    tamanho = max(largura, altura) * TAMANHO_TABULEIRO

    return np.array(
        [
            [centro[0] - tamanho / 2, centro[1] - tamanho / 2],
            [centro[0] + tamanho / 2, centro[1] - tamanho / 2],
            [centro[0] + tamanho / 2, centro[1] + tamanho / 2],
            [centro[0] - tamanho / 2, centro[1] + tamanho / 2],
        ],
        dtype=np.float32,
    )


def ponto_do_tabuleiro(tabuleiro_pts, u, v):
    p1, p2, p3, p4 = tabuleiro_pts
    topo = interpolar(p1, p2, u)
    base = interpolar(p4, p3, u)
    return interpolar(topo, base, v)


def pontos_da_celula(tabuleiro_pts, linha, coluna, margem=0.14):
    u0 = coluna / 3 + margem / 3
    u1 = (coluna + 1) / 3 - margem / 3
    v0 = linha / 3 + margem / 3
    v1 = (linha + 1) / 3 - margem / 3

    return np.array(
        [
            ponto_do_tabuleiro(tabuleiro_pts, u0, v0),
            ponto_do_tabuleiro(tabuleiro_pts, u1, v0),
            ponto_do_tabuleiro(tabuleiro_pts, u1, v1),
            ponto_do_tabuleiro(tabuleiro_pts, u0, v1),
        ],
        dtype=np.float32,
    )


def centro_da_celula(tabuleiro_pts, linha, coluna):
    return ponto_do_tabuleiro(tabuleiro_pts, (coluna + 0.5) / 3, (linha + 0.5) / 3)


def ponto_para_celula(tabuleiro_pts, ponto):
    destino = np.array([[0, 0], [3, 0], [3, 3], [0, 3]], dtype=np.float32)
    matriz = cv2.getPerspectiveTransform(tabuleiro_pts.astype(np.float32), destino)
    ponto_arr = np.array([[ponto]], dtype=np.float32)
    convertido = cv2.perspectiveTransform(ponto_arr, matriz)[0][0]
    coluna_float, linha_float = convertido

    if not (0 <= coluna_float < 3 and 0 <= linha_float < 3):
        return None

    return int(linha_float), int(coluna_float)


def desenhar_linha_animada(frame, p1, p2, progresso, cor, espessura):
    destino = interpolar(p1, p2, progresso)
    cv2.line(frame, tuple(p1.astype(int)), tuple(destino.astype(int)), cor, espessura)


def desenhar_x(frame, pts, tempo, mascarar=True, progresso=1.0):
    pts = pts.astype(np.float32)
    p1, p2, p3, p4 = pts

    if mascarar:
        mascarar_area(frame, pts)

    pulso = int(7 + 3 * ((np.sin(tempo * 6.0) + 1) / 2))
    progresso_final = progresso if progresso < 1.0 else 1.0

    desenhar_linha_animada(frame, p1, p3, progresso_final, VERMELHO, pulso + 4)
    desenhar_linha_animada(frame, p2, p4, progresso_final, VERMELHO, pulso + 4)
    desenhar_linha_animada(frame, p1, p3, progresso_final, (40, 40, 255), pulso)
    desenhar_linha_animada(frame, p2, p4, progresso_final, (40, 40, 255), pulso)


def desenhar_o(frame, pts, tempo, mascarar=True, progresso=1.0):
    pts = pts.astype(np.float32)

    if mascarar:
        mascarar_area(frame, pts)

    centro = np.mean(pts, axis=0).astype(int)
    largura = np.linalg.norm(pts[0] - pts[1])
    altura = np.linalg.norm(pts[1] - pts[2])
    pulso = (np.sin(tempo * 5.0) + 1) / 2
    raio = int(min(largura, altura) * (0.30 + pulso * 0.07) * max(progresso, 0.08))
    espessura = int(7 + pulso * 4)
    inicio = int((tempo * 140) % 360)
    arco = int(300 * progresso)

    cv2.ellipse(frame, tuple(centro), (raio, raio), 0, inicio, inicio + arco, AZUL, espessura + 4)
    cv2.ellipse(frame, tuple(centro), (raio, raio), 0, inicio, inicio + arco, (255, 150, 50), espessura)


def desenhar_tabuleiro(frame, tabuleiro_pts, tempo):
    tabuleiro_int = tabuleiro_pts.astype(np.int32)
    cv2.fillConvexPoly(frame, tabuleiro_int, BRANCO)

    for i in range(1, 3):
        t = i / 3
        a = ponto_do_tabuleiro(tabuleiro_pts, t, 0).astype(int)
        b = ponto_do_tabuleiro(tabuleiro_pts, t, 1).astype(int)
        c = ponto_do_tabuleiro(tabuleiro_pts, 0, t).astype(int)
        d = ponto_do_tabuleiro(tabuleiro_pts, 1, t).astype(int)
        cv2.line(frame, tuple(a), tuple(b), VERDE, 5)
        cv2.line(frame, tuple(c), tuple(d), VERDE, 5)

    varredura = (tempo * 0.8) % 1
    inicio = ponto_do_tabuleiro(tabuleiro_pts, 0, varredura).astype(int)
    fim = ponto_do_tabuleiro(tabuleiro_pts, 1, varredura).astype(int)

    cv2.polylines(frame, [tabuleiro_int], True, VERDE_ESCURO, 5)
    cv2.line(frame, tuple(inicio), tuple(fim), AMARELO, 3)


def desenhar_pecas_salvas(frame, estado, tempo):
    for linha in range(3):
        for coluna in range(3):
            simbolo = estado.celulas[linha][coluna]

            if simbolo is None:
                continue

            pts_celula = pontos_da_celula(estado.tabuleiro_pts, linha, coluna)

            if simbolo == "X":
                desenhar_x(frame, pts_celula, tempo, mascarar=False)
            elif simbolo == "O":
                desenhar_o(frame, pts_celula, tempo, mascarar=False)


def desenhar_previa_candidato(frame, estado, tempo):
    if estado.candidato is None:
        return

    simbolo, linha, coluna = estado.candidato
    progresso = estado.progresso_candidato(tempo)
    pts_celula = pontos_da_celula(estado.tabuleiro_pts, linha, coluna)

    if simbolo == "X":
        desenhar_x(frame, pts_celula, tempo, mascarar=False, progresso=progresso)
    elif simbolo == "O":
        desenhar_o(frame, pts_celula, tempo, mascarar=False, progresso=progresso)

    centro = centro_da_celula(estado.tabuleiro_pts, linha, coluna).astype(int)
    segundos_restantes = max(TEMPO_CONFIRMACAO - (tempo - estado.candidato_inicio), 0)
    texto = f"{segundos_restantes:.1f}s"
    cv2.putText(frame, texto, tuple(centro + np.array([-30, 10])), cv2.FONT_HERSHEY_SIMPLEX, 0.7, PRETO, 2)


def verificar_vitoria(celulas):
    linhas = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for linha in linhas:
        valores = [celulas[l][c] for l, c in linha]

        if valores[0] is not None and valores.count(valores[0]) == 3:
            return valores[0], linha

    return None, None


def desenhar_resultado(frame, estado):
    if estado.linha_vencedora is None or estado.tabuleiro_pts is None:
        return

    inicio_linha, _, fim_linha = estado.linha_vencedora
    inicio = centro_da_celula(estado.tabuleiro_pts, *inicio_linha).astype(int)
    fim = centro_da_celula(estado.tabuleiro_pts, *fim_linha).astype(int)
    cv2.line(frame, tuple(inicio), tuple(fim), AMARELO, 10)


def desenhar_hud(frame, estado, tempo):
    if estado.tabuleiro_pts is None:
        linhas = ["Aponte o QR TABULEIRO para calibrar.", "Depois use um QR X/O por vez."]
    elif estado.vencedor:
        linhas = [f"Vencedor: {estado.vencedor}", "R reinicia | F tela cheia | ESC sai"]
    elif estado.empate:
        linhas = ["Empate!", "R reinicia | F tela cheia | ESC sai"]
    else:
        linhas = [f"Turno: {estado.jogador_atual}", "Segure o QR na celula por 3s."]

        if estado.candidato is not None:
            simbolo, linha, coluna = estado.candidato
            progresso = estado.progresso_candidato(tempo) * 100
            linhas.append(f"Confirmando {simbolo}: L{linha + 1} C{coluna + 1} ({progresso:.0f}%)")

    x, y = 12, 28
    largura = 430
    altura = 30 + len(linhas) * 26
    cv2.rectangle(frame, (8, 8), (8 + largura, 8 + altura), (255, 255, 255), -1)
    cv2.rectangle(frame, (8, 8), (8 + largura, 8 + altura), (210, 210, 210), 2)

    for i, linha in enumerate(linhas):
        cv2.putText(frame, linha, (x, y + i * 26), cv2.FONT_HERSHEY_SIMPLEX, 0.65, PRETO, 2)


def criar_janela_video():
    flags = cv2.WINDOW_NORMAL

    if hasattr(cv2, "WINDOW_FREERATIO"):
        flags |= cv2.WINDOW_FREERATIO

    cv2.namedWindow(JANELA_NOME, flags)
    cv2.resizeWindow(JANELA_NOME, 1280, 720)

    if hasattr(cv2, "WND_PROP_ASPECT_RATIO") and hasattr(cv2, "WINDOW_FREERATIO"):
        cv2.setWindowProperty(JANELA_NOME, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_FREERATIO)


def alternar_tela_cheia(tela_cheia):
    novo_estado = not tela_cheia
    modo = cv2.WINDOW_FULLSCREEN if novo_estado else cv2.WINDOW_NORMAL
    cv2.setWindowProperty(JANELA_NOME, cv2.WND_PROP_FULLSCREEN, modo)
    return novo_estado


def processar_marcadores(estado, decoded_info, points, tempo):
    if points is None:
        estado.expirar_candidato(tempo)
        return

    pecas = []

    for texto, pts in zip(decoded_info, points):
        texto = texto.strip().upper()

        if texto == "":
            continue

        pts = pts.reshape(4, 2).astype(np.float32)

        if texto == "TABULEIRO":
            estado.atualizar_tabuleiro(calcular_tabuleiro_virtual(pts))
        elif texto in ("X", "O"):
            pecas.append((texto, pts))

    if estado.tabuleiro_pts is None:
        estado.expirar_candidato(tempo)
        return

    marcou_candidato = False

    for simbolo, pts in pecas:
        centro = np.mean(pts, axis=0)
        celula = ponto_para_celula(estado.tabuleiro_pts, centro)

        if celula is None:
            continue

        linha, coluna = celula
        estado.registrar_candidato(simbolo, linha, coluna, tempo)

        if estado.candidato == (simbolo, linha, coluna):
            marcou_candidato = True

    if not marcou_candidato:
        estado.expirar_candidato(tempo)


def main():
    detector = cv2.QRCodeDetector()
    estado = EstadoJogo()

    camera_id = selecionar_camera()
    camera = CameraThread(camera_id)

    if not camera.is_opened():
        print("Erro: camera nao encontrada.")
        return

    camera.start()
    criar_janela_video()
    tela_cheia = False

    print("\nCamera iniciada em thread separada.")
    print("Fluxo novo: calibre TABULEIRO e registre X/O um por vez por 3 segundos.")
    print("Pressione F para tela cheia, R para reiniciar ou ESC para sair.")

    while True:
        ret, frame = camera.read()
        tempo = time.time()

        if not ret:
            time.sleep(0.01)
            continue

        ok, decoded_info, points, _ = detector.detectAndDecodeMulti(frame)

        if ok:
            processar_marcadores(estado, decoded_info, points, tempo)
        else:
            estado.expirar_candidato(tempo)

        if estado.tabuleiro_pts is not None:
            desenhar_tabuleiro(frame, estado.tabuleiro_pts, tempo)
            desenhar_pecas_salvas(frame, estado, tempo)
            desenhar_previa_candidato(frame, estado, tempo)
            desenhar_resultado(frame, estado)

        desenhar_hud(frame, estado, tempo)
        cv2.imshow(JANELA_NOME, frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == 27:
            break

        if tecla in (ord("r"), ord("R")):
            estado.reset()

        if tecla in (ord("f"), ord("F")):
            tela_cheia = alternar_tela_cheia(tela_cheia)

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
