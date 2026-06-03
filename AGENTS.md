# AGENTS.md

## Contexto do Projeto

Este repositório contém um projeto de Computação Gráfica: um Jogo da Velha com Realidade Aumentada usando Python, OpenCV, QR Codes e conceitos de Visão Computacional.

O arquivo principal é:

```text
jogo_da_velha_ar.py
```

O documento técnico do projeto fica em:

```text
docs/TDD.md
```

## Objetivo Atual

O sistema deve permitir uma partida de jogo da velha em AR sem depender de todos os QR Codes visíveis ao mesmo tempo.

A lógica atual usa estado persistente:

1. O QR `TABULEIRO` calibra a área virtual do jogo.
2. O QR `X` ou `O` é usado apenas para registrar uma jogada.
3. Após o tempo de confirmação, a jogada é salva em uma matriz 3x3.
4. O programa renderiza a peça salva mesmo que o QR Code físico saia da câmera.
5. O sistema alterna turno e verifica vitória/empate.

## Comandos Úteis

Criar ambiente virtual:

```powershell
python -m venv venv
```

Ativar ambiente virtual no Windows:

```powershell
.\venv\Scripts\activate
```

Instalar dependências:

```powershell
pip install -r requirements.txt
```

Gerar QR Codes:

```powershell
python gerar_qrcodes.py
```

Executar o projeto:

```powershell
python jogo_da_velha_ar.py
```

Validar sintaxe:

```powershell
python -m py_compile jogo_da_velha_ar.py
```

## Controles da Aplicação

- `ESC`: sair.
- `R`: reiniciar partida.
- `F`: alternar tela cheia.

## Diretrizes de Edição

- Preserve a lógica de estado persistente do jogo.
- Evite voltar para uma abordagem que dependa de rastrear todos os QR Codes continuamente.
- Ao alterar o tempo de confirmação, ajuste a constante `TEMPO_CONFIRMACAO`.
- Ao alterar o tamanho da grade, ajuste a constante `TAMANHO_TABULEIRO`.
- Não inclua a pasta `venv/` em commits.
- Não inclua `__pycache__/` em commits.
- Evite commitar arquivos temporários, vídeos ou PDFs de entrega sem pedido explícito.
- Antes de commitar código Python, rode `python -m py_compile jogo_da_velha_ar.py`.

## Arquitetura Resumida

Principais componentes:

- `CameraThread`: captura frames em thread separada.
- `EstadoJogo`: mantém matriz 3x3, turno, candidato, vitória e empate.
- `processar_marcadores`: interpreta QR Codes detectados.
- `ponto_para_celula`: converte posição do marcador para célula da matriz.
- `desenhar_tabuleiro`: renderiza a grade AR.
- `desenhar_pecas_salvas`: renderiza jogadas confirmadas.
- `verificar_vitoria`: identifica combinações vencedoras.

## Cuidados Técnicos

- OpenCV usa imagens em formato BGR, não RGB.
- A câmera pode falhar por iluminação ruim, QR Code pequeno ou movimento brusco.
- A confirmação de jogada depende de estabilidade temporal.
- A tela cheia é controlada pela janela do OpenCV, não por interface web.
- O projeto ainda é um protótipo acadêmico; prefira mudanças simples, explicáveis e fáceis de demonstrar.

## Documentação

Ao alterar comportamento importante, atualize:

```text
README.md
docs/TDD.md
```

Se a mudança for apenas visual ou pequena, atualizar o README pode ser suficiente.
