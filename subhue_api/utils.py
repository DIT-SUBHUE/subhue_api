import logging
import os
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests

URL = "https://api.subhue.org/unidades/"


def obter_e_filtrar_unidades(
    filtros: Dict[str, List[str]],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Obtém dados de unidades a partir da API e os filtra com base nos critérios especificados.
    """
    logging.info("Iniciando obter_e_filtrar_unidades")
    logging.debug(f"Parâmetros recebidos em filtros: {filtros}")

    df = obter_unidades_da_api()
    if df is None:
        logging.info("Não foi possível obter dados da API.")
        return None, None

    try:
        logging.debug("Preenchendo coluna 'cnes' com zeros à esquerda.")
        df["cnes"] = df["cnes"].str.zfill(7)
    except Exception as e:
        logging.error(f"Erro ao preencher CNES com zeros à esquerda: {e}")

    logging.info("Chamando filtrar_unidades")
    return filtrar_unidades(df, filtros)


def filtrar_unidades(
    df: pd.DataFrame, filtros: Dict[str, List[str]]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filtra unidades com base nos critérios especificados.
    """
    logging.info("Iniciando filtrar_unidades")
    logging.debug(f"Shape do DataFrame recebido: {df.shape}")
    logging.debug(f"Filtros recebidos: {filtros}")

    try:
        # Filtros para unidades hospitalares
        cond_tipo_hospitalar = df["tipo_unidade"].isin(filtros["tipos_hospitalares"])
        cond_cnes_hospitalar = df["cnes"] == filtros["cnes_hospitalar"]
        cond_cnes2_hospitalar = ~df["cnes"].isin(filtros["cnes_excluidos_hospitalar"])
        df_hospitalar = df[
            (cond_tipo_hospitalar & cond_cnes2_hospitalar) | cond_cnes_hospitalar
        ].copy()
        logging.debug(f"Unidades hospitalares filtradas: {df_hospitalar.shape}")

        # Filtros para unidades de emergência
        cond_tipo_emergencia = ~df["tipo_unidade"].isin(
            filtros["tipos_emergencia_excluidos"]
        )
        cond_cnes_emergencia = ~df["cnes"].isin(filtros["cnes_excluidos_emergencia"])
        cond_cnes2_emergencia = df["cnes"].isin(filtros["cnes_incluidos_emergencia"])
        df_emergencia = df[
            (cond_tipo_emergencia & cond_cnes_emergencia) | cond_cnes2_emergencia
        ].copy()
        logging.debug(f"Unidades de emergência filtradas: {df_emergencia.shape}")

        return df_hospitalar, df_emergencia
    except Exception as e:
        logging.error(f"Erro ao filtrar unidades: {e}")
        return None, None


def obter_unidades_da_api(timeout: int = 25) -> Optional[pd.DataFrame]:
    """
    Obtém unidades de uma API e os converte em um DataFrame do Pandas.
    """
    logging.info(f"Iniciando requisição para {URL}")
    logging.debug(f"Timeout configurado: {timeout}")

    try:
        response = requests.get(URL, timeout=timeout)
        response.raise_for_status()
        logging.info("Requisição bem-sucedida.")
    except requests.exceptions.Timeout as te:
        logging.error(f"Timeout na requisição para {URL}: {te}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição: {e}")
        return None

    try:
        dados = response.json()
        logging.debug(f"Dados obtidos: {dados}")
        df = pd.DataFrame(dados)
        logging.debug(f"DataFrame criado com shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Erro ao processar dados da API: {e}")
        return None
