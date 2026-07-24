
from __future__ import annotations

import math
import random
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# Experimento 1: variacao automatica de cor
# ---------------------------------------------------------------------------

def gerar_cor_aleatoria(rng: random.Random | None = None) -> tuple[float, float, float, float]:
    r = rng if rng is not None else random
    return (r.random(), r.random(), r.random(), 1.0)


# ---------------------------------------------------------------------------
# Experimento 2: multiplos objetos na cena
# ---------------------------------------------------------------------------

TIPOS_VALIDOS = ("cube", "sphere", "cylinder")

CONFIGURACAO_PADRAO = [
    {"tipo": "cube", "location": (-2, 0, 1)},
    {"tipo": "sphere", "location": (0, 0, 1)},
    {"tipo": "cylinder", "location": (2, 0, 1)},
]


def gerar_configuracao_objetos() -> list[dict]:
    return [dict(cfg) for cfg in CONFIGURACAO_PADRAO]


def gerar_nome_objeto(indice: int, tipo: str) -> str:
    return f"Object_{indice}_{tipo}"


def nomes_dos_objetos(configs: Sequence[dict]) -> list[str]:
    return [gerar_nome_objeto(i, cfg["tipo"]) for i, cfg in enumerate(configs)]


def distancia(p1: Iterable[float], p2: Iterable[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def verificar_sem_sobreposicao(configs: Sequence[dict], distancia_minima: float = 1.0) -> bool:
    locais = [cfg["location"] for cfg in configs]
    for i in range(len(locais)):
        for j in range(i + 1, len(locais)):
            if distancia(locais[i], locais[j]) < distancia_minima:
                return False
    return True