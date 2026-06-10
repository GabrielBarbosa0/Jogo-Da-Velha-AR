# Jogo da Velha AR com QR Code

Projeto de Computação Gráfica utilizando **Realidade Aumentada (AR)** e **Visão Computacional** desenvolvido em Python com OpenCV.

O sistema utiliza QR Codes como marcadores fiduciais para detectar elementos físicos pela câmera e projetar objetos gráficos virtuais diretamente sobre o ambiente real em tempo real.

Ao executar o projeto, uma interface gráfica em tela cheia apresenta o botão **Jogar**. Depois dele, o usuário escolhe a câmera que será utilizada antes de iniciar a captura e a partida.

## Vídeo Demonstrativo

[![Demonstração do projeto Jogo da Velha AR](https://img.youtube.com/vi/0WJbqrRqtr0/hqdefault.jpg)](https://youtu.be/0WJbqrRqtr0)

Clique na imagem para assistir à demonstração do projeto no YouTube.

## Como Funciona

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
4. Se o marcador ficar estável por 2 segundos, a jogada é confirmada.
5. A posição confirmada é salva em uma matriz 3x3.
6. A peça passa a ser renderizada pelo programa, mesmo que o QR Code físico saia da câmera.
7. O sistema alterna o turno entre `X` e `O`.
8. A vitória ou empate é verificado automaticamente.

Essa lógica reduz o problema de piscada/falha de detecção, porque o sensor não precisa rastrear todos os marcadores da partida ao mesmo tempo.

## Controles

### Interface inicial

- `Jogar`: abre a seleção de câmera.
- `Iniciar jogo`: confirma a câmera selecionada e inicia a captura.
- `Atualizar`: procura novamente por dispositivos de câmera.
- `F11`: alterna a interface inicial entre janela e tela cheia.
- `ESC`: sai da tela cheia; quando já estiver em janela, fecha a interface.

### Durante a partida

- `ESC`: fecha o programa.
- `R`: reinicia o tabuleiro e limpa as jogadas salvas.
- `F`: alterna entre janela normal e tela cheia.

## Conceitos Aplicados

- Realidade Aumentada (AR)
- Visão Computacional
- Rastreamento de marcadores
- Estado persistente do jogo
- Detecção de múltiplos marcadores
- Processamento de imagem
- Renderização 2D
- Animação procedural
- Transformações geométricas
- Interpolação espacial
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
├── AGENTS.md
├── docs/
│   └── TDD.md
├── gerar_qrcodes.py
├── interface_grafica.py
├── jogo_da_velha_ar.py
├── qr_TABULEIRO.png
├── qr_X.png
├── qr_O.png
├── README.md
└── requirements.txt
```

## Documentação

- [TDD técnico do projeto](docs/TDD.md)
- [Instruções para agentes e colaboradores](AGENTS.md)

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/GabrielBarbosa0/Jogo-Da-Velha-AR.git
```

### 2. Entrar na pasta do projeto

```bash
cd Jogo-Da-Velha-AR
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

Ao iniciar, o programa abre a interface gráfica para escolha da câmera.

O fluxo de inicialização é:

1. A interface abre em tela cheia.
2. O usuário pressiona **Jogar**.
3. O sistema procura as câmeras disponíveis.
4. O usuário seleciona uma câmera.
5. Ao pressionar **Iniciar jogo**, a interface fecha e a captura AR começa.

## Funcionamento Técnico

O programa utiliza uma classe `CameraThread` para capturar frames em segundo plano. A thread principal usa o frame mais recente para executar:

- abertura da interface gráfica com `tkinter`;
- seleção visual da câmera antes da captura;
- detecção de QR Codes com `QRCodeDetector.detectAndDecodeMulti`;
- calibração da área virtual do tabuleiro;
- conversão da posição do QR Code para linha/coluna da matriz 3x3;
- confirmação da jogada após 2 segundos de estabilidade;
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
- Transformações geométricas
- Processamento de imagem
- Realidade Aumentada
- Visão Computacional
- Paralelismo básico com multithread
