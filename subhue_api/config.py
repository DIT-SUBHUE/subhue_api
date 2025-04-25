"""
Configuration module for Subhue API endpoints.
"""

from .endpoints import SubhueEndpoints, get_endpoints


class EndpointConfig:
    """Configuração de endpoints de API."""

    def __init__(self, environment: str = "prod"):
        """
        Inicializa a configuração de endpoints.

        Args:
            environment: O ambiente a ser usado ('prod', 'dev', 'local')
        """
        self.endpoints: SubhueEndpoints = get_endpoints(environment)
        self.dev_mode = environment != "prod"

    def get_auth_url(self) -> str:
        """Retorna URL de autenticação."""
        return self.endpoints.auth

    def get_endpoint_url(self, endpoint: str) -> str:
        """
        Retorna URL do endpoint solicitado.

        Args:
            endpoint: Nome do endpoint ('altas', 'atendimentos', etc.)

        Returns:
            str: URL completa do endpoint

        Raises:
            AttributeError: Se o endpoint não existir
        """
        endpoint = endpoint.lower()
        if not hasattr(self.endpoints, endpoint):
            valid_endpoints = [
                attr
                for attr in dir(self.endpoints)
                if not attr.startswith("_") and attr != "base_url"
            ]
            raise AttributeError(
                f"Endpoint '{endpoint}' não encontrado. Opções válidas: {', '.join(valid_endpoints)}"
            )

        return getattr(self.endpoints, endpoint)
