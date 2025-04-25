"""
Authentication module for Subhue API.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional

import requests


class ApiAuth(ABC):
    """Interface abstrata para autenticação de API."""

    @abstractmethod
    def get_token(self) -> str:
        """Obtém o token de autenticação."""
        pass


class TokenAuth(ApiAuth):
    """Implementação concreta para autenticação baseada em token."""

    def __init__(self, username: str, password: str, auth_url: str):
        self.username = username
        self.password = password
        self.auth_url = auth_url

    def get_token(self) -> Optional[str]:
        """Obtém token usando credenciais username/password."""
        try:
            credenciais = {
                "username": self.username,
                "password": self.password,
            }
            logging.debug(f"Credenciais: {credenciais}")
            logging.info(f"Obtendo token da API: {self.auth_url}")
            response = requests.post(url=self.auth_url, data=credenciais)
            response.raise_for_status()
            return response.json().get("token", "Token não encontrado na resposta")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao obter token: {e}")
            return None

if __name__ == "__main__":
    # Exemplo de uso
    auth = TokenAuth(
        username="17266204763",
        password="subhue*2025",
        auth_url="http://127.0.0.1:8000/api-token-auth/"
    )
    token = auth.get_token()
    print(token)