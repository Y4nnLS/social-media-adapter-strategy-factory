
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from ..models import Conteudo, Estatisticas, UnifiedResponse


class SocialMediaAdapter(ABC):
    """Interface comum para qualquer plataforma de mídia social."""

    platform: str

    @abstractmethod
    def publicar(self, conteudo: Conteudo) -> UnifiedResponse:
        ...

    @abstractmethod
    def agendar(self, conteudo: Conteudo, quando: datetime) -> UnifiedResponse:
        ...

    @abstractmethod
    def obter_estatisticas(self, external_id: str) -> Estatisticas:
        ...


class SimulatedAPIError(Exception):
    pass
