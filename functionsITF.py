import os
import threading
import sys
import io
from tkinter import ttk
import tkinter as tk
from arquivos import save_log_block_comments
from decorador import capturar_erros, register_execucao

# Variável global para armazenar o nome do arquivo de log
log_bloqueio_file = None

@register_execucao
@capturar_erros
class SilenciarErros(io.StringIO):
    """Classe para silenciar qualquer mensagem enviada ao terminal."""
    def write(self, message):
        pass  # Ignora qualquer mensagem enviada

@register_execucao
@capturar_erros
class RedirectText(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def write(self, message):
        self.text_widget.insert("end", message)
        self.text_widget.yview("end")

def identificar_e_executar_script(url, current_user, personalized_message, log_text, filtro_ativo, coments_all):
    global log_bloqueio_file
    
    # essa função deve ser ativa para limitar a execução
    # comentario = "369745_s1d9_@egt%"
    # total_comments = 2
    # save_log_block_comments(comentario, total_comments)
    log_bloqueio_file = os.path.join('logs', f'bloqueio_{current_user}.txt')

        # Redireciona stdout e stderr para silenciar as mensagens
    sys.stdout = RedirectText(log_text)
    sys.stderr = SilenciarErros()  # Silenciar erros no terminal
    
    sys.stdout = RedirectText(log_text)
    sys.stderr = RedirectText(log_text)

    try:
        if "facebook.com" in url:
            from face import main as main_facebook
            main_facebook(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo,coments_all)
        elif "instagram.com" in url:
            from insta import main as main_instagram
            main_instagram(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo)
        else:
            print("URL não reconhecida. Por favor, insira uma URL válida do Facebook ou Instagram.")
    except Exception as e:
        print(f"Erro: {e}")

@register_execucao
@capturar_erros
def executar_script_thread(url, current_user, personalized_message, log_text, filtro_ativo, coments_all):
    threading.Thread(target=identificar_e_executar_script, args=(url, current_user, personalized_message, log_text, filtro_ativo, coments_all), daemon=True).start()

@register_execucao
@capturar_erros
def executar_script(url, current_user, personalized_message, log_text, filtro_ativo, coments_all):
    executar_script_thread(url, current_user, personalized_message, log_text, filtro_ativo, coments_all)

@register_execucao
@capturar_erros
def abrir_log():
    try:
        logs_directory = os.path.join(os.getcwd(), 'logs')
        
        if os.path.exists(logs_directory):
            if os.name == 'nt':  # Windows
                os.startfile(logs_directory)
            elif os.name == 'posix':  # macOS ou Linux
                os.system(f'open "{logs_directory}"')  # Para macOS
                # os.system(f'xdg-open "{logs_directory}"')  # Para Linux
            print(f"Pasta de logs aberta: {logs_directory}")
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



    
# chave = "minha_chave"
# limite_execucoes = 2
# executar_com_limite(chave, limite_execucoes)