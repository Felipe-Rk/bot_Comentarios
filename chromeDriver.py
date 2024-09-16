import os
from selenium import webdriver
from arquivos import separation_line
from decorador import capturar_erros, register_execucao

@register_execucao
@capturar_erros
def start_driver():
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
    return driver