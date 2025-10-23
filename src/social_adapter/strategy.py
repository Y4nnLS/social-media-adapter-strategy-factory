
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, List
from .models import Conteudo, UnifiedResponse
from .adapters.base import SocialMediaAdapter


class ScheduleStrategy(ABC):
    @abstractmethod
    def executar(self, conteudo: Conteudo, adapters: Iterable[SocialMediaAdapter]) -> List[UnifiedResponse]:
        ...


class ImmediateStrategy(ScheduleStrategy):
    def executar(self, conteudo: Conteudo, adapters: Iterable[SocialMediaAdapter]) -> List[UnifiedResponse]:
        responses: List[UnifiedResponse] = []
        for adapter in adapters:
            responses.append(adapter.publicar(conteudo))
        return responses


class QueuedScheduleStrategy(ScheduleStrategy):
    """Simula agendamento: grava 'when' e retorna 'scheduled'."""
    def __init__(self, when: datetime):
        self.when = when

    def executar(self, conteudo: Conteudo, adapters: Iterable[SocialMediaAdapter]) -> List[UnifiedResponse]:
        responses: List[UnifiedResponse] = []
        for adapter in adapters:
            responses.append(adapter.agendar(conteudo, self.when))
        return responses
