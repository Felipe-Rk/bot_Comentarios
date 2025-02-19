import re
import time
from arquivos import separation_line, timeout
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from decorador import capturar_erros, register_execucao


login_verificado = False

@register_execucao
@capturar_erros
def remove_characters_outside_of_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

@capturar_erros
def check_login(driver, IA):   
    start_time = time.time()

    while True:
        timeout(start_time)
        try:
            element = driver.execute_script("""
                return document.querySelector("button[title='Entrar']");
            """)

            if element:
                print("Faça Login para continuar a execução...")
                time.sleep(20)
                continue
            else:
                app_element = driver.execute_script("""
                    return document.querySelector("textarea#userInput[placeholder='Mensagem para o Copilot']");
                """)

                if app_element:
                    print('Login realizado...Executando...')
                    login_verificado = True
                    time.sleep(2)
                    break       
        except Exception as e:
            continue 
        
@register_execucao
@capturar_erros      
def get_answer_ia(driver, comment_text,prompt_text, personalized_message=None):
    
    global login_verificado
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    IA = 'https://copilot.microsoft.com/?showconv=1'
    driver.get(IA)
    time.sleep(5)
    
    # Verifica se o login já foi realizado
    if not login_verificado:
        check_login(driver, IA)
        login_verificado = True 

    if not personalized_message:
        personalized_message = "Responda de forma breve, direta e descontraída e não fique respondendo com a mesma mensagem sempre e não responda com nomes." 
        prompt_text = (
            f"{prompt_text}"  
            f"Não fique respondendo com a mesma mensagem sempre e não responda com nomes! Mensagens: {personalized_message} . Comentario: {comment_text}."
        )
    
    else:
        prompt_text = ( 
            f"{prompt_text}"
            f"Não fique respondendo com a mesma mensagem sempre e não responda com nomes! Mensagens:{personalized_message} .Comentario: {comment_text}"
        )

    # Remove caracteres fora do BMP
    prompt_text = remove_characters_outside_of_bmp(prompt_text)

    for char in prompt_text:
            driver.switch_to.active_element.send_keys(char)
            time.sleep(0.01)
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(5)
    response_container = driver.execute_script(""" 
        try {
            return document.querySelector("#app > main > div.h-dvh > div > div > div.min-h-[calc(100dvh-60px-var(--composer-container-height))].sm\\:min-h-[calc(100dvh-120px-var(--composer-container-height))] > div > div:nth-child(2)").innerText;
        } catch (e) {
            return null;
        }
    """)
    if not response_container:
        response_container = driver.execute_script(""" 
            try {
                let message = document.evaluate(
                    '//*[@id="app"]/main/div[3]/div/div/div[2]/div/div[2]', 
                    document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                
                if (message) {
                    return message.innerText;
                } else {
                    return "Esse comentário não pode ser respondido";
                }
            } catch (e) {
                return "Esse comentário não pode ser respondido";
            }
        """)
        
    if not response_container or response_container.startswith("Texto não encontrado"):
        response_container = driver.execute_script(""" 
            try {
                let message = document.querySelector("#app > main > div.h-dvh > div > div > div.min-h-[calc(100dvh-60px-var(--composer-container-height))].sm\\:min-h-[calc(100dvh-120px-var(--composer-container-height))] > div > div:nth-child(2)").innerHTML;
                return message;
            } catch (e) {
                return "Esse comentário não pode ser respondido";
            }
        """)
    time.sleep(5)
    if response_container:
        # Remove a parte relacionada ao "Copilot" ou outras palavras indesejadas
        response_container = re.sub(r'(?i)copilot.*?$', '', response_container).strip()

        # Extrai o conteúdo dentro das aspas, se presente
        match = re.search(r'"(.*?)"', response_container)
        if match:
            ia_response = match.group(1)
        else:
            ia_response = response_container
    ia_response = ia_response
    print(separation_line())
    print(f"Resposta da IA: {ia_response}")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return ia_response
