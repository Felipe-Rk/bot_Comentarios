import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from chromeDriver import start_driver
from face import comments, load_all_comments

def localizar_comentario(driver, url, comment_id):
    """
    Função que carrega a página de comentários e localiza o comentário pelo ID fornecido.
    """
    # Verifica se a URL atual já é a página correta
    if driver.current_url != url:
        print("Acessando a publicação:", url)
        driver.get(url)
        time.sleep(5)  # Esperar a página carregar
        comments(driver, 'Todos')
        load_all_comments(driver)  # Certificar-se de que todos os comentários são carregados
    else:
        print("Navegador já está na URL correta. Pulando carregamento da página.")


    # Encontrar todos os comentários e verificar se o comentário com o ID está presente
    comment_containers = driver.find_elements(By.XPATH, "//div[@class='x169t7cy x19f6ikt']")
    for container in comment_containers:
        links = container.find_elements(By.XPATH, ".//a[contains(@href, 'comment_id=')]")
        for link in links:
            href_full = link.get_attribute("href")
            if "comment_id=" in href_full:
                comment_id_found = href_full.split("comment_id=")[-1].split("&")[0]
                if comment_id == comment_id_found:
                    print(f"Comentário com ID {comment_id} encontrado e destacado.")
                    # Scroll para o comentário encontrado e destacá-lo
                    driver.execute_script("arguments[0].scrollIntoView();", container)
                    time.sleep(5)  # Pausa para que você possa ver o comentário destacado
                    return
    
    print(f"Comentário com ID {comment_id} não encontrado.")


def main(url, comment_id, log_text, driver):
    """
    Função principal para ser chamada pelo functionsITF.py
    """
    driver = start_driver()  # Inicializar o driver
    localizar_comentario(driver, url, comment_id)  # Localizar o comentário
    print("Navegador mantido aberto. Feche manualmente quando terminar.")
    # time.sleep(10000)
