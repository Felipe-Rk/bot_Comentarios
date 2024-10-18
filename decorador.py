import functools
import os
import datetime
import traceback
from arquivos import create_log_execucao, folder_system

# Criar diretórios necessários e obter os caminhos
dados_path, logs_path = folder_system()

def capturar_erros(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Captura o traceback completo em formato de string
            error_trace = traceback.format_exc()
            # Você pode customizar 'url_ou_id' conforme necessário ou passar como argumento
            log_message = f"{func.__name__} - Erro ocorrido: {str(e)}\nDetalhes:\n{error_trace}"
            create_log_execucao('url_ou_id', log_message)  
            print(f"Erro na função {func.__name__}: {e}")
            print(f"Detalhes do erro:\n{error_trace}")  # Exibe o traceback completo no console
            return None
    return wrapper

def register_execucao(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                log_message = f"{func.__name__} - Finalizada com erro"
            else:
                log_message = f"{func.__name__} - Finalizada com sucesso"
            create_log_execucao('url_ou_id', log_message)
            return result
        except Exception as e:
            # Captura o traceback completo em formato de string
            error_trace = traceback.format_exc()
            log_message = f"{func.__name__} - Finalizada com erro: {str(e)}\nDetalhes:\n{error_trace}"
            create_log_execucao('url_ou_id', log_message)
            return None
    return wrapper
