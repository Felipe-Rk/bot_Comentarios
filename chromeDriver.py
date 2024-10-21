import os
import threading
import sys
import io
import time
from tkinter import ttk
import tkinter as tk
from arquivos import save_log_block_comments, separation_line
from decorador import capturar_erros, register_execucao
from selenium import webdriver

# Variável global para armazenar a instância do driver
driver = None
# Flags para rastrear se as funções principais já foram executadas
pagina_aberta = False
comentarios_carregados = False

@register_execucao
@capturar_erros
def start_driver():
    global driver  # Referência à variável global

    if driver is None:  # Verifica se o driver não foi iniciado ainda
        user_name = os.getlogin()  # Identifica o nome do usuário do computador automaticamente
        chrome_profile_path = fr'C:\Users\{user_name}\AppData\Local\Google\Chrome\User Data\Default'  # Usa o perfil 'Default'
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
        chrome_options.add_argument("--profile-directory=Default")  # Abre o perfil padrão
        
        # Opcional: Para evitar problemas com a abertura em múltiplas instâncias
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        
        print(separation_line())
        print('Iniciando sistema...')
    else:
        print("Usando a instância existente do driver.")
    
    return driver

def reset_flags():
    global pagina_aberta, comentarios_carregados
    pagina_aberta = False
    comentarios_carregados = False