import random
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "blender_scripts"))

import pytest
from experiment_utils import (
    gerar_cor_aleatoria,
    gerar_configuracao_objetos,
    gerar_nome_objeto,
    nomes_dos_objetos,
    verificar_sem_sobreposicao,
    TIPOS_VALIDOS,
)


# ---------------------------------------------------------------------------
# Experimento 1: cor aleatoria
# ---------------------------------------------------------------------------

class TestCorAleatoria:

    @pytest.mark.parametrize("_", range(20))
    def test_valores_dentro_do_intervalo_rgb(self, _):
        r, g, b, a = gerar_cor_aleatoria()
        assert 0.0 <= r <= 1.0
        assert 0.0 <= g <= 1.0
        assert 0.0 <= b <= 1.0

    def test_canal_alpha_sempre_fixo_em_1(self):
        _, _, _, a = gerar_cor_aleatoria()
        assert a == 1.0

    def test_retorna_tupla_de_4_elementos(self):
        cor = gerar_cor_aleatoria()
        assert isinstance(cor, tuple)
        assert len(cor) == 4

    def test_reprodutivel_com_mesmo_seed(self):
        cor1 = gerar_cor_aleatoria(random.Random(42))
        cor2 = gerar_cor_aleatoria(random.Random(42))
        assert cor1 == cor2

    def test_seeds_diferentes_geram_cores_diferentes(self):
        cor1 = gerar_cor_aleatoria(random.Random(1))
        cor2 = gerar_cor_aleatoria(random.Random(2))
        assert cor1 != cor2

    def test_execucoes_sucessivas_variam(self):
        # Sanidade: gerar 10 cores sem seed fixo nao deve produzir a mesma
        # cor 10 vezes seguidas (probabilidade praticamente nula).
        cores = {gerar_cor_aleatoria() for _ in range(10)}
        assert len(cores) > 1


# ---------------------------------------------------------------------------
# Experimento 2: multiplos objetos
# ---------------------------------------------------------------------------

class TestMultiplosObjetos:

    def test_quantidade_de_objetos(self):
        config = gerar_configuracao_objetos()
        assert len(config) == 3

    def test_tipos_sao_validos(self):
        config = gerar_configuracao_objetos()
        for obj in config:
            assert obj["tipo"] in TIPOS_VALIDOS

    def test_cada_objeto_tem_localizacao_com_3_coordenadas(self):
        config = gerar_configuracao_objetos()
        for obj in config:
            assert len(obj["location"]) == 3

    def test_nomes_sao_unicos(self):
        config = gerar_configuracao_objetos()
        nomes = nomes_dos_objetos(config)
        assert len(nomes) == len(set(nomes))

    def test_nome_segue_padrao_esperado(self):
        assert gerar_nome_objeto(0, "cube") == "Object_0_cube"
        assert gerar_nome_objeto(2, "cylinder") == "Object_2_cylinder"

    def test_objetos_nao_se_sobrepoem(self):
        config = gerar_configuracao_objetos()
        assert verificar_sem_sobreposicao(config, distancia_minima=1.0)

    def test_deteccao_de_sobreposicao_funciona(self):
        # Sanidade do proprio teste: se dois objetos estiverem na mesma
        # posicao, a funcao precisa detectar a sobreposicao.
        config_com_sobreposicao = [
            {"tipo": "cube", "location": (0, 0, 1)},
            {"tipo": "sphere", "location": (0, 0, 1)},
        ]
        assert not verificar_sem_sobreposicao(config_com_sobreposicao, distancia_minima=1.0)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))