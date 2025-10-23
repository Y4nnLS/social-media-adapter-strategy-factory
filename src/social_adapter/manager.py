
from __future__ import annotations
from datetime import datetime
from typing import Dict, Iterable, List
from .models import Conteudo, Estatisticas, UnifiedResponse
from .adapters.base import SocialMediaAdapter


class GerenciadorMidiaSocial:
    """Fachada unificada para orquestrar adapters e estratégias."""

    def __init__(self):
        self.adapters: Dict[str, SocialMediaAdapter] = {}

    def registrar(self, nome: str, adapter: SocialMediaAdapter) -> None:
        self.adapters[nome] = adapter

    def publicar(self, conteudo: Conteudo, plataformas: Iterable[str]) -> List[UnifiedResponse]:
        responses: List[UnifiedResponse] = []
        for nome in plataformas:
            adapter = self.adapters.get(nome)
            if not adapter:
                responses.append(UnifiedResponse(status="error", platform=nome, message="Adapter não registrado"))
                continue
            responses.append(adapter.publicar(conteudo))
        return responses

    def agendar(self, conteudo: Conteudo, quando: datetime, plataformas: Iterable[str]) -> List[UnifiedResponse]:
        responses: List[UnifiedResponse] = []
        for nome in plataformas:
            adapter = self.adapters.get(nome)
            if not adapter:
                responses.append(UnifiedResponse(status="error", platform=nome, message="Adapter não registrado"))
                continue
            responses.append(adapter.agendar(conteudo, quando))
        return responses

    def estatisticas(self, platform: str, external_id: str) -> Estatisticas:
        adapter = self.adapters.get(platform)
        if not adapter:
            raise KeyError(f"Adapter '{platform}' não registrado.")
        return adapter.obter_estatisticas(external_id)
