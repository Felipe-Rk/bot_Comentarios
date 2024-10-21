import re
from telnetlib import EC
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from arquivos import check_response_block, check_stop_signal, save_comments_excel, save_comments_txt, upload_files_comments, generate_log_block, generate_log_other_content, generate_unique_file_name, separation_line, save_comments, timeout, generate_log_block
from chromeDriver import start_driver
from decorador import capturar_erros, register_execucao
from ia import get_answer_ia

coments_all = "Todos"

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
                    home_page_element = driver.find_element(By.XPATH, "//a[@href='/stories/create/']")
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
            # Tenta encontrar o botão "Ver mais comentários"
            ver_mais_comentarios = driver.find_element(By.XPATH, "//span[contains(text(), 'Ver mais comentários')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ver_mais_comentarios)
            driver.execute_script("arguments[0].click();", ver_mais_comentarios)
            # Espera até que novos comentários apareçam ou um timeout
            time.sleep(2)  # Espera curta para carregar os novos comentários
        except NoSuchElementException:
            print("Não há mais comentários para carregar.")
            break
        except Exception as e:
            print(f"Erro ao clicar no botão: {e}")
            break

        # Após clicar, espera explicitamente que mais comentários apareçam
        try:
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.XPATH, "//div[@class='x169t7cy x19f6ikt']")) > 0
            )
        except Exception as e:
            print(f"Erro durante a espera do carregamento de comentários: {e}")
            break
        
@register_execucao
@capturar_erros
def capture_comments(driver, url, current_user, extrair):
    comment_containers = driver.find_elements(By.XPATH, "//div[@class='x169t7cy x19f6ikt']")
    if not comment_containers:
        print("Nenhum comentário encontrado. Verifique o XPath.")
        return

    comentarios = []
    comentarios_file = generate_unique_file_name(url)
    comentarios_file_txt = generate_unique_file_name(url) + '.txt'
    comentarios_file_excel = generate_unique_file_name(url) + '.xlsx'
    
    for index, container in enumerate(comment_containers):
        print(f"Lendo comentário {index + 1} de {len(comment_containers)}...")
        try:
            placeholder = container.find_element(By.XPATH, ".//div[@aria-placeholder]")
            if placeholder:
                print("Nenhum comentário adicional encontrado. Parando o processamento.")
                break
        except Exception:
            pass 

        user_name = container.find_element(By.XPATH, ".//a[contains(@class, 'x1i10hfl')]/span").text        
        comment_id = "comment_id não encontrado"
        links = container.find_elements(By.XPATH, ".//a[contains(@href, 'comment_id=')]")
        
        for link in links:
            href_full = link.get_attribute("href")
            if "comment_id=" in href_full:
                comment_id = href_full.split("comment_id=")[-1].split("&")[0]
                if re.match(r'^\d+$', comment_id):
                            break
                
        try:
            ver_mais = container.find_element(By.XPATH, ".//div[contains(@class, 'x1i10hfl') and text()='Ver mais']")
            driver.execute_script("arguments[0].click();", ver_mais)
            print("Comentário expandido.")
        except Exception:
            pass  # Se não encontrar o botão 'Ver mais', o comentário já está completo.
        foi_respondido = False  # Definindo um valor padrão

           # Verifica se há a opção "Ver todas as respostas"
        try:
            ver_respostas = container.find_element(By.XPATH, ".//span[contains(text(), 'Ver todas as')]")
            driver.execute_script("arguments[0].click();", ver_respostas)
            print("Respostas expandidas.")
            time.sleep(2)
            foi_respondido = check_response(container, current_user)
        except Exception:
            pass  

        try:
            comment_text = container.find_element(By.XPATH, ".//div[contains(@class, 'x1lliihq')]/span/div").text
            comment_text = comment_text.replace('\n', ' ')  # Remove quebras de linha (\n)
            tipo_conteudo = "Texto"
        except Exception:
            # Se não for possível capturar o texto, setar comment_text como None e identificar o tipo de conteúdo
            comment_text = None
            try:
                # Verifica se o comentário contém uma imagem
                container.find_element(By.XPATH, ".//img")
                tipo_conteudo = "Imagem"
            except Exception:
                try:
                    container.find_element(By.XPATH, ".//video")
                    tipo_conteudo = "Vídeo"
                except Exception:

                    tipo_conteudo = "Outro Conteúdo Não Textual"

        if comment_text is None:
            print(f"Comentário contém um(a) {tipo_conteudo}.")
            generate_log_other_content(url, comment_id, user_name, tipo_conteudo, comment_text)
            continue
        
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
    save_comments_excel(comentarios, comentarios_file_excel)
    if extrair:
        save_comments_txt(comentarios, comentarios_file_txt)
    return comentarios_file

@register_execucao
@capturar_erros
def check_response(container, current_user):
    try:
        response_divs = container.find_elements(
            By.XPATH,
            ".//div[contains(@class, 'html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 x1n2onr6')]//div[contains(@aria-label, 'Resposta de')]"
        )
        for response_div in response_divs:
            aria_label = response_div.get_attribute("aria-label")
            if f"Resposta de {current_user} ao" in aria_label:
                print('Comentário respondido')
                return True
        
        print("Comentário não respondido.")
        return False
    except Exception as e:
        print(f"Comentário não respondido. Erro: {str(e)}")
        return False

@register_execucao
@capturar_erros
def reply_comments(driver, comentarios, comentarios_file, url, prompt_text, personalized_message):
    for comentario in comentarios:
        if comentario['respondido']:
            continue
        ia_response = get_answer_ia(driver, comentario['comentario'], prompt_text, personalized_message)
        if check_response_block(ia_response):
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
        actions.move_to_element(comentario_container).perform()
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comentario_container)
        time.sleep(1)

         # Tentar localizar o botão "Responder"
        try:
            responder_button = comentario_container.find_element(By.XPATH, ".//div[@role='button' and @tabindex='0' and contains(text(), 'Responder')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", responder_button)
        except Exception as e:
            print("Botão 'Responder' não encontrado imediatamente, tentando rolar até ele.")
            # Se não for encontrado, rolar mais uma vez até o botão
            driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", comentario_container)
            responder_button = comentario_container.find_element(By.XPATH, ".//div[@role='button' and @tabindex='0' and contains(text(), 'Responder')]")
        
        # Verificar se o botão está visível e clicá-lo
        if responder_button.is_displayed():
            actions.move_to_element(responder_button).click().perform()
        else:
            print("Tentativa de rolar até o botão novamente.")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", responder_button)
            actions.move_to_element(responder_button).click().perform()

        time.sleep(1)
        actions = ActionChains(driver)
        for char in ia_response:
            actions.send_keys(char)
            actions.perform()
            time.sleep(0.01)   
        time.sleep(1)
        driver.switch_to.active_element.send_keys(Keys.RETURN)
        print(separation_line())
        print(f"Comentário respondido")
        time.sleep(3)
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
        try:
            comment_containers = driver.find_elements(By.XPATH, "//div[@class='html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x18d9i69 x1swvt13 x1pi30zi']")
            if comment_containers:
                # Tentar clicar em 'Mais relevantes'
                try:
                    viewer_full = driver.find_element(By.XPATH, "//span[normalize-space(text())='Mais relevantes']")
                    actions.move_to_element(viewer_full).click().perform()
                    print(f'mais relevantes clicado')
                    time.sleep(2)
                except:
                    print("Botão 'Mais relevantes' não encontrado, tentando 'Mais recentes'.")
                    try:
                        viewer_recent = driver.find_element(By.XPATH, "//span[normalize-space(text())='Mais recentes']")
                        actions.move_to_element(viewer_recent).click().perform()
                        print(f'mais recentes clicado')
                        time.sleep(2)
                    except:
                        print("Botão 'Mais recentes' não encontrado, tentando 'Comentários mais relevantes'.")
                        try:
                            viewer_most_relevant = driver.find_element(By.XPATH, "//span[normalize-space(text())='Comentários mais relevantes']")
                            actions.move_to_element(viewer_most_relevant).click().perform()
                            print(f'Comentários mais relevantes clicado')
                            time.sleep(2)
                        except Exception as e:
                            print(f"Erro ao tentar clicar em 'Comentários mais relevantes': {e}")
                
                # Captura os contêineres de comentários completos
                full_containers = driver.find_elements(By.XPATH, "//div[@class='x4k7w5x x1h91t0o x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1n2onr6 x1qrby5j x1jfb8zj']")
                if full_containers:
                    # Localiza e clica no botão 'Todos os comentários'
                    viewer_full_coments = driver.find_element(By.XPATH, "//span[normalize-space(text())='Todos os comentários']")
                    viewer_full_coments.click()
                    print(f'todos os comentarios clicado')
                else:
                    print("Nenhum contêiner de comentário completo encontrado.")
            else:
                print("Nenhum contêiner de comentário encontrado.")
        except Exception as e:
            print(f"Erro ao tentar capturar todos os comentários: {e}")
    
    elif coments_all == "Relevantes":
        print('Capturar comentários relevantes')

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
def main(url, current_user, personalized_message, log_bloqueio_file, filtro_ativo, extrair, driver):  
    if not extrair:
        open_url(driver)
        verify_login_face(driver, url)
        comments(driver, coments_all)
        load_all_comments(driver)
        
        while not check_stop_signal():
            comentarios_file = capture_comments(driver, url, current_user, extrair)
            comentarios = upload_files_comments(comentarios_file)
            
            filtro_text = filtro(filtro_ativo)
            prompt_text = construct_prompt_text(filtro_text)
            
            reply_comments(driver, comentarios, comentarios_file, url, prompt_text, personalized_message)
            time.sleep(5)  # Pequena pausa entre iterações
            
        print("Sinal de parada detectado. Finalizando iteração.")
    else:
        print("Executando lógica de extração adicional")
        open_url(driver)
        verify_login_face(driver, url)
        comments(driver, coments_all)
        load_all_comments(driver)
        
        comentarios_file = capture_comments(driver, url, current_user, extrair)
        comentarios = upload_files_comments(comentarios_file)
        print("Comentários extraídos com sucesso!")