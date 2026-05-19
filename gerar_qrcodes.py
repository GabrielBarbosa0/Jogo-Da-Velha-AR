import qrcode

codigos = ["TABULEIRO", "X", "O"]

for texto in codigos:
    img = qrcode.make(texto)
    img.save(f"qr_{texto}.png")

print("QR Codes gerados!")