"""
HTTP client module for Subhue API communication.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup


class ApiClient(ABC):
    """Interface abstrata para cliente de API."""

    @abstractmethod
    def send_request(self, data: List[Dict], method: str = "POST") -> Any:
        """Envia requisição para a API."""
        pass


class ApiResponseProcessor:
    """Classe responsável por processar as respostas da API."""

    def process_response(self, response):
        """Processa a resposta da API."""
        post_result = {}
        try:
            response_json = response.json()
            if isinstance(response_json, dict) and "inseridos" in response_json:
                post_result["inseridos"] = response_json.get("inseridos", [])
                post_result["atualizados"] = response_json.get("atualizados", [])
                post_result["falhas"] = response_json.get("falhas", [])

                logging.info(f"📥 Resultado do Lote: {post_result}")
                logging.debug(
                    f"Falhas: {response_json.get(
                    "detalhes_falhas", []
                )}"
                )
                return post_result
        except ValueError:
            logging.warning("A resposta não é um JSON válido.")
            return None


class HttpClient(ApiClient):
    """Implementação concreta de cliente HTTP."""

    def __init__(
        self,
        endpoint_url: str,
        headers: Dict[str, str],
        response_processor: ApiResponseProcessor,
    ):
        self.endpoint_url = endpoint_url
        self.headers = headers
        self.response_processor = response_processor

    def send_request(self, data: List[Dict], method: str = "POST") -> Any:
        """Envia requisição HTTP."""
        try:
            response = requests.request(
                method=method.upper(),
                url=self.endpoint_url,
                json=data,
                headers=self.headers,
            )
            response.raise_for_status()
            return self.response_processor.process_response(response)
        except Exception as e:
            logging.error(f"Erro ao enviar requisição: {e}")

            if response is not None:
                try:
                    soup = BeautifulSoup(response.text, "html.parser")
                    api_error = soup.find(class_="exception_value").text
                    logging.error(f"📥 Resposta da API: {api_error}")
                except Exception:
                    logging.error(f"📥 Resposta da API: {response.text}")
            else:
                logging.error("📥 Nenhuma resposta da API foi recebida.")

            return None
