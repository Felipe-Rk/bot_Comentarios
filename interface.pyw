import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox  
from ttkthemes import ThemedTk
from arquivos import create_stop_signal
from decorador import capturar_erros, register_execucao
from functionsITF import Tooltip, apply_styles, executar_script, abrir_log,RedirectText

@register_execucao
@capturar_erros
def main():
    windows = ThemedTk(theme="radiance")
    windows.title("Gegenciador de comentários")
    windows.geometry("900x670")  # Aumentar a largura da janela
    windows.configure(bg='#4682B4')
    windows.resizable(True, True)

     # Exibe o pop-up de saudação e bloqueia a interação até que o usuário clique em "OK"
    messagebox.showinfo("Bem-vindo", "Bem-vindo ao Gerenciador de Comentários!Passe o mouse sobre o '?' para verificar como funciona.\n"
                         "Pressione OK para continuar.")

    apply_styles()

    # Configuração de peso nas linhas e colunas da janela principal
    windows.grid_columnconfigure(0, weight=1)
    windows.grid_columnconfigure(1, weight=2)  # Adicionando peso à segunda coluna
    windows.grid_rowconfigure(1, weight=1)

    # Título centralizado
    title_label = ttk.Label(windows, text="Gerenciador de comentários", font=("Helvetica", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=20)  # Título centralizado

    # Container principal para organizar os widgets
    container = ttk.Frame(windows, padding="10 10 10 10")
    container.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    # Configuração de peso nas colunas e linhas do container
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # Ícone de ajuda na parte superior da janela
    help_label = ttk.Label(container, text="?", foreground="white", cursor="hand2", font=("Helvetica", 16, "bold"))
    help_label.grid(row=0, column=2, pady=10, padx=10, sticky='ne')

        # Ícone de ajuda na parte superior da windows
    help_label = ttk.Label(container, text="?", foreground="white", cursor="hand2", font=("Helvetica", 16, "bold"))
    help_label.grid(row=0, column=2, pady=10, padx=10, sticky='ne')
    Tooltip(help_label,
        "INFORMAÇÕES DE FUNCIONAMENTO\n"
        "                                                             \n"
        "AVISO - A PRIMEIRA VEZ PRECISA LOGAR NO FACEBOOK/INSTAGRAM E IA PARA CONTINUAR A EXECUÇÃO!!!!\n"
        "                                                             \n"
        "O programa não precisa ser fechado para utilizar outras funções\n"
        "                                                             \n"

        "LINK - Cole a URL que você quer que seja comentado. Facebook ou Instagram.\n"
        "                                                             \n"
        "NOME DE USUÁRIO - É seu nome ou do Facebook/Instagram que irá responder, para não "
        "ficar respostas duplicadas.\n"
        "                                                             \n"
        "FUNÇÂO - RESPONDER | EXTRAIR | LOCALIZAR \n"
        "                                                             \n"
         "RESPONDER - Função principal, ele carrega, verifica comentarios respondidos ou não \n"
        "extrai todos os comentários para arquivos especificos e responde utilizando IA\n"
        "*FICA EM LOOP VERIFICANDO A PUBLICAÇÃO A CADA 5M PARA NOVOS COMENTÁRIOS, APERTAR EM PARAR PARA FINALIZAR\n"
        "                                                             \n"  
          "EXTRAIR - Carrega a página com todos comentários e gera os arquivos e abre logo em seguida para verificação.\n"
        "Dentro do arquivo possui os campos referente ao comentario e o ID, que será utilizado no localizador\n"
        "                                                             \n"  
          "LOCALIZAR - Usado para localizar comentários não respondidos por meio do arquivo gerado com os IDs.\n"
        "copiar o ID referente ao comentário não respondido e executar para localizar, ele será o primeiro aparecendo\n"
        "                                                             \n"
        "MENSAGEM PERSONALIZADA - Seja muito objetivo no que você quer. "
        "Esta mensagem vai definir como responder a cada comentário.\n"
        "                                                             \n"
        "MENSAGEM PADRÃO - Caso não seja preenchido, este é um comentário padrão.\n"
        "Responda de forma breve, direta e descontraída.\n"
        "                                                             \n"
        "Por padrão o código vem com filtro para comentário ofensivo/grosseiro \n"
        "Caso deseje remover,selecione 'Não' nos filtros de respostas."
        "                                                             \n"
        "Comentários que possuem somente video, emoji ou imagens não são respondidos! \n"

    )
    # Widgets da interface (à esquerda)
    label_url = ttk.Label(container, text="Link:")
    label_url.grid(row=1, column=0, pady=10, padx=10, sticky='w')

    entry_url = ttk.Entry(container, width=50)
    entry_url.grid(row=1, column=1, pady=10, padx=10, sticky='ew')

    label_usuario = ttk.Label(container, text="Nome do Usuário:")
    label_usuario.grid(row=2, column=0, pady=10, padx=10, sticky='w')

    entry_usuario = ttk.Entry(container, width=50)
    entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky='ew')

    label_funcao = ttk.Label(container, text="Função:")
    label_funcao.grid(row=3, column=0, pady=10, padx=10, sticky='w')

    funcao_var = tk.StringVar(value="Extrair")
    select_funcao = ttk.Combobox(container, textvariable=funcao_var, values=["Localizar", "Responder", "Extrair"], state="readonly", width=20)
    select_funcao.grid(row=3, column=1, pady=10, padx=10, sticky='w')

    label_id_comentario = ttk.Label(container, text="ID do Comentário:")
    label_id_comentario.grid(row=4, column=0, pady=10, padx=10, sticky='w')

    entry_id_comentario = ttk.Entry(container, width=50)
    entry_id_comentario.grid(row=4, column=1, pady=10, padx=10, sticky='ew')

    label_message = ttk.Label(container, text="Mensagem personalizada:")
    label_message.grid(row=5, column=0, pady=10, padx=10, sticky='w')

    entry_message = ttk.Entry(container, width=50)
    entry_message.grid(row=5, column=1, pady=10, padx=10, sticky='ew')

    label_filtro = ttk.Label(container, text="Filtro de Resposta:", background='#2C3E50', foreground='white', font=("Helvetica", 12))
    label_filtro.grid(row=6, column=0, pady=10, padx=10, sticky='w')

    filtro_var = tk.StringVar(value="Sim")
    select_filtro = ttk.Combobox(container, textvariable=filtro_var, values=["Sim", "Não"], state="readonly", width=10, font=("Helvetica", 12))
    select_filtro.grid(row=6, column=1, pady=10, padx=10, sticky='w')

    # Campo de log à direita
    log_text = scrolledtext.ScrolledText(windows, wrap=tk.WORD, height=20, width=60, bg='#1C1C1C', fg='white', font=('Helvetica', 12))
    log_text.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
    
    # Redirecionar a saída padrão e de erro para o widget log_text
    sys.stdout = RedirectText(log_text)  
    sys.stderr = RedirectText(log_text)  

    # Botões estilizados (abaixo das opções de escrita)
    btn_executar = ttk.Button(container, text="Executar", command=lambda: executar_script(entry_url.get(), entry_usuario.get(), funcao_var.get(), entry_id_comentario.get(), entry_message.get(), filtro_var.get(), log_text))
    btn_executar.grid(row=9, column=0, columnspan=2, pady=10)

    stop_button = ttk.Button(container, text="Parar", command=create_stop_signal, state="disabled")
    stop_button.grid(row=10, column=0, columnspan=2, pady=10) 

    btn_baixar_log = ttk.Button(container, text="Abrir Pasta de Logs", command=abrir_log)
    btn_baixar_log.grid(row=11, column=0, columnspan=2, pady=10)

    label_rodape = ttk.Label(windows, text="Desenvolvedor: Felipe Roiko", font=("Times New Roman", 20, "italic"))
    label_rodape.grid(row=12, column=0, columnspan=2, pady=20)

    def update_fields(*args):
        funcao = funcao_var.get()
        if funcao == "Localizar":
            entry_id_comentario.config(state="normal")
            entry_message.config(state="disabled")
            select_filtro.config(state="disabled")
            stop_button.config(state="disabled")
        elif funcao == "Responder":
            entry_id_comentario.config(state="disabled")
            entry_message.config(state="normal")
            select_filtro.config(state="normal")
            stop_button.config(state="normal") 
        elif funcao == "Extrair":
            entry_id_comentario.config(state="disabled")
            entry_message.config(state="disabled")
            select_filtro.config(state="disabled")
            stop_button.config(state="disabled")

    funcao_var.trace("w", update_fields)
    update_fields()

    windows.mainloop()

if __name__ == "__main__":
    main()
