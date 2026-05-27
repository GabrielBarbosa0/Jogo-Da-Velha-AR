# Jogo da Velha AR com QR Code

Projeto de Computação Gráfica utilizando **Realidade Aumentada (AR)** e **Visão Computacional** desenvolvido em Python com OpenCV.

O sistema utiliza QR Codes como marcadores fiduciais para detectar elementos físicos através da câmera e projetar objetos gráficos virtuais diretamente sobre o ambiente real em tempo real.

## Demonstração

O projeto reconhece três tipos de marcadores:

| QR Code | Função |
|---|---|
| TABULEIRO | Gera o tabuleiro AR |
| X | Projeta um X virtual animado |
| O | Projeta um círculo virtual animado |

Os elementos acompanham:

- posição;
- escala;
- inclinação;
- rotação do marcador.

Além disso, o overlay cobre o QR Code detectado com uma área branca antes de desenhar o elemento virtual, melhorando a leitura visual da cena.

## Conceitos Aplicados

- Realidade Aumentada (AR)
- Visão Computacional
- Rastreamento de Marcadores
- Detecção de múltiplos marcadores
- Processamento de Imagem
- Renderização 2D
- Animação procedural
- Transformações Geométricas
- Interpolação Espacial
- Pipeline Gráfico
- Captura de vídeo com multithread

## Tecnologias Utilizadas

- Python
- OpenCV
- NumPy
- threading
- qrcode
- Pillow

## Estrutura do Projeto

```text
.
├── jogo_da_velha_ar.py
├── gerar_qrcodes.py
├── qr_TABULEIRO.png
├── qr_X.png
├── qr_O.png
├── requirements.txt
├── README.md
└── venv/
```

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/jogo-da-velha-ar.git
```

### 2. Entrar na pasta do projeto

```bash
cd jogo-da-velha-ar
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual no Windows

```bash
venv\Scripts\activate
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

## Executando o Projeto

### Gerar os QR Codes

```bash
python gerar_qrcodes.py
```

### Executar aplicação AR

```bash
python jogo_da_velha_ar.py
```

## Webcam do Celular

O projeto suporta webcam virtual via celular utilizando aplicativos como:

- DroidCam
- Iriun Webcam
- Camo

Ao iniciar o programa, será exibida uma lista de câmeras disponíveis para seleção.

## Funcionamento

1. O sistema abre a câmera em uma thread separada.
2. A thread principal processa o frame mais recente.
3. QR Codes são detectados usando `QRCodeDetector.detectAndDecodeMulti`.
4. O sistema consegue tratar múltiplos marcadores no mesmo frame.
5. O marcador detectado é coberto por uma base branca.
6. Elementos gráficos animados são renderizados sobre o QR Code.
7. O tabuleiro é expandido dinamicamente baseado na posição do marcador.

## Tabuleiro AR

O QR Code `TABULEIRO` funciona como marcador principal da área do jogo.

A partir dele:

- o sistema calcula proporções;
- expande a área virtual;
- aplica um fundo branco semitransparente;
- desenha o grid do jogo da velha;
- anima uma linha de varredura para dar sensação de atualização.

## Marcador X

O QR Code `X` renderiza:

- uma base branca sobre o marcador;
- um X vermelho animado;
- linhas que crescem em ciclo contínuo;
- espessura pulsante.

## Marcador O

O QR Code `O` renderiza:

- uma base branca sobre o marcador;
- um círculo azul animado;
- raio pulsante;
- arco rotativo para simular movimento.

## Multithread e Multimarcadores

O projeto utiliza uma classe `CameraThread` para separar a captura da câmera do processamento principal. A câmera fica lendo frames em segundo plano, enquanto a thread principal executa detecção, cálculo geométrico e renderização.

A detecção de múltiplos marcadores continua sendo feita pelo `detectAndDecodeMulti`, permitindo reconhecer `TABULEIRO`, `X` e `O` simultaneamente no mesmo frame.

## Próximas Etapas

- Sistema lógico completo do jogo da velha
- Associação de peças X/O às células do tabuleiro
- Detecção automática de vitória
- Melhorias de estabilidade no tracking
- HUD interativa
- Refinamento das animações
- Renderização 3D real

## Relação com a Disciplina

Este projeto aplica diretamente conceitos de:

- Computação Gráfica
- Renderização
- Transformações Geométricas
- Processamento de Imagem
- Realidade Aumentada
- Visão Computacional
- Paralelismo básico com multithread
