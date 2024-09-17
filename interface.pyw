import tkinter as tk
from tkinter import ttk, scrolledtext
from ttkthemes import ThemedTk
from decorador import capturar_erros, register_execucao
from functionsITF import Tooltip, apply_styles, executar_script, abrir_log

@register_execucao
@capturar_erros
def main():
    windows = ThemedTk(theme="radiance")
    windows.title("Automatização de Respostas")
    windows.geometry("690x670")
    windows.configure(bg='#4682B4')
    windows.resizable(True, True)
    windows.iconbitmap("ico\\interface.ico")
    
    apply_styles()

    # Configuração de peso nas linhas e colunas da windows principal
    windows.grid_columnconfigure(0, weight=1)
    windows.grid_rowconfigure(1, weight=1)

    # Título centralizado
    title_label = ttk.Label(windows, text="Automatização de Respostas", font=("Helvetica", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=20)

    # Container principal para organizar os widgets
    container = ttk.Frame(windows, padding="10 10 10 10")
    container.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

    # Configuração de peso nas colunas e linhas do container para redimensionamento
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=3)
    container.grid_rowconfigure(4, weight=1)  # A linha com o log será expansível

    # Ícone de ajuda na parte superior da windows
    help_label = ttk.Label(container, text="?", foreground="white", cursor="hand2", font=("Helvetica", 16, "bold"))
    help_label.grid(row=0, column=2, pady=10, padx=10, sticky='ne')
    Tooltip(help_label,
        "INFORMAÇÕES DE FUNCIONAMENTO\n"
        "                                                             \n"
        "AVISO - A PRIMEIRA VEZ PRECISA LOGAR NO FACEBOOK/INSTAGRAM E IA PARA CONTINUAR A EXECUÇÃO!!!!\n"
        "                                                             \n"
        "O PROGRAMA DEVE SER EXECUTADO COMO ADMINISTRADOR"
        
        "                                                             \n"
        "LINK - Cole a URL que você quer que seja comentado. Facebook ou Instagram.\n"
        "                                                             \n"
        "NOME DE USUÁRIO - É seu nome ou do Facebook/Instagram que irá responder, para não "
        "ficar respostas duplicadas.\n"
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
        "Por padrão o código vem com reposta para comentário relevantes \n"
        "Caso deseje alterar, selecione 'Todos' no comentários."
    )

    # Widgets da interface
    label_url = ttk.Label(container, text="Link:")
    label_url.grid(row=1, column=0, pady=10, padx=10, sticky='w')

    entry_url = ttk.Entry(container, width=50)
    entry_url.grid(row=1, column=1, pady=10, padx=10, sticky='ew')

    label_usuario = ttk.Label(container, text="Nome do Usuário:")
    label_usuario.grid(row=2, column=0, pady=10, padx=10, sticky='w')

    entry_usuario = ttk.Entry(container, width=50)
    entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky='ew')

    label_message = ttk.Label(container, text="message personalizada:")
    label_message.grid(row=3, column=0, pady=10, padx=10, sticky='w')

    entry_message = ttk.Entry(container, width=50)
    entry_message.grid(row=3, column=1, pady=10, padx=10, sticky='ew')

    # Área de log centralizada
    log_text = scrolledtext.ScrolledText(container, wrap=tk.WORD, height=15, width=80, bg='#1C1C1C', fg='white', font=('Helvetica', 12))
    log_text.grid(row=4, column=0, columnspan=3, pady=20, padx=10, sticky='nsew')

    # Botões estilizados
    btn_executar = ttk.Button(container, text="Executar", command=lambda: executar_script(entry_url.get(), entry_usuario.get(), entry_message.get(), log_text, filtro_var.get(), comentarios_var.get()))
    btn_executar.grid(row=5, column=0, columnspan=3, pady=10)

    btn_baixar_log = ttk.Button(container, text="Abrir Pasta de Logs", command=abrir_log)
    btn_baixar_log.grid(row=6, column=0, columnspan=3, pady=10)

    label_filtro = ttk.Label(container, text="Filtro de Resposta:", background='#2C3E50', foreground='white', font=("Helvetica", 12))
    label_filtro.grid(row=5, column=1, pady=10, padx=(10, 5), sticky='e')

    filtro_var = tk.StringVar(value="Sim")  # Valor padrão "Sim"
    select_filtro = ttk.Combobox(container, textvariable=filtro_var, values=["Sim", "Não"], state="readonly", width=10, font=("Helvetica", 12))
    select_filtro.grid(row=5, column=2, pady=10, padx=(5, 10), sticky='w')

    # Campo de seleção para comentários
    label_comentarios = ttk.Label(container, text="Comentários:", background='#2C3E50', foreground='white', font=("Helvetica", 12))
    label_comentarios.grid(row=6, column=1, pady=10, padx=(10, 5), sticky='e')

    comentarios_var = tk.StringVar(value="Relevantes")  # Valor padrão "Relevantes"
    select_comentarios = ttk.Combobox(container, textvariable=comentarios_var, values=["Relevantes", "Todos"], state="readonly", width=10, font=("Helvetica", 12))
    select_comentarios.grid(row=6, column=2, pady=10, padx=(5, 10), sticky='w')

    # Rodapé
    label_rodape = ttk.Label(windows, text="Desenvolvedor: Felipe Roiko", font=("Times New Roman", 20, "italic"))
    label_rodape.grid(row=7, column=0, columnspan=3, pady=20)

    windows.mainloop()

if __name__ == "__main__":
    main()
