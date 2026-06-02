# Jogo da Velha AR com QR Code

Projeto de Computação Gráfica utilizando **Realidade Aumentada (AR)** e **Visão Computacional** desenvolvido em Python com OpenCV.

O sistema utiliza QR Codes como marcadores fiduciais para detectar elementos físicos através da câmera e projetar objetos gráficos virtuais diretamente sobre o ambiente real em tempo real.

## Demonstração

O projeto reconhece três tipos de marcadores:

| QR Code | Função |
|---|---|
| TABULEIRO | Calibra a área virtual do tabuleiro |
| X | Registra uma jogada do jogador X |
| O | Registra uma jogada do jogador O |

Depois que uma jogada é confirmada, ela fica salva no estado interno do jogo. Assim, o QR Code físico não precisa continuar visível para que a peça permaneça na tela.

## Lógica Atual

O projeto deixou de depender de todos os QR Codes visíveis ao mesmo tempo. O fluxo atual é:

1. O usuário aponta o QR Code `TABULEIRO` para calibrar a área do jogo.
2. O sistema salva a posição virtual do tabuleiro.
3. O jogador posiciona um QR Code `X` ou `O` dentro de uma célula.
4. Se o marcador ficar estável por 3 segundos, a jogada é confirmada.
5. A posição confirmada é salva em uma matriz 3x3.
6. A peça passa a ser renderizada pelo programa, mesmo que o QR Code físico saia da câmera.
7. O sistema alterna o turno entre `X` e `O`.
8. A vitória ou empate é verificado automaticamente.

Essa lógica reduz o problema de piscada/falha de detecção, porque o sensor não precisa rastrear todos os marcadores da partida ao mesmo tempo.

## Controles

- `ESC`: fecha o programa.
- `R`: reinicia o tabuleiro e limpa as jogadas salvas.
- `F`: alterna entre janela normal e tela cheia.

## Conceitos Aplicados

- Realidade Aumentada (AR)
- Visão Computacional
- Rastreamento de Marcadores
- Estado persistente do jogo
- Detecção de múltiplos marcadores
- Processamento de Imagem
- Renderização 2D
- Animação procedural
- Transformações Geométricas
- Interpolação Espacial
- Matriz 3x3 para lógica do jogo
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

## Funcionamento Técnico

O programa utiliza uma classe `CameraThread` para capturar frames em segundo plano. A thread principal usa o frame mais recente para executar:

- detecção de QR Codes com `QRCodeDetector.detectAndDecodeMulti`;
- calibração da área virtual do tabuleiro;
- conversão da posição do QR Code para linha/coluna da matriz 3x3;
- confirmação da jogada após 3 segundos de estabilidade;
- renderização do tabuleiro e das peças salvas;
- verificação de vitória ou empate.

A janela de vídeo é criada em modo redimensionável. Ao maximizar a janela ou pressionar `F`, a imagem da câmera passa a ocupar todo o espaço disponível da tela, em vez de ficar presa ao tamanho original da webcam.

## Tabuleiro AR

O QR Code `TABULEIRO` funciona como referência para calcular a área virtual do jogo.

A partir dele, o sistema:

- calcula o centro do marcador;
- expande uma área quadrada ao redor dele;
- aplica um fundo branco sólido;
- desenha a grade 3x3;
- mantém a última posição calibrada mesmo que o QR Code não esteja sendo detectado em todos os frames.

## Marcadores X e O

Os QR Codes `X` e `O` não são mais tratados como peças permanentes. Eles funcionam como entrada de jogada.

Quando uma peça é confirmada:

- a célula é salva na matriz;
- o QR Code físico pode sair da câmera;
- o programa continua renderizando a peça naquela posição;
- o turno passa para o outro jogador.

## Próximas Etapas

- Refinar a estabilidade da calibração do tabuleiro.
- Permitir calibração por uma grade desenhada fisicamente, sem QR Code `TABULEIRO`.
- Adicionar placar e botão visual de reinício.
- Melhorar a aparência das animações.
- Exportar vídeo demonstrativo do funcionamento.

## Relação com a Disciplina

Este projeto aplica diretamente conceitos de:

- Computação Gráfica
- Renderização
- Transformações Geométricas
- Processamento de Imagem
- Realidade Aumentada
- Visão Computacional
- Paralelismo básico com multithread
