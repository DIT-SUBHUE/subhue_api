"""
Data processing module for Subhue API.
"""

import logging
import time
from typing import Any, Dict, List, Optional

import pandas as pd

from .client import ApiClient
from .converters import DataConverter


class DataFrameProcessor:
    """Classe responsável por processar DataFrames."""

    def __init__(self, converter: DataConverter):
        self.converter = converter

    def prepare_payload(
        self,
        dataframe: pd.DataFrame,
        date_columns: Optional[List[str]] = None,
        only_date_columns: Optional[List[str]] = None,
        numeric_columns: Optional[List[str]] = None,
        float_columns: Optional[List[str]] = None,
        boolean_columns: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        Cria uma lista de dicionários a partir de um DataFrame, com tratamento dinâmico para colunas específicas.
        """
        date_columns = date_columns or []
        only_date_columns = only_date_columns or []
        numeric_columns = numeric_columns or []
        float_columns = float_columns or []
        boolean_columns = boolean_columns or []

        dict_list = []
        for _, row in dataframe.iterrows():
            payload = {}
            for col in dataframe.columns:
                if col in date_columns:
                    payload[col] = self.converter.convert_to_datetime(row[col])
                elif col in only_date_columns:
                    payload[col] = self.converter.convert_to_date(row[col])
                elif col in numeric_columns:
                    payload[col] = self.converter.convert_to_int(row[col])
                elif col in float_columns:
                    payload[col] = self.converter.convert_to_float(row[col])
                elif col in boolean_columns:
                    payload[col] = self.converter.convert_to_bool(row[col])
                else:
                    payload[col] = self.converter.clean_text(row[col])
            dict_list.append(payload)
        return dict_list


class BatchProcessor:
    """Classe responsável por processar envios em lote."""

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def process_in_batches(
        self,
        payload: List[Dict],
        batch_size: int = 1,
        sleep_time: int = 0,
        method: str = "POST",
        max_errors: Optional[int] = None,
    ):
        """Processa envio de dados em lotes."""
        logging.info(f"{method} - Iniciando envio de dados para a API.")
        logging.info(
            f"PAYLOAD_LEN: {len(payload)} - BATCH_SIZE: {batch_size} - SLEEP_TIME: {sleep_time} - MAX_ERRORS: {max_errors}"
        )
        error_count = 0

        try:
            for i in range(0, len(payload), batch_size):
                batch = payload[i : i + batch_size]
                try:
                    self.api_client.send_request(batch, method)
                    logging.info(
                        f"✅ Enviado lote {i // batch_size + 1} de {len(payload) // batch_size + 1}"
                    )
                except Exception as e:
                    error_count += 1
                    logging.error(f"❌ Erro ao enviar lote {i // batch_size + 1}: {e}")

                    # Verifica se o número máximo de erros foi atingido
                    if max_errors is not None and error_count >= max_errors:
                        logging.error(
                            f"🚫 Número máximo de erros ({max_errors}) atingido. Interrompendo envio."
                        )
                        break
                finally:
                    time.sleep(sleep_time)
        except Exception as e:
            logging.error(f"❌ Erro inesperado: {e}")
        finally:
            logging.info(f"📊 Total de erros durante o envio: {error_count}")
