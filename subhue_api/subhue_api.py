"""
Main Subhue API integration module.
This module provides the main Subhue class that serves as a facade for the API components.
"""

import logging
import os
from typing import Dict, List, Optional

import pandas as pd
from dotenv import load_dotenv

from .auth import TokenAuth
from .client import ApiResponseProcessor, HttpClient
from .config import EndpointConfig
from .converters import DataConverter
from .processors import BatchProcessor, DataFrameProcessor

load_dotenv()


class SubhueAPI:
    """Classe de fachada que integra os componentes para interação com a API Subhue."""

    def __init__(self, endpoint: str, environment: str = "prod"):
        """
        Inicializa a API Subhue.

        Args:
            endpoint: O tipo de endpoint a ser usado ('altas', 'atendimentos', etc.)
            environment: O ambiente a ser usado ('prod', 'dev', 'local')
        """
        # Configura a dependência de componentes
        self.config = EndpointConfig(environment)
        self.data_converter = DataConverter()
        self.df_processor = DataFrameProcessor(self.data_converter)
        self.response_processor = ApiResponseProcessor()

        # Autenticação
        auth_url = self.config.get_auth_url()
        username = os.getenv("LOGIN_SUBHUE")
        password = os.getenv("SENHA_SUBHUE")
        self.auth = TokenAuth(username, password, auth_url)

        # URLs
        self.api_url = auth_url
        self.endpoint_url = self.config.get_endpoint_url(endpoint)

        # Token e Headers
        self.token = self.auth.get_token()
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

        # Cliente HTTP
        self.api_client = HttpClient(
            self.endpoint_url, self.headers, self.response_processor
        )
        self.batch_processor = BatchProcessor(self.api_client)

        logging.info("Token da API SUBHUE obtido com sucesso!")
        logging.info(f"URL de endpoint: {self.endpoint_url}")

    def prepare_payload_from_dataframe(
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
        return self.df_processor.prepare_payload(
            dataframe,
            date_columns,
            only_date_columns,
            numeric_columns,
            float_columns,
            boolean_columns,
        )

    def send_payload(
        self,
        payload: List[Dict],
        batch_size: int = 1,
        sleep_time: int = 0,
        method: str = "POST",
        max_errors: Optional[int] = None,
    ):
        """
        Envia o payload para a API em lotes de tamanho fixo.
        """
        self.batch_processor.process_in_batches(
            payload, batch_size, sleep_time, method, max_errors
        )


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    API_USERNAME = os.getenv("LOGIN_SUBHUE")
    API_PASSWORD = os.getenv("SENHA_SUBHUE")

    print("API_USERNAME:", API_USERNAME)
    print("API_PASSWORD:", API_PASSWORD)

    # Exemplo de uso com ambiente de desenvolvimento
    subhue = SubhueAPI("altas", environment="dev")
    print(f"Token: {subhue.token}")
    print(f"Endpoint URL: {subhue.endpoint_url}")
