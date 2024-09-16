import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from arquivos import upload_files_comments, generate_log_block, generate_unique_file_name, separation_line, save_comments, timeout, generate_log_block
from chromeDriver import start_driver
from decorador import capturar_erros, register_execucao
from ia import get_answer_ia

@register_execucao
@capturar_erros
def open_url(driver):
    print(separation_line())
    print('Abrindo Facebook')
    driver.get('https://www.facebook.com/')
    time.sleep(5) 


@register_execucao
@capturar_erros
def verify_login_face(driver, url):
    start_time = time.time()
    
    while True:
        start_time = time.time()
        try:
            timeout(start_time)
            login_element = driver.find_element(By.CLASS_NAME, "x1n2onr6.x1ja2u2z.x1afcbsf.x78zum5.xdt5ytf.x1a2a7pz.x6ikm8r.x10wlt62.x71s49j.x1jx94hy.x1qpq9i9.xdney7k.xu5ydu1.xt3gfkd.x104qc98.x1g2kw80.x16n5opg.xl7ujzl.xhkep3z.x193iq5w")
            print(separation_line())
            print("Faça o login para continuar...")
            time.sleep(20)
        except NoSuchElementException:
                try:
                    print(separation_line())
                    home_page_element = driver.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84') and contains(text(), 'Criar story')]")
                    print('Login realizado. Acessando publicação...')
                    driver.get(url)
                    time.sleep(5)
                    break
                except NoSuchElementException:
                    print(separation_line())
                    print('Aguardando login...')
                    time.sleep(20) 

@register_execucao
@capturar_erros
def load_all_comments(driver):
    print(separation_line())
    print("Carregando todos os comentários...")

    while True:
        try:
            # Primeiro, tenta encontrar pelo texto "Ver mais comentários"
            ver_mais_comentarios = driver.find_element(By.XPATH, "//span[contains(text(), 'Ver mais comentários')]")
        except Exception as e:
            # print(f"Erro ao encontrar o botão pelo texto: {e}")
            try:
                # Se não encontrar pelo texto, encontra o container dos comentários
                container_comentarios = driver.find_element(By.CLASS_NAME, 'x78zum5.xdt5ytf.x1iyjqo2.xs83m0k.x2lwn1j.x1odjw0f.x1n2onr6.x9ek82g.x6ikm8r.xdj266r.x11i5rnm.x4ii5y1.x1mh8g0r.xexx8yu.x1pi30zi.x18d9i69.x1swvt13')
                # Em seguida, tenta encontrar o botão pelo CSS class
                elementos = container_comentarios.find_elements(By.CLASS_NAME, 'x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xdj266r.xat24cr.x1n2onr6.x1plvlek .xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.xl56j7k')
                ver_mais_comentarios = None
                for elemento in elementos:
                    if elemento.text == 'Ver mais comentários':
                        ver_mais_comentarios = elemento
                        break
            except Exception as e:
                # print(f"Erro ao encontrar o botão pelo CSS class: {e}")
                break

        if ver_mais_comentarios:
            try:
                driver.execute_script("arguments[0].click();", ver_mais_comentarios)
                
            except Exception as e:
                print(f"Erro ao clicar no botão: {e}")
                break
        else:
            break

@register_execucao
@capturar_erros
def capture_comments(driver, url, current_user):
    # coments(driver, coments_all)
    load_all_comments(driver)
    comment_containers = driver.find_elements(By.XPATH, "//div[@class='x169t7cy x19f6ikt']")
    if not comment_containers:
        print("Nenhum comentário encontrado. Verifique o XPath.")
        return

    comentarios = []
    comentarios_file = generate_unique_file_name(url)
    
    for index, container in enumerate(comment_containers):
        print(f"Lendo comentário {index + 1} de {len(comment_containers)}...")
        try:
            placeholder = container.find_element(By.XPATH, ".//div[@aria-placeholder]")
            if placeholder:
                print("Nenhum comentário adicional encontrado. Parando o processamento.")
                break
        except Exception:
            pass 

        try:
            ver_mais = container.find_element(By.XPATH, ".//div[contains(text(), 'Ver mais') and @role='button']")
            driver.execute_script("arguments[0].scrollIntoView();", ver_mais)
            ver_mais.click()
            time.sleep(1)
        except Exception:
            pass

        user_name = container.find_element(By.XPATH, ".//a[contains(@class, 'x1i10hfl')]/span").text
        # comment_link = container.find_element(By.XPATH, ".//a[contains(@class, 'x1i10hfl')]")
        # comment_id = comment_link.get_attribute("href").split("comment_id=")[-1].split("&")[0]

        # # Verifique se o ID extraído é válido (contém apenas números e tem 15+ dígitos)
        # if not re.match(r'^\d{15,}$', comment_id):
        #     # Se não for válido, use o fallback para extrair com regex
        #     href_full = comment_link.get_attribute("href")
        #     match = re.search(r'\d{15,}', href_full)
        #     if match:
        #         comment_id = match.group(0)
        #     else:
        #         comment_id = "comment_id não encontrado"
        
        comment_id = "comment_id não encontrado"
        links = container.find_elements(By.XPATH, ".//a[contains(@href, 'comment_id=')]")
        
        for link in links:
            href_full = link.get_attribute("href")
            if "comment_id=" in href_full:
                comment_id = href_full.split("comment_id=")[-1].split("&")[0]
                break
        try:
            comment_text = container.find_element(By.XPATH, ".//div[contains(@class, 'x1lliihq')]/span/div").text
        except Exception:
            comment_text = None

        if comment_text is None:
            print("Comentário contém uma imagem ou outro elemento não textual.")
            generate_log_block(url, comment_id, user_name, "Comentário não textual (imagem ou avatar).")
            continue
        
        foi_respondido = check_response(container, current_user)
        comentarios.append({
            'comment_id': comment_id,
            'nome': user_name,
            'comentario': comment_text,
            'respondido': foi_respondido
        })
        print(f"Usuário: {user_name}")
        print(f"Comentário: {comment_text}")
        print(separation_line())
    save_comments(comentarios, comentarios_file)
    return comentarios_file

@register_execucao
@capturar_erros
def check_response(container, current_user):
    try:
        response_indicator = container.find_element(
            By.XPATH,
            f".//*[contains(text(), '{current_user} respondeu')]"
        )
        print(f"{response_indicator.text}")
        return True
    except:
        print("Comentário não respondido.")
        return False

@register_execucao
@capturar_erros
def reply_comments(driver, comentarios, comentarios_file, url, prompt_text, personalized_message):
    for comentario in comentarios:
        if comentario['respondido']:
            continue
        ia_response = get_answer_ia(driver, comentario['comentario'], prompt_text, personalized_message)
        if generate_log_block(ia_response):
            generate_log_block(url, comentario['comment_id'], comentario['nome'], comentario['comentario'])
            continue
        reply_on_facebook(driver, comentario, ia_response)
        comentario['respondido'] = True
        save_comments(comentarios, comentarios_file)
        time.sleep(1)

@register_execucao
@capturar_erros
def reply_on_facebook(driver, comentario, ia_response):
    try:
        comentario_container = driver.find_element(By.XPATH, f"//div[@class='x169t7cy x19f6ikt' and descendant::a[contains(@href, 'comment_id={comentario['comment_id']}')]]")
        actions = ActionChains(driver)
        print(f'linha 195 {comentario_container}')
        actions.move_to_element(comentario_container).perform()
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comentario_container)
        time.sleep(1)
        responder_button = comentario_container.find_element(By.XPATH, ".//div[@role='button' and @tabindex='0' and contains(text(), 'Responder')]")
        actions.move_to_element(responder_button).click().perform()
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comentario_container)
        time.sleep(1)
        actions = ActionChains(driver)
        for char in ia_response:
            actions.send_keys(char)
            actions.perform()
            time.sleep(0.02)   
        time.sleep(1)
        driver.switch_to.active_element.send_keys(Keys.RETURN)
        print(separation_line())
        print(f"Comentário respondido")
        time.sleep(1)
    except Exception as e:
        print(separation_line())
        raise  # Re-raise the exception to allow the decorator to handle it


@capturar_erros
def filtro(filtro_ativo):
    
    if filtro_ativo == 'Sim':
        return ("Se o comentário for um link, apenas um nome, ou for ofensivo/grosseiro,"
                "responda com esse filtro - 'Esse comentário não pode ser respondido'."
            )
    return ""

@capturar_erros
def comments(driver, coments_all):
    actions = ActionChains(driver)
    if coments_all == "Todos":
        print("Capturar Todos os comentários")
        comment_containers = driver.find_elements(By.XPATH, "//div[@class='html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x18d9i69 x1swvt13 x1pi30zi']")
        if comment_containers:
            viewer_full = driver.find_element(By.XPATH, "//span[normalize-space(text())='Mais relevantes']")
            actions.move_to_element(viewer_full).click().perform()
            time.sleep(1)
            full_containers = driver.find_elements(By.XPATH,"//div[@class='x4k7w5x x1h91t0o x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1n2onr6 x1qrby5j x1jfb8zj'] ")
            if full_containers:   
                viewer_full_coments = driver.find_element(By.XPATH, "//span[normalize-space(text())='Todos os comentários']")
                viewer_full_coments.click()
                time.sleep(1)
                return
        
    if coments_all == "Relevantes":
        print('Capturar comentários relevantes')
        return

   


@capturar_erros
def construct_prompt_text(filtro_text):
    """Constrói o prompt_text com base no texto do filtro."""
    base_text = (
        "Este é um comentário do facebook "
        "apenas responda sem informações a mais!"
    )
    
    prompt_text = (
        base_text +
        filtro_text +
        " Essa é a legenda da publicação ou uma message específica sobre como ou o que responder ao comentário."
    )
    
    return prompt_text
  
@register_execucao
@capturar_erros       
def main(url, current_user,log_bloqueio_file, personalized_message,filtro_ativo, coments_all): #log_bloqueio_file - remover para rodar somente essa pagina
    driver = start_driver()
    open_url(driver)
    verify_login_face(driver, url)
    comments(driver, coments_all)
    load_all_comments(driver)
    comentarios_file = capture_comments(driver, url, current_user)
    comentarios = upload_files_comments(comentarios_file)
    
    filtro_text = filtro(filtro_ativo)
    prompt_text = construct_prompt_text(filtro_text)
    
    reply_comments(driver, comentarios, comentarios_file, url, prompt_text, personalized_message)
    # driver.quit()

if __name__ == "__main__":
    url = 'https://www.facebook.com/photo/?fbid=914229407399311&set=a.547401260748796'
    current_user = "Felipe Roiko"
    personalized_message = "Responda de forma breve, direta e descontraída." 
    log_bloqueio_file = "log_bloqueio.txt" 
    filtro_ativo = "Não"
    coments_all = "Relevantes"
    main(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo, coments_all) #log_bloqueio_file - remover para rodar somente essa pagina

