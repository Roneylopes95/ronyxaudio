"""
PC Ronyx Download Áudio Automação  -  versão Android (Kivy)
Baixa o áudio original do vídeo (M4A) direto pela URL, sem conversão.
Use apenas com conteúdo que você tem direito de baixar.
"""
import os
import threading

from kivy.app import App
from kivy.clock import mainthread
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex, platform

Window.clearcolor = (0.04, 0.04, 0.08, 1)
CYAN, MAG = get_color_from_hex("#22d3ee"), get_color_from_hex("#d946ef")
OK, ERR = get_color_from_hex("#4ade80"), get_color_from_hex("#f87171")

KV = """
#:import hex kivy.utils.get_color_from_hex
BoxLayout:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(10)

    Image:
        source: 'logo.png'
        size_hint_y: None
        height: dp(150)
    Label:
        text: 'PC RONYX'
        bold: True
        font_size: '24sp'
        color: hex('#22d3ee')
        size_hint_y: None
        height: dp(32)
    Label:
        text: 'Download Áudio Automação'
        font_size: '15sp'
        color: hex('#d946ef')
        size_hint_y: None
        height: dp(24)

    BoxLayout:
        size_hint_y: None
        height: dp(48)
        spacing: dp(8)
        TextInput:
            id: url
            hint_text: 'Cole a URL do vídeo'
            multiline: False
            background_color: hex('#14142a')
            foreground_color: 1, 1, 1, 1
            hint_text_color: hex('#94a3b8')
            cursor_color: hex('#22d3ee')
            padding: dp(12), dp(14)
        Button:
            text: 'Colar'
            size_hint_x: None
            width: dp(80)
            background_normal: ''
            background_color: hex('#14142a')
            color: hex('#22d3ee')
            on_release: app.colar()

    Button:
        id: btn
        text: 'BAIXAR ÁUDIO'
        bold: True
        size_hint_y: None
        height: dp(52)
        background_normal: ''
        background_color: hex('#d946ef')
        on_release: app.iniciar(url.text)

    Label:
        id: status
        text: 'Aguardando URL...'
        bold: True
        font_size: '18sp'
        color: hex('#22d3ee')
        text_size: self.width, None
        halign: 'center'
        size_hint_y: None
        height: self.texture_size[1] + dp(6)
    ProgressBar:
        id: bar
        max: 100
        value: 0
        size_hint_y: None
        height: dp(14)
    Label:
        id: detalhe
        text: 'Formato: M4A (áudio original, sem conversão)'
        font_size: '13sp'
        color: hex('#94a3b8')
        text_size: self.width, None
        halign: 'center'
        valign: 'top'
"""


def fmt_bytes(n):
    if not n:
        return "?"
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


def pasta_destino():
    """Tenta a pasta Música; se não puder gravar, usa a pasta do app."""
    if platform == "android":
        from android.storage import primary_external_storage_path
        try:
            p = os.path.join(primary_external_storage_path(), "Music", "PC Ronyx")
            os.makedirs(p, exist_ok=True)
            teste = os.path.join(p, ".teste")
            open(teste, "w").close()
            os.remove(teste)
            return p
        except Exception:
            from jnius import autoclass
            act = autoclass("org.kivy.android.PythonActivity").mActivity
            return act.getExternalFilesDir(None).getAbsolutePath()
    p = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(p, exist_ok=True)
    return p


class RonyxApp(App):
    title = "PC Ronyx Download Áudio Automação"
    icon = "logo.png"

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                "android.permission.READ_MEDIA_AUDIO",
            ])

    def colar(self):
        self.root.ids.url.text = (Clipboard.paste() or "").strip()

    # ---- atualizações de tela (sempre na thread principal) ----
    @mainthread
    def status(self, titulo, detalhe="", cor=CYAN):
        i = self.root.ids
        i.status.text, i.status.color, i.detalhe.text = titulo, cor, detalhe

    @mainthread
    def barra(self, v):
        self.root.ids.bar.value = v

    @mainthread
    def liberar(self):
        self.root.ids.btn.disabled = False
        self.root.ids.btn.text = "BAIXAR ÁUDIO"

    # ---- fluxo ----
    def iniciar(self, url):
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            self.status("URL inválida", "Cole um link começando com http", ERR)
            return
        self.root.ids.btn.disabled = True
        self.root.ids.btn.text = "PROCESSANDO..."
        self.barra(0)
        self.status("Conectando...", "Buscando informações do vídeo")
        threading.Thread(target=self.baixar, args=(url,), daemon=True).start()

    def baixar(self, url):
        try:
            import yt_dlp

            pasta = pasta_destino()

            def hook(d):
                if d["status"] == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate")
                    feito = d.get("downloaded_bytes", 0)
                    if total:
                        pct = feito / total * 100
                        self.barra(pct)
                        self.status(f"Baixando... {pct:.0f}%",
                                    f"{fmt_bytes(feito)} de {fmt_bytes(total)}  |  "
                                    f"{fmt_bytes(d.get('speed'))}/s")
                    else:
                        self.status("Baixando...", f"{fmt_bytes(feito)} baixados")
                elif d["status"] == "finished":
                    self.status("Finalizando...", "Salvando arquivo")

            opts = {
                "format": "bestaudio[ext=m4a]/bestaudio",
                "outtmpl": os.path.join(pasta, "%(title)s.%(ext)s"),
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "noprogress": True,
                "cachedir": False,
                "progress_hooks": [hook],
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                reqs = info.get("requested_downloads") or []
                caminho = (reqs[0].get("filepath") if reqs else None) or ydl.prepare_filename(info)
            self.barra(100)
            self.status("Concluído!", f"Salvo em:\n{caminho}", OK)
        except Exception as e:
            self.barra(0)
            self.status("Erro", str(e)[:400], ERR)
        finally:
            self.liberar()


if __name__ == "__main__":
    RonyxApp().run()
