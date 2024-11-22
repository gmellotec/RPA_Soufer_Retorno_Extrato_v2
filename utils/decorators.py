from functools import wraps
import time
from __init__ import log

def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        duracao = fim - inicio
        # Convertendo segundos para horas, minutos e segundos
        horas, resto = divmod(duracao, 3600)
        minutos, segundos = divmod(resto, 60)
        log.info(f"Tempo total de execução: {int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}")
        return resultado
    return wrapper