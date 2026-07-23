"""
Benchmark de performance.
"""

import time
import tracemalloc
from functools import wraps
from logs.logger import logger


def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        logger.info(f"[BENCHMARK] {func.__qualname__}: {tempo_ms:.1f} ms")
        return resultado
    return wrapper


def medir_memoria(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        resultado = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        logger.info(f"[MEMORIA] {func.__qualname__}: pico={peak/1024:.1f} KB")
        return resultado
    return wrapper


class BenchmarkSuite:
    def __init__(self):
        self.resultados = []

    def executar(self, nome, func, *args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        self.resultados.append({"nome": nome, "tempo_ms": round(tempo_ms, 2)})
        return resultado

    def relatorio(self):
        import pandas as pd
        df = pd.DataFrame(self.resultados)
        if not df.empty:
            df = df.sort_values("tempo_ms", ascending=False).reset_index(drop=True)
        return df

    def tempo_total(self):
        return sum(r["tempo_ms"] for r in self.resultados)