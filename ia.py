import time
from arquivos import separation_line, timeout
from selenium.webdriver.common.by import By

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
                return document.querySelector("#b_sydConvCont > cib-serp").shadowRoot
                    .querySelector("#cib-conversation-main").shadowRoot
                    .querySelector("#cib-chat-main > cib-welcome-container").shadowRoot
                    .querySelector("div.muid-upsell > div");
            """)

            if element:
                print("Faça Login para continuar a execução...")
                time.sleep(20)
                continue
            else:
                app_element = driver.execute_script("""
                    return document.querySelector("#copilot_app_cta > span");
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
    time.sleep(4)
    
    # Verifica se o login já foi realizado
    if not login_verificado:
        check_login(driver, IA)
        login_verificado = True 

    if not personalized_message:
        personalized_message = "Responda de forma breve, direta e descontraída." 
        prompt_text = (
            f"{prompt_text}"  
            f" message: {personalized_message} . Comentario: {comment_text}."
        )
    
    else:
        prompt_text = ( 
            f"{prompt_text}"
            f"message:{personalized_message} .Comentario: {comment_text}"
        )

    # Remove caracteres fora do BMP
    prompt_text = remove_characters_outside_of_bmp(prompt_text)

    driver.switch_to.active_element.send_keys(prompt_text)
    send_button = driver.execute_script("""
        return document.querySelector("#b_sydConvCont > cib-serp").shadowRoot
                    .querySelector("#cib-action-bar-main").shadowRoot
                    .querySelector("div > div.main-container > div > div.bottom-controls > div > div.bottom-right-controls > div.control.submit > button");
    """)
    send_button.click()
    time.sleep(7)
    response_container = driver.execute_script("""
        try {
            return document.querySelector("#b_sydConvCont > cib-serp").shadowRoot
                        .querySelector("#cib-conversation-main").shadowRoot
                        .querySelector("#cib-chat-main > cib-chat-turn").shadowRoot
                        .querySelector("cib-message-group.response-message-group").shadowRoot
                        .querySelector("cib-message").shadowRoot
                        .querySelector("cib-shared > div")
                        .querySelector(".ac-textBlock > p").innerText;
        } catch (e) {
            return null;
        }
    """)
    if not response_container:
        response_container = driver.execute_script("""
            try {
                return document.querySelector("#b_sydConvCont > cib-serp").shadowRoot
                            .querySelector("#cib-conversation-main").shadowRoot
                            .querySelector("#cib-chat-main > cib-chat-turn").shadowRoot
                            .querySelector("cib-message-group.response-message-group").shadowRoot
                            .querySelector("cib-message[attributions]").shadowRoot
                            .querySelector("cib-shared > div").innerText;
            } catch (e) {
                return "Texto não encontrado em ambas as formas";
            }
        """)
    if not response_container or response_container == "Texto não encontrado em ambas as formas":
        response_container = driver.execute_script("""
            try {
                let message = document.evaluate(
                    '//*[@id="cib-chat-main"]/cib-chat-turn//cib-message-group[2]', 
                    document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                
                if (message) {
                    return message.shadowRoot
                                .querySelector("cib-message").shadowRoot
                                .querySelector("cib-shared > div").innerText;
                } else {
                    return "Texto não encontrado usando XPath";
                }
            } catch (e) {
                return "Texto não encontrado em todas as tentativas";
            }
        """)
    if not response_container or response_container.startswith("Texto não encontrado"):
        response_container = driver.execute_script("""
            try {
                let message = document.querySelector("#b_sydConvCont > cib-serp").shadowRoot
                            .querySelector("#cib-conversation-main").shadowRoot
                            .querySelector("#cib-chat-main > cib-chat-turn").shadowRoot
                            .querySelector("cib-message-group.response-message-group").shadowRoot
                            .querySelector("cib-message").shadowRoot
                            .querySelector("cib-shared > div").innerHTML;
        """)
    ia_response = response_container
    print(separation_line())
    print(f"Resposta da IA: {ia_response}")
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return ia_response
