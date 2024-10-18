import os
import threading
import sys
import io
from tkinter import ttk
import tkinter as tk
from arquivos import save_log_block_comments, separation_line
from decorador import capturar_erros, register_execucao
from chromeDriver import start_driver  # Importa o driver inicializado do chromedriver.py

# Variável global para armazenar o nome do arquivo de log
log_bloqueio_file = None

@register_execucao
@capturar_erros
class RedirectText(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def write(self, message):
        self.text_widget.insert("end", message)
        self.text_widget.yview("end")

def identificar_e_executar_script(url, current_user, funcao, id_comentario, personalized_message, log_text, filtro_ativo, coments_all):
    global log_bloqueio_file

    log_bloqueio_file = os.path.join('logs', f'bloqueio_{current_user}.txt')

    try:
        driver = start_driver()  # Usa o driver inicializado do chromedriver.py

        if "facebook.com" in url:
            if funcao == "Localizar":
                from localizar import main as main_localizar
                main_localizar(url, id_comentario, log_text, driver)  # Passando o driver
            elif funcao == "Responder":
                from face import main as main_facebook
                main_facebook(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo, coments_all, extrair=False, driver=driver)  # Passando o driver
            elif funcao == "Extrair":
                from face import main as main_facebook
                main_facebook(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo, coments_all, extrair=True, driver=driver)  # Passando o driver
        elif "instagram.com" in url:
            from insta import main as main_instagram
            main_instagram(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo, driver=driver)  # Passando o driver
        else:
            print("URL não reconhecida. Por favor, insira uma URL válida do Facebook ou Instagram.")
    except Exception as e:
        print(f"Erro: {e}")

@register_execucao
@capturar_erros
def executar_script_thread(url, current_user, funcao, id_comentario, personalized_message, log_text, filtro_ativo, coments_all):
    threading.Thread(target=identificar_e_executar_script, args=(url, current_user, funcao, id_comentario, personalized_message, log_text, filtro_ativo, coments_all), daemon=True).start()

@register_execucao
@capturar_erros
def executar_script(url, current_user, funcao, id_comentario, personalized_message, log_text, filtro_ativo, coments_all):
    executar_script_thread(url, current_user, funcao, id_comentario, personalized_message, log_text, filtro_ativo, coments_all)

@register_execucao
@capturar_erros
def abrir_log():
    try:
        if getattr(sys, 'frozen', False):  # Verifica se o script está rodando como executável
            log_directory = os.path.join(os.path.dirname(sys.executable), 'logs')  # Diretório 'logs' no mesmo local do executável
        else:
            log_directory = os.path.join(os.getcwd(), 'logs')  # Diretório 'logs' no ambiente de desenvolvimento

        if os.path.exists(log_directory):
            if os.name == 'nt':  # Windows
                os.startfile(log_directory)
            elif os.name == 'posix':  # macOS ou Linux
                os.system(f'open "{log_directory}"')  # Para macOS
                # os.system(f'xdg-open "{log_directory}"')  # Para Linux
            print(f"Pasta de logs aberta: {log_directory}")
        else:
            print("Pasta de logs não encontrada.")
    except Exception as e:
        print(f"Erro ao abrir a pasta de logs: {e}")

@register_execucao
@capturar_erros
def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')

    # Definir estilos para widgets com fundo preto e texto branco
    style.configure('TLabel', font=('Helvetica', 12), background='#4682B4', foreground='white')
    style.configure('TButton', font=('Helvetica', 12, 'bold'), background='#228B22', foreground='white')
    style.configure('TEntry', font=('Helvetica', 12), background='black', foreground='black', borderwidth=1)
    style.configure('TScrolledText', font=('Helvetica', 12), background='black', foreground='white', borderwidth=1)
    
    # Configuração adicional para botões
    style.map('TButton',
              background=[('active', '#6B8E23')],
              foreground=[('active', 'black')])

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()
