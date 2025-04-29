"""
Endpoints configuration for Subhue API.
This module centralizes all API endpoints for different environments.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class SubhueEndpoints:
    """Base class for Subhue API endpoints."""

    base_url: str
    unidades: str
    auth: str
    altas: str
    censo_leitos: str
    los: str
    ociosidade: str
    atendimentos: str
    atendimentos_update: str
    classificados: str
    registrados: str
    internacoes: str

    # smsrio
    mapa_leitos: str
    macroindicadores_geral: str
    macroindicadores_pediatrico: str
    macroindicadores_maternidade: str
    casos_sociais: str
    longa_permanencia: str

    @classmethod
    def from_base_url(cls, base_url: str) -> "SubhueEndpoints":
        """Create endpoints from a base URL."""
        return cls(
            base_url=base_url,
            unidades=f"{base_url}/unidades/",
            auth=f"{base_url}/api-token-auth/",
            altas=f"{base_url}/vitai/altas/",
            censo_leitos=f"{base_url}/vitai/censo-leitos/",
            los=f"{base_url}/vitai/los-emergencia/",
            ociosidade=f"{base_url}/vitai/giro-leitos/",
            atendimentos=f"{base_url}/vitai/atendimento/",
            atendimentos_update=f"{base_url}/vitai/atendimento/bulk-update/",
            classificados=f"{base_url}/vitai/classificados/",
            registrados=f"{base_url}/vitai/registrados/",
            internacoes=f"{base_url}/vitai/internacoes/",
            # smrrio
            mapa_leitos=f"{base_url}/mapa/leitos/",
            macroindicadores_geral=f"{base_url}/macroindicadores/geral/",
            macroindicadores_pediatrico=f"{base_url}/macroindicadores/pediatrico/",
            macroindicadores_maternidade=f"{base_url}/macroindicadores/maternidade/",
            casos_sociais=f"{base_url}/smsrio/casos-sociais/",
            longa_permanencia=f"{base_url}/smsrio/longa-permanencia/",
        )


# Production endpoints
PROD_ENDPOINTS = SubhueEndpoints.from_base_url("https://api.subhue.org")

# Development endpoints
DEV_ENDPOINTS = SubhueEndpoints.from_base_url("https://api-dev.subhue.org")

# Local development endpoints
LOCAL_ENDPOINTS = SubhueEndpoints.from_base_url("http://127.0.0.1:8000")

# Backend development endpoints (commented out but kept for reference)
# BACKEND_DEV_ENDPOINTS = SubhueEndpoints.from_base_url("https://backend-dev.subhue.org")

# Available environments
ENVIRONMENTS: Dict[str, SubhueEndpoints] = {
    "prod": PROD_ENDPOINTS,
    "dev": DEV_ENDPOINTS,
    "local": LOCAL_ENDPOINTS,
}


def get_endpoints(environment: str = "prod") -> SubhueEndpoints:
    """
    Get endpoints for a specific environment.

    Args:
        environment: The environment to get endpoints for ('prod', 'dev', 'local')

    Returns:
        SubhueEndpoints: The endpoints for the specified environment

    Raises:
        ValueError: If the environment is not valid
    """
    if environment not in ENVIRONMENTS:
        valid_envs = ", ".join(ENVIRONMENTS.keys())
        raise ValueError(
            f"Invalid environment: {environment}. Valid options: {valid_envs}"
        )

    return ENVIRONMENTS[environment]
