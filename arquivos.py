from datetime import datetime
import xlsxwriter
import sys
import time
import hashlib
import json
import os

# Função para detectar o caminho correto para salvar os arquivos
def folder_system():
    if getattr(sys, 'frozen', False):  # Se estiver rodando como executável
        base_path = os.path.dirname(sys.executable)  # Obtém o diretório onde o executável foi iniciado
    else:  
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    dados_path = os.path.join(base_path, 'dados')
    logs_path = os.path.join(base_path, 'logs')
    
    # Cria as pastas se não existirem
    os.makedirs(dados_path, exist_ok=True)
    os.makedirs(logs_path, exist_ok=True)

    return dados_path, logs_path

# Obtém os caminhos dos diretórios ao iniciar
dados_path, logs_path = folder_system()

def generate_unique_file_name(url):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    print("Arquivo de dados gerado")
    return os.path.join(dados_path, f"comentarios_{url_hash}.json")

def generate_path_log(url, tipo_log):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(logs_path, f"{tipo_log}_{url_hash}.txt")

def create_log_excecao(url, mensagem):
    caminho_log = generate_path_log(url, 'erro')
    with open(caminho_log, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()} - {mensagem}\n")

def create_log_execucao(url, mensagem):
    caminho_log = generate_path_log(url, 'execucao')
    with open(caminho_log, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()} - {mensagem}\n")

def generate_log_block(url, comentario_id, nome_usuario, comentario_texto):
    log_file = os.path.join(logs_path, f"bloqueio_{hashlib.md5(url.encode()).hexdigest()}.txt")
    
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_content = ( 
        f"URL da Página: {url}\n"
        f"ID do Comentário: {comentario_id}\n"
        f"Nome do Usuário: {nome_usuario}\n"
        f"Comentário: {comentario_texto}\n"
        f"Data e Hora: {data_hora}\n"
        f"-----------------------------------\n"
    )
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_content)
    
    print(f"Log de bloqueio gerado: {log_file}")

def generate_log_other_content(url, comentario_id, nome_usuario, tipo_conteudo, comentario):
    log_file = os.path.join(logs_path, f"texto_outro_conteudo_ignorado_{hashlib.md5(url.encode()).hexdigest()}.txt")
    
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_content = ( 
        f"URL da Página: {url}\n"
        f"ID do Comentário: {comentario_id}\n"
        f"Nome do Usuário: {nome_usuario}\n"
        f"Tipo de Conteúdo: {tipo_conteudo}\n"  # Agora registramos o tipo de conteúdo
        f"Conteúdo: {comentario}\n "
        f"Data e Hora: {data_hora}\n"
        f"-----------------------------------\n"
    )
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_content)
    
    print(f"Log de bloqueio gerado: {log_file}")
    
def check_response_block(resposta_ia):
    return "Esse comentário não pode ser respondido" in resposta_ia

def save_comments(comentarios, comentarios_file):
    with open(comentarios_file, 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=4)
    print("Comentários capturados e salvos.")

def save_comments_txt(comentarios, comentarios_file_txt):
    with open(comentarios_file_txt, 'w', encoding='utf-8') as f:
        for comentario in comentarios:
            f.write(f"ID: {comentario['comment_id']}\n")
            f.write(f"Nome: {comentario['nome']}\n")
            f.write(f"Comentário: {comentario['comentario']}\n")
            f.write(f"Respondido: {'Sim' if comentario['respondido'] else 'Não'}\n")
            f.write("-" * 50 + "\n")
    print("Comentários capturados e salvos em TXT.")
    os.startfile(comentarios_file_txt)

def save_comments_excel(comentarios, comentarios_file_excel):
    workbook = xlsxwriter.Workbook(comentarios_file_excel)
    worksheet = workbook.add_worksheet()

    # Cabeçalhos
    headers = ['ID', 'Nome', 'Comentário', 'Respondido']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Adicionando os comentários
    for row_num, comentario in enumerate(comentarios, 1):
        worksheet.write(row_num, 0, comentario['comment_id'])
        worksheet.write(row_num, 1, comentario['nome'])
        worksheet.write(row_num, 2, comentario['comentario'])
        worksheet.write(row_num, 3, 'Sim' if comentario['respondido'] else 'Não')

    workbook.close()
    print("Comentários capturados e salvos em Excel.")


def upload_files_comments(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar comentários: {e}")
        return []

def timeout(start_time, timeout=120):
    if time.time() - start_time > timeout:
        print('Tempo para ação atingido. Finalizando sistema!')
        sys.exit() 

def separation_line():
    return '----------------------------------------------------------------------------'

def save_log_block_comments(comentario, total_comentarios):
    caminho_arquivo = os.path.join(logs_path, 'SystemLog32.txt')
    
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) >= 2:
                execucoes_registradas = int(linhas[1].strip().split(':')[1])
            else:
                execucoes_registradas = 0
    else:
        execucoes_registradas = 0

    if execucoes_registradas >= total_comentarios:
        print(f"O código já foi executado {total_comentarios} vezes. Execução não permitida.")
        sys.exit()

    execucoes_registradas += 1

    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.write(f'Chave:{comentario}\nExecucoes:{execucoes_registradas}')

    print(f"Executando pela {execucoes_registradas}ª vez.")
