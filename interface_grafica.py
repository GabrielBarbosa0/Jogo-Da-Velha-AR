import threading
import tkinter as tk
from tkinter import ttk


COR_FUNDO = "#111418"
COR_PAINEL = "#1D232A"
COR_BORDA = "#303841"
COR_TEXTO = "#F5F7FA"
COR_TEXTO_SECUNDARIO = "#AAB4BF"
COR_DESTAQUE = "#40D667"
COR_DESTAQUE_ATIVO = "#35BB59"
COR_X = "#FF4D5A"
COR_O = "#4FA8FF"


class InterfaceInicial:
    def __init__(self, buscar_cameras):
        self.buscar_cameras = buscar_cameras
        self.camera_selecionada = None
        self.tela_cheia = True
        self.busca_em_andamento = False
        self.resultado_busca = None

        self.root = tk.Tk()
        self.root.title("Jogo da Velha AR")
        self.root.configure(bg=COR_FUNDO)
        self.root.attributes("-fullscreen", True)
        self.root.minsize(820, 560)
        self.root.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.root.bind("<F11>", self.alternar_tela_cheia)
        self.root.bind("<Escape>", self.sair_tela_cheia)

        self.estilo = ttk.Style(self.root)
        self.estilo.theme_use("clam")
        self.estilo.configure(
            "Camera.TCombobox",
            fieldbackground=COR_PAINEL,
            background=COR_PAINEL,
            foreground=COR_TEXTO,
            arrowcolor=COR_TEXTO,
            bordercolor=COR_BORDA,
            lightcolor=COR_BORDA,
            darkcolor=COR_BORDA,
            padding=10,
            font=("Segoe UI", 13),
        )
        self.estilo.map(
            "Camera.TCombobox",
            fieldbackground=[("readonly", COR_PAINEL)],
            foreground=[("readonly", COR_TEXTO)],
            selectbackground=[("readonly", COR_PAINEL)],
            selectforeground=[("readonly", COR_TEXTO)],
        )

        self.mostrar_inicio()

    def executar(self):
        self.root.mainloop()
        return self.camera_selecionada

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_barra_superior(self, titulo="JOGO DA VELHA AR"):
        barra = tk.Frame(self.root, bg=COR_FUNDO)
        barra.pack(fill="x", padx=34, pady=(24, 0))

        marca = tk.Label(
            barra,
            text=titulo,
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=("Segoe UI Semibold", 15),
        )
        marca.pack(side="left")

        dica = tk.Label(
            barra,
            text="F11  Tela cheia",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 10),
        )
        dica.pack(side="right")

    def criar_botao(self, parent, texto, comando, destaque=True, largura=22):
        fundo = COR_DESTAQUE if destaque else COR_PAINEL
        ativo = COR_DESTAQUE_ATIVO if destaque else COR_BORDA
        cor_texto = "#07110A" if destaque else COR_TEXTO

        return tk.Button(
            parent,
            text=texto,
            command=comando,
            width=largura,
            height=2,
            bg=fundo,
            fg=cor_texto,
            activebackground=ativo,
            activeforeground=cor_texto,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI Semibold", 14),
        )

    def desenhar_tabuleiro_decorativo(self, canvas, tamanho):
        margem = 18
        passo = (tamanho - margem * 2) / 3

        for i in range(1, 3):
            posicao = margem + passo * i
            canvas.create_line(
                posicao,
                margem,
                posicao,
                tamanho - margem,
                fill=COR_DESTAQUE,
                width=5,
            )
            canvas.create_line(
                margem,
                posicao,
                tamanho - margem,
                posicao,
                fill=COR_DESTAQUE,
                width=5,
            )

        def centro(linha, coluna):
            return (
                margem + passo * (coluna + 0.5),
                margem + passo * (linha + 0.5),
            )

        for linha, coluna in [(0, 0), (1, 2), (2, 1)]:
            x, y = centro(linha, coluna)
            raio = passo * 0.25
            canvas.create_oval(
                x - raio,
                y - raio,
                x + raio,
                y + raio,
                outline=COR_O,
                width=7,
            )

        for linha, coluna in [(0, 2), (1, 1), (2, 0)]:
            x, y = centro(linha, coluna)
            raio = passo * 0.24
            canvas.create_line(
                x - raio,
                y - raio,
                x + raio,
                y + raio,
                fill=COR_X,
                width=7,
                capstyle="round",
            )
            canvas.create_line(
                x + raio,
                y - raio,
                x - raio,
                y + raio,
                fill=COR_X,
                width=7,
                capstyle="round",
            )

    def mostrar_inicio(self):
        self.limpar_tela()
        self.criar_barra_superior()

        conteudo = tk.Frame(self.root, bg=COR_FUNDO)
        conteudo.pack(expand=True, fill="both", padx=40, pady=20)

        centro = tk.Frame(conteudo, bg=COR_FUNDO)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(
            centro,
            text="Jogo da Velha\nem Realidade Aumentada",
            justify="center",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=("Segoe UI Semibold", 32),
        )
        titulo.pack(pady=(0, 12))

        subtitulo = tk.Label(
            centro,
            text="Calibre o tabuleiro, posicione os marcadores e jogue pela câmera.",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 13),
        )
        subtitulo.pack(pady=(0, 22))

        tamanho = min(280, max(210, int(self.root.winfo_screenheight() * 0.32)))
        canvas = tk.Canvas(
            centro,
            width=tamanho,
            height=tamanho,
            bg=COR_PAINEL,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
        )
        canvas.pack(pady=(0, 26))
        self.desenhar_tabuleiro_decorativo(canvas, tamanho)

        self.criar_botao(centro, "▶  JOGAR", self.mostrar_selecao_camera).pack()

        rodape = tk.Label(
            self.root,
            text="Computação Gráfica • Python • OpenCV",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 10),
        )
        rodape.pack(pady=(0, 22))

    def mostrar_selecao_camera(self):
        self.limpar_tela()
        self.criar_barra_superior("CONFIGURAÇÃO DA PARTIDA")

        conteudo = tk.Frame(self.root, bg=COR_FUNDO)
        conteudo.pack(expand=True, fill="both", padx=40, pady=30)

        painel = tk.Frame(
            conteudo,
            bg=COR_PAINEL,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            padx=42,
            pady=38,
        )
        painel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            painel,
            text="Selecionar câmera",
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=("Segoe UI Semibold", 26),
        ).pack(anchor="w")

        tk.Label(
            painel,
            text="Escolha o dispositivo que será usado para capturar o tabuleiro e as jogadas.",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 12),
            wraplength=560,
            justify="left",
        ).pack(anchor="w", pady=(8, 28))

        self.camera_var = tk.StringVar()
        self.combo_camera = ttk.Combobox(
            painel,
            textvariable=self.camera_var,
            state="readonly",
            width=42,
            style="Camera.TCombobox",
        )
        self.combo_camera.pack(fill="x")

        self.status_camera = tk.Label(
            painel,
            text="Procurando câmeras disponíveis...",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 10),
        )
        self.status_camera.pack(anchor="w", pady=(10, 24))

        acoes = tk.Frame(painel, bg=COR_PAINEL)
        acoes.pack(fill="x")

        self.botao_voltar = self.criar_botao(
            acoes,
            "VOLTAR",
            self.mostrar_inicio,
            destaque=False,
            largura=14,
        )
        self.botao_voltar.pack(side="left")

        self.botao_atualizar = self.criar_botao(
            acoes,
            "ATUALIZAR",
            self.iniciar_busca_cameras,
            destaque=False,
            largura=14,
        )
        self.botao_atualizar.pack(side="left", padx=10)

        self.botao_iniciar = self.criar_botao(
            acoes,
            "INICIAR JOGO",
            self.confirmar_camera,
            largura=18,
        )
        self.botao_iniciar.pack(side="right")
        self.botao_iniciar.configure(state="disabled")

        self.iniciar_busca_cameras()

    def iniciar_busca_cameras(self):
        if self.busca_em_andamento:
            return

        self.busca_em_andamento = True
        self.resultado_busca = None
        self.status_camera.configure(text="Procurando câmeras disponíveis...", fg=COR_TEXTO_SECUNDARIO)
        self.combo_camera.configure(values=())
        self.camera_var.set("")
        self.botao_iniciar.configure(state="disabled")
        self.botao_atualizar.configure(state="disabled")
        self.botao_voltar.configure(state="disabled")

        thread = threading.Thread(target=self.executar_busca_cameras, daemon=True)
        thread.start()
        self.root.after(100, self.verificar_resultado_busca)

    def executar_busca_cameras(self):
        try:
            self.resultado_busca = self.buscar_cameras()
        except Exception:
            self.resultado_busca = []

    def verificar_resultado_busca(self):
        if self.resultado_busca is None:
            self.root.after(100, self.verificar_resultado_busca)
            return

        cameras = self.resultado_busca
        self.busca_em_andamento = False
        self.botao_atualizar.configure(state="normal")
        self.botao_voltar.configure(state="normal")

        if not cameras:
            self.status_camera.configure(
                text="Nenhuma câmera encontrada. Conecte um dispositivo e tente novamente.",
                fg=COR_X,
            )
            return

        opcoes = [f"Câmera {camera_id}  •  dispositivo {camera_id}" for camera_id in cameras]
        self.combo_camera.configure(values=opcoes)
        self.combo_camera.current(0)
        self.status_camera.configure(
            text=f"{len(cameras)} câmera(s) encontrada(s).",
            fg=COR_DESTAQUE,
        )
        self.botao_iniciar.configure(state="normal")

    def confirmar_camera(self):
        selecao = self.combo_camera.current()

        if selecao < 0 or not self.resultado_busca:
            return

        self.camera_selecionada = self.resultado_busca[selecao]
        self.root.destroy()

    def alternar_tela_cheia(self, _evento=None):
        self.tela_cheia = not self.tela_cheia
        self.root.attributes("-fullscreen", self.tela_cheia)

    def sair_tela_cheia(self, _evento=None):
        if self.tela_cheia:
            self.tela_cheia = False
            self.root.attributes("-fullscreen", False)
        else:
            self.cancelar()

    def cancelar(self):
        self.camera_selecionada = None
        self.root.destroy()


def selecionar_camera_grafica(buscar_cameras):
    return InterfaceInicial(buscar_cameras).executar()
