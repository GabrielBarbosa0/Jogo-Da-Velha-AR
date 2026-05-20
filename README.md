# 🎮 Jogo da Velha AR com QR Code

Projeto de Computação Gráfica utilizando **Realidade Aumentada (AR)** e **Visão Computacional** desenvolvido em Python com OpenCV.

O sistema utiliza QR Codes como marcadores fiduciais para detectar elementos físicos através da câmera e projetar objetos gráficos virtuais diretamente sobre o ambiente real em tempo real.

---

# 📷 Demonstração

O projeto reconhece três tipos de marcadores:

| QR Code | Função |
|---|---|
| TABULEIRO | Gera o tabuleiro AR |
| X | Projeta um X virtual |
| O | Projeta um círculo virtual |

Os elementos acompanham:
- posição;
- escala;
- inclinação;
- rotação do marcador.

---

# 🧠 Conceitos Aplicados

- Realidade Aumentada (AR)
- Visão Computacional
- Rastreamento de Marcadores
- Processamento de Imagem
- Renderização 2D
- Transformações Geométricas
- Interpolação Espacial
- Pipeline Gráfico

---

# 🛠 Tecnologias Utilizadas

- Python
- OpenCV
- NumPy
- qrcode
- Pillow

---

# 📂 Estrutura do Projeto

```text
.
├── ar_jogo_da_velha.py
├── gerar_qrcodes.py
├── qr_TABULEIRO.png
├── qr_X.png
├── qr_O.png
├── requirements.txt
├── README.md
└── venv/
```

---

# ⚙️ Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/jogo-da-velha-ar.git
```

---

## 2. Entrar na pasta do projeto

```bash
cd jogo-da-velha-ar
```

---

## 3. Criar ambiente virtual

### Windows

```bash
python -m venv venv
```

---

## 4. Ativar ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

---

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando o Projeto

## Gerar os QR Codes

```bash
python gerar_qrcodes.py
```

---

## Executar aplicação AR

```bash
python ar_jogo_da_velha.py
```

---

# 📱 Webcam do Celular

O projeto suporta webcam virtual via celular utilizando aplicativos como:

- DroidCam
- Iriun Webcam
- Camo

Ao iniciar o programa, será exibida uma lista de câmeras disponíveis para seleção.

---

# 🎯 Funcionamento

1. O sistema abre a câmera em tempo real.
2. QR Codes são detectados usando `QRCodeDetector`.
3. O marcador é rastreado continuamente.
4. Elementos gráficos são renderizados sobre o QR Code.
5. O tabuleiro é expandido dinamicamente baseado na posição do marcador.

---

# 🟩 Tabuleiro AR

O QR Code `TABULEIRO` funciona como marcador principal da área do jogo.

A partir dele:
- o sistema calcula proporções;
- expande a área virtual;
- desenha o grid do jogo da velha.

---

# ❌ Marcador X

O QR Code `X` renderiza:
- um X vermelho;
- alinhado à perspectiva do marcador;
- atualizado em tempo real.

---

# ⭕ Marcador O

O QR Code `O` renderiza:
- um círculo azul;
- proporcional ao tamanho do QR Code;
- adaptado à inclinação da câmera.

---

# 🚀 Próximas Etapas

- Sistema lógico completo do jogo da velha
- Detecção automática de vitória
- Melhorias de estabilidade no tracking
- Renderização 3D real
- HUD interativa
- Física básica
- Peças com modelos 3D
- Interação por mão/dedos

---

# 📚 Relação com a Disciplina

Este projeto aplica diretamente conceitos de:
- Computação Gráfica
- Renderização
- Transformações Geométricas
- Processamento de Imagem
- Realidade Aumentada
- Visão Computacional

