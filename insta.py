import re
from selenium.webdriver.common.by import By
import time
from arquivos import upload_files_comments, generate_log_block, generate_unique_file_name, separation_line, save_comments, timeout, generate_log_block
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from chromeDriver import start_driver
from decorador import capturar_erros, register_execucao
from ia import get_answer_ia

@capturar_erros
def abrir_instagram():
    driver = start_driver()
    print("Abrindo Instagram...")
    driver.get('https://www.instagram.com')
    time.sleep(5)
    return driver

@capturar_erros
def check_login_insta(driver, url):
    start_time = time.time()
   
    while True:
        timeout(start_time)
        try:
            # Verifica se o campo de login inicial está presente
            login_element = driver.find_element(By.CLASS_NAME, '_aa4a')
            print('Conecte sua conta para continuar...Aguardando...')
            time.sleep(30)
        except NoSuchElementException:
            try:
                # Verifica se o botão "Continuar como" está presente
                login_button = driver.find_element(By.XPATH, "//div[@class='_ap3a _aaco _aacw _aad3 _aada _aade' and contains(text(), 'Continuar como')]")
                print('Conecte sua conta para continuar...Aguardando...')
                time.sleep(30)
            except NoSuchElementException:
                try:
                    # Verifica se a página inicial está presente
                    home_page_element = driver.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft') and contains(text(), 'Página inicial')]")
                    print('Login realizado. Acessando publicação...')
                    driver.get(url)
                    time.sleep(5)  
                    break
                except NoSuchElementException:
                    
                    print('Conecte sua conta para continuar...Aguardando...')
                    time.sleep(30)  
@capturar_erros
def load_list(driver):
    print('Carregando e lendo comentários...')
    while True:
        try:
            container = driver.find_element(By.CLASS_NAME, "x5yr21d.xw2csxc.x1odjw0f.x1n2onr6")
            altura_conteudo = driver.execute_script("return arguments[0].scrollHeight;", container)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", container)
            try:
                ver_comentarios = container.find_element(By.XPATH, "//span[contains(text(), 'Ver comentários ocultos')]")
                if ver_comentarios:
                    print('Encontrado "Ver comentários ocultos", encerrando rolagem.')
                    break  
            except:
                nova_altura_conteudo = driver.execute_script("return arguments[0].scrollHeight;", container)
                if nova_altura_conteudo == altura_conteudo:
                    break
        except Exception as e:
            print(f'Erro: {e}')
            break
    # Rola a página de volta para o início dos comentários
    driver.execute_script("arguments[0].scrollTop = 0;", container)
    time.sleep(1)
    print("Iniciando próxima etapa...")

@capturar_erros
def check_response(container, current_user):
    try:
        response_indicator = container.find_element(
            By.XPATH,
            f".//a[contains(@href, '/{current_user}/')]"
        )
        print(f"Resposta encontrada para o usuário: {current_user}")
        return True
    except NoSuchElementException as e:
        return False
    except Exception as e:
        return False

@register_execucao
@capturar_erros
def capture_comments(driver, url, current_user):
    comentarios = []
    comentarios_file = generate_unique_file_name(url)
    
    comment_containers = driver.find_elements(By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")
    for index, container in enumerate(comment_containers):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", container)
            # Captura os detalhes do comentário
            user_link_element = container.find_element(By.XPATH, ".//a[contains(@class, 'notranslate _a6hd')]")
            user_href = user_link_element.get_attribute("href")
            user_name = user_href.split('/')[-2]  # O nome do usuário está entre as barras "/"
            
            comment_link = container.find_element(By.XPATH, ".//a[contains(@class, 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd')]")
            comment_id = comment_link.get_attribute("href").split("/")[-2]
            
            comment_text = container.find_element(By.XPATH, ".//div[contains(@class, 'x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1')]").text

            try:
                ver_mais = container.find_element(By.XPATH, ".//span[contains(text(), 'Ver todas as')]")
                driver.execute_script("arguments[0].scrollIntoView();", ver_mais)
                ver_mais.click()
                time.sleep(1)
                foi_respondido = check_response(container, current_user)
            except NoSuchElementException:
                foi_respondido = False
                pass  
            
            comentario_data = {
                'comment_id': comment_id,
                'nome': user_name,
                'comentario': comment_text,
                'respondido': foi_respondido,
            }

            if not any(com['comment_id'] == comment_id for com in comentarios):
                comentarios.append(comentario_data)
                print(f"comment_id: {comment_id}")
                print(f"Usuário: {user_name}")
                print(f"Comentário: {comment_text}")
                print(f"Respondido: {foi_respondido}")
                print(separation_line())
                
        except:
    
            continue
    save_comments(comentarios, comentarios_file)
    return comentarios_file

@register_execucao
@capturar_erros
def clean_special_characters(text):
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

@register_execucao
@capturar_erros
def reply_comments(driver, comentarios, comentarios_file, url, prompt_text, personalized_message):
    for comentario in comentarios:
        if comentario['respondido']:
            continue  
        try:
            ia_response = get_answer_ia(driver, comentario['comentario'], prompt_text, personalized_message)
            ia_response = clean_special_characters(ia_response) 
            if generate_log_block(ia_response):
                generate_log_block(url, comentario['comment_id'], comentario['nome'], comentario['comentario'])
                continue
            
            respond_on_instagram(driver, comentario, ia_response)
            comentario['respondido'] = True
            save_comments(comentarios, comentarios_file)
        
        except Exception as e:
            print(f"Erro ao responder comentário {comentario['comment_id']}: {e}")
        
        time.sleep(1)
        
@register_execucao
@capturar_erros
def respond_on_instagram(driver, comentario, ia_response):
    try:
        container = driver.find_element(By.CLASS_NAME, "x5yr21d.xw2csxc.x1odjw0f.x1n2onr6")

        comment_id = comentario['comment_id']
         
        comentario_container = driver.find_elements(By.XPATH, 
            "//div[contains(@class, 'x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1')]")

        
        for container in comentario_container:
            try:
                container_id_elements = container.find_elements(By.XPATH, ".//a[contains(@href, '/c/')]")
                
                if container_id_elements:
                    container_id_element = container_id_elements[0]
                    container_id = container_id_element.get_attribute("href").split('/')[-2]

                    if container_id == comment_id:
                        print('linha 172', container_id, container_id)
                        actions = ActionChains(driver)
                        actions.move_to_element(container).perform()
                        time.sleep(1)
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
                        time.sleep(2)
                        responder_button = container.find_element(By.XPATH, ".//span[contains(@class,'x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft') and contains(text(), 'Responder')]")
                        actions.move_to_element(responder_button).click().perform()
                        time.sleep(1)
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
                        time.sleep(1)
                        actions = ActionChains(driver)
                        for char in ia_response:
                            actions.send_keys(char)
                            actions.perform()
                            time.sleep(0.02)   
                        time.sleep(1)
                        driver.switch_to.active_element.send_keys(Keys.RETURN)
                        time.sleep(2)
                        
                        # Verifica se a mensagem de erro apareceu
                        erro_elementos = driver.find_elements(By.XPATH, "//p[@class='_abmp' and contains(text(), 'Não foi possível publicar o comentário.')]")
                        if erro_elementos:
                            print(separation_line())
                            print("Não foi possível publicar o comentário. Gerando log de bloqueio.")
                            generate_log_block(driver.current_url, comentario['comment_id'], comentario['nome'], comentario['comentario'])
                            time.sleep(2)
                            actions.send_keys(Keys.CONTROL, "a").send_keys(Keys.BACKSPACE).perform()
                        else:
                            print(separation_line())
                            print(f"Comentário respondido")
            
            except Exception as e:
                print(separation_line())
                # print(f"Erro ao tentar responder ao comentário: {e}")
    except Exception as e:
        print(separation_line())
        print(f"Erro ao localizar ou responder ao comentário: {e}")

def filtro(filtro_ativo):
    
    if filtro_ativo == 'Sim':
        return ("Se o comentário for um link, apenas um nome, ou for ofensivo/grosseiro,"
                "responda com esse filtro - 'Esse comentário não pode ser respondido'."
            )
    return ""

@register_execucao
@capturar_erros
def construct_prompt_text(filtro_text):
    """Constrói o prompt_text com base no texto do filtro."""
    base_text = (
        "Este é um comentário do Instagram "
        "apenas responda sem informações a mais!"
    )
    
    prompt_text = (
        base_text +
        filtro_text +
        " Essa é a legenda da publicação ou uma mensagem específica sobre como ou o que responder ao comentário."
    )
    
    return prompt_text

@register_execucao
@capturar_erros
def main(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo): #log_bloqueio_file - remover para rodar somente essa pagina
    driver = abrir_instagram()
    check_login_insta(driver, url)
    load_list(driver)
    comentarios_file = capture_comments(driver, url, current_user)
    comentarios = upload_files_comments(comentarios_file)
    
    filtro_text = filtro(filtro_ativo)
    prompt_text = construct_prompt_text(filtro_text)
    
    reply_comments(driver, comentarios, comentarios_file, url, prompt_text, personalized_message)
    
    print("Processo concluído.")
    # driver.quit()

if __name__ == "__main__":
    url = 'https://www.instagram.com/p/C8pIoYjgDEW/' 
    current_user = "feliperoiko" 
    personalized_message = "RResponda de forma breve, direta e descontraída. "
    log_bloqueio_file = "log_bloqueio.txt"
    filtro_ativo = "Sim"
    
    main(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo) #log_bloqueio_file - remover para rodar somente essa pagina
    