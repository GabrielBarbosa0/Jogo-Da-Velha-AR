import threading
import time

import cv2
import numpy as np


BRANCO = (255, 255, 255)
VERDE = (0, 220, 80)
VERMELHO = (0, 0, 255)
AZUL = (255, 80, 0)
AMARELO = (0, 220, 255)


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


def listar_cameras(max_cameras=10):
    cameras_disponiveis = []

    print("Procurando câmeras disponíveis...")

    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)

        if cap.isOpened():
            ret, _ = cap.read()

            if ret:
                cameras_disponiveis.append(i)
                print(f"[{i}] Câmera disponível")

        cap.release()

    return cameras_disponiveis


def selecionar_camera():
    cameras = listar_cameras()

    if not cameras:
        print("Nenhuma câmera encontrada.")
        exit()

    print("\nSelecione a câmera que deseja usar:")

    for cam in cameras:
        print(f"{cam} - Câmera {cam}")

    while True:
        escolha = input("\nDigite o número da câmera: ")

        if escolha.isdigit() and int(escolha) in cameras:
            return int(escolha)

        print("Opção inválida. Tente novamente.")


def interpolar(p1, p2, t):
    return (p1 + (p2 - p1) * t).astype(int)


def mascarar_area(frame, pts, cor=BRANCO):
    cv2.fillConvexPoly(frame, pts.astype(np.int32), cor)


def desenhar_linha_animada(frame, p1, p2, progresso, cor, espessura):
    destino = interpolar(p1, p2, progresso)
    cv2.line(frame, tuple(p1.astype(int)), tuple(destino), cor, espessura)


def desenhar_x(frame, pts, tempo):
    pts = pts.astype(np.float32)
    p1, p2, p3, p4 = pts

    mascarar_area(frame, pts)

    progresso = (np.sin(tempo * 4.0) + 1) / 2
    progresso = 0.25 + progresso * 0.75
    pulso = int(7 + 3 * ((np.sin(tempo * 6.0) + 1) / 2))

    desenhar_linha_animada(frame, p1, p3, progresso, VERMELHO, pulso + 4)
    desenhar_linha_animada(frame, p2, p4, progresso, VERMELHO, pulso + 4)
    desenhar_linha_animada(frame, p1, p3, progresso, (40, 40, 255), pulso)
    desenhar_linha_animada(frame, p2, p4, progresso, (40, 40, 255), pulso)


def desenhar_o(frame, pts, tempo):
    pts = pts.astype(np.float32)
    mascarar_area(frame, pts)

    centro = np.mean(pts, axis=0).astype(int)
    largura = np.linalg.norm(pts[0] - pts[1])
    altura = np.linalg.norm(pts[1] - pts[2])
    pulso = (np.sin(tempo * 5.0) + 1) / 2
    raio = int(min(largura, altura) * (0.30 + pulso * 0.07))
    espessura = int(7 + pulso * 4)
    inicio = int((tempo * 140) % 360)

    cv2.ellipse(frame, tuple(centro), (raio, raio), 0, inicio, inicio + 300, AZUL, espessura + 4)
    cv2.ellipse(frame, tuple(centro), (raio, raio), 0, inicio, inicio + 300, (255, 150, 50), espessura)


def desenhar_tabuleiro(frame, pts, tempo):
    pts = pts.astype(np.float32)
    centro = np.mean(pts, axis=0)

    largura = np.linalg.norm(pts[0] - pts[1])
    altura = np.linalg.norm(pts[1] - pts[2])
    pulso = (np.sin(tempo * 3.0) + 1) / 2
    tamanho = max(largura, altura) * (3.4 + pulso * 0.15)

    destino = np.array(
        [
            [centro[0] - tamanho / 2, centro[1] - tamanho / 2],
            [centro[0] + tamanho / 2, centro[1] - tamanho / 2],
            [centro[0] + tamanho / 2, centro[1] + tamanho / 2],
            [centro[0] - tamanho / 2, centro[1] + tamanho / 2],
        ],
        dtype=np.float32,
    )

    p1, p2, p3, p4 = destino
    destino_int = destino.astype(np.int32)

    fundo = frame.copy()
    cv2.fillConvexPoly(fundo, destino_int, BRANCO)
    cv2.addWeighted(fundo, 0.82, frame, 0.18, 0, frame)

    for i in range(1, 3):
        t = i / 3

        a = (p1 + (p2 - p1) * t).astype(int)
        b = (p4 + (p3 - p4) * t).astype(int)
        cv2.line(frame, tuple(a), tuple(b), VERDE, 5)

        c = (p1 + (p4 - p1) * t).astype(int)
        d = (p2 + (p3 - p2) * t).astype(int)
        cv2.line(frame, tuple(c), tuple(d), VERDE, 5)

    varredura = int((tempo * 180) % max(int(tamanho), 1))
    t_varredura = varredura / tamanho
    inicio = interpolar(p1, p4, t_varredura)
    fim = interpolar(p2, p3, t_varredura)

    cv2.polylines(frame, [destino_int], True, VERDE, 5)
    cv2.line(frame, tuple(inicio), tuple(fim), AMARELO, 3)


def main():
    detector = cv2.QRCodeDetector()

    camera_id = selecionar_camera()
    camera = CameraThread(camera_id)

    if not camera.is_opened():
        print("Erro: câmera não encontrada.")
        return

    camera.start()

    print("\nCâmera iniciada em thread separada.")
    print("Detecção principal continua usando múltiplos marcadores por frame.")
    print("Pressione ESC para sair.")

    while True:
        ret, frame = camera.read()

        if not ret:
            time.sleep(0.01)
            continue

        ok, decoded_info, points, _ = detector.detectAndDecodeMulti(frame)
        tempo = time.time()

        if ok and points is not None:
            marcadores = []

            for texto, pts in zip(decoded_info, points):
                texto = texto.strip().upper()

                if texto == "":
                    continue

                marcadores.append((texto, pts.reshape(4, 2)))

            marcadores.sort(key=lambda item: 0 if item[0] == "TABULEIRO" else 1)

            for texto, pts in marcadores:

                if texto == "TABULEIRO":
                    desenhar_tabuleiro(frame, pts, tempo)

                elif texto == "X":
                    desenhar_x(frame, pts, tempo)

                elif texto == "O":
                    desenhar_o(frame, pts, tempo)

        cv2.imshow("Jogo da Velha AR - QR Code", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
