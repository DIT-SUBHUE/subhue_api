"""
Converters module for handling data type conversions.
"""

from datetime import datetime
from typing import Optional

import pandas as pd


class DataConverter:
    """Classe responsável pela conversão de dados para diferentes tipos."""

    @staticmethod
    def clean_text(value):
        """Remove espaços extras e converte NaN para None."""
        return None if pd.isnull(value) else str(value).strip()

    @staticmethod
    def convert_to_int(value):
        """Converte float para inteiro, se possível."""
        return None if pd.isnull(value) else int(value)

    @staticmethod
    def convert_to_datetime(value):
        """Converte datetime para o formato desejado."""
        return (
            None
            if pd.isnull(value) or value == "" or not isinstance(value, datetime)
            else value.strftime("%Y-%m-%d %H:%M:%SZ")
        )

    @staticmethod
    def convert_to_date(value):
        """Converte datetime para o formato desejado."""
        return (
            None
            if pd.isnull(value) or value == "" or not isinstance(value, datetime)
            else value.strftime("%Y-%m-%d")
        )

    @staticmethod
    def convert_to_float(value):
        """Converte float para float mesmo, tratando NaN."""
        return None if pd.isnull(value) else float(value)

    @staticmethod
    def convert_to_bool(value: str):
        """Converte valor para booleano."""
        negative_values = ["não", "nao", "n", "0", "false"]
        return False if str(value).lower() in negative_values else True
