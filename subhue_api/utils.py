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

    Args:
        url (str): URL da API para obter os dados.
        filtros (Dict[str, List[str]]): Dicionário com os critérios de filtragem.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Uma tupla contendo dois DataFrames, o primeiro com as unidades hospitalares
        e o segundo com as unidades de emergência. Retorna (None, None) em caso de erro.
    """
    df = obter_unidades_da_api()
    if df is None:
        return None, None

    try:
        df["cnes"] = df["cnes"].str.zfill(7)
    except Exception as e:
        logging.error(f"Erro ao preencher CNES com zeros à esquerda: {e}")

    return filtrar_unidades(df, filtros)


def filtrar_unidades(
    df: pd.DataFrame, filtros: Dict[str, List[str]]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filtra unidades com base nos critérios especificados.

    Args:
        df (pd.DataFrame): DataFrame contendo as unidades.
        filtros (Dict[str, List[str]]): Dicionário com os critérios de filtragem.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Uma tupla contendo dois DataFrames, o primeiro com as unidades hospitalares
        e o segundo com as unidades de emergência.
    """
    try:
        # Filtros para unidades hospitalares
        cond_tipo_hospitalar = df["tipo_unidade"].isin(filtros["tipos_hospitalares"])
        cond_cnes_hospitalar = df["cnes"] == filtros["cnes_hospitalar"]
        cond_cnes2_hospitalar = ~df["cnes"].isin(filtros["cnes_excluidos_hospitalar"])
        df_hospitalar = df[
            (cond_tipo_hospitalar & cond_cnes2_hospitalar) | cond_cnes_hospitalar
        ].copy()

        # Filtros para unidades de emergência
        cond_tipo_emergencia = ~df["tipo_unidade"].isin(
            filtros["tipos_emergencia_excluidos"]
        )
        cond_cnes_emergencia = ~df["cnes"].isin(filtros["cnes_excluidos_emergencia"])
        cond_cnes2_emergencia = df["cnes"].isin(filtros["cnes_incluidos_emergencia"])
        df_emergencia = df[
            (cond_tipo_emergencia & cond_cnes_emergencia) | cond_cnes2_emergencia
        ].copy()

        return df_hospitalar, df_emergencia
    except Exception as e:
        logging.error(f"Erro ao filtrar unidades: {e}")
        return None, None


def obter_unidades_da_api(timeout: int = 25) -> Optional[pd.DataFrame]:
    """
    Obtém unidades de uma API e os converte em um DataFrame do Pandas.

    Args:
        url (str): URL da API para obter os dados.
        timeout (int): Tempo máximo de espera para a requisição.

    Returns:
        Optional[pd.DataFrame]: DataFrame com os dados obtidos, ou None em caso de erro.
    """
    logging.info(f"Iniciando requisição para {URL}")

    try:
        response = requests.get(URL, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout as te:
        logging.error(f"Timeout na requisição para {URL}: {te}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição: {e}")
        return None

    try:
        dados = response.json()
        logging.debug(f"Dados obtidos: {dados}")
        return pd.DataFrame(dados)
    except Exception as e:
        logging.error(f"Erro ao processar dados da API: {e}")
        return None
