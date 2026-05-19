import cv2
import numpy as np


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


def desenhar_x(frame, pts):
    pts = pts.astype(int)
    p1, p2, p3, p4 = pts

    cv2.line(frame, tuple(p1), tuple(p3), (0, 0, 255), 8)
    cv2.line(frame, tuple(p2), tuple(p4), (0, 0, 255), 8)


def desenhar_o(frame, pts):
    pts = pts.astype(int)
    centro = np.mean(pts, axis=0).astype(int)

    largura = np.linalg.norm(pts[0] - pts[1])
    altura = np.linalg.norm(pts[1] - pts[2])
    raio = int(min(largura, altura) * 0.35)

    cv2.circle(frame, tuple(centro), raio, (255, 0, 0), 8)


def desenhar_tabuleiro(frame, pts):
    pts = pts.astype(np.float32)
    centro = np.mean(pts, axis=0)

    largura = np.linalg.norm(pts[0] - pts[1])
    altura = np.linalg.norm(pts[1] - pts[2])
    tamanho = max(largura, altura) * 3.5

    destino = np.array([
        [centro[0] - tamanho / 2, centro[1] - tamanho / 2],
        [centro[0] + tamanho / 2, centro[1] - tamanho / 2],
        [centro[0] + tamanho / 2, centro[1] + tamanho / 2],
        [centro[0] - tamanho / 2, centro[1] + tamanho / 2],
    ], dtype=np.int32)

    p1, p2, p3, p4 = destino

    for i in range(1, 3):
        t = i / 3

        a = (p1 + (p2 - p1) * t).astype(int)
        b = (p4 + (p3 - p4) * t).astype(int)
        cv2.line(frame, tuple(a), tuple(b), (0, 255, 0), 4)

        c = (p1 + (p4 - p1) * t).astype(int)
        d = (p2 + (p3 - p2) * t).astype(int)
        cv2.line(frame, tuple(c), tuple(d), (0, 255, 0), 4)

    cv2.polylines(frame, [destino], True, (0, 255, 0), 4)


def main():
    detector = cv2.QRCodeDetector()

    camera_id = selecionar_camera()
    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print("Erro: câmera não encontrada.")
        return

    print("\nCâmera iniciada.")
    print("Pressione ESC para sair.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar imagem da câmera.")
            break

        ok, decoded_info, points, _ = detector.detectAndDecodeMulti(frame)

        if ok and points is not None:
            for texto, pts in zip(decoded_info, points):
                texto = texto.strip().upper()

                if texto == "":
                    continue

                pts = pts.reshape(4, 2)

                if texto == "TABULEIRO":
                    desenhar_tabuleiro(frame, pts)

                elif texto == "X":
                    desenhar_x(frame, pts)

                elif texto == "O":
                    desenhar_o(frame, pts)

                cv2.polylines(frame, [pts.astype(int)], True, (255, 255, 0), 2)

                cv2.putText(
                    frame,
                    texto,
                    tuple(pts[0].astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

        cv2.imshow("Jogo da Velha AR - QR Code", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()