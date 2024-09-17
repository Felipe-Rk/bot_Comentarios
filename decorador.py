import functools
import os
import datetime
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
            create_log_execucao('url_ou_id', f"{func.__name__} - Erro ocorrido - {e}")  # 'url_ou_id' é um placeholder
            print(f"Erro na função {func.__name__}: {e}")
            return None
    return wrapper

def register_execucao(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                create_log_execucao('url_ou_id', f"{func.__name__} - Finalizada com erro")
            else:
                create_log_execucao('url_ou_id', f"{func.__name__} - Finalizada")
            return result
        except Exception as e:
            create_log_execucao('url_ou_id', f"{func.__name__} - Finalizada com erro ")
            # Note que o erro não é re-lançado, para manter o programa rodando
            return None
    return wrapper
        
