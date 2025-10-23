
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Dict, Optional
from .base import SocialMediaAdapter, SimulatedAPIError
from ..models import Conteudo, Estatisticas, UnifiedResponse


@dataclass
class InstagramAPI:
    api_key: str
    api_secret: str
    enabled: bool = True

    def _check(self):
        if not self.enabled:
            raise SimulatedAPIError("Instagram desabilitado via configuração.")
        if not self.api_key or not self.api_secret:
            raise SimulatedAPIError("Credenciais inválidas/ausentes para Instagram.")

    def post(self, text: str, media: Optional[list] = None) -> Dict[str, str]:
        self._check()
        # Simula criação de um ID e link público
        exid = "instagram_" + uuid.uuid4().hex[:8]
        return {"id": exid, "link": f"https://instagram.example.com/p/" + exid}

    def schedule(self, text: str, when: datetime, media: Optional[list] = None) -> Dict[str, str]:
        self._check()
        exid = "sched_instagram_" + uuid.uuid4().hex[:8]
        return {"id": exid, "link": f"https://instagram.example.com/s/" + exid, "when": when.isoformat()}

    def stats(self, external_id: str) -> Dict[str, int]:
        self._check()
        # Simula métricas aleatórias determinísticas baseadas no ID
        seed = sum(ord(c) for c in external_id) % 100
        return {"likes": seed, "comments": seed // 2, "shares": seed // 3, "views": seed * 10}


class InstagramAdapter(SocialMediaAdapter):
    platform = "instagram"

    def __init__(self, api: InstagramAPI):
        self.api = api

    def publicar(self, conteudo: Conteudo) -> UnifiedResponse:
        try:
            result = self.api.post(conteudo.texto, conteudo.midias or [])
            return UnifiedResponse(
                status="success",
                platform=self.platform,
                message="Publicado com sucesso",
                external_id=result["id"],
                permalink=result.get("link"),
            )
        except SimulatedAPIError as e:
            return UnifiedResponse(status="error", platform=self.platform, message=str(e))

    def agendar(self, conteudo: Conteudo, quando: datetime) -> UnifiedResponse:
        try:
            result = self.api.schedule(conteudo.texto, quando, conteudo.midias or [])
            return UnifiedResponse(
                status="scheduled",
                platform=self.platform,
                message="Agendado com sucesso",
                external_id=result["id"],
                permalink=result.get("link"),
                extra={"when": result.get("when")}
            )
        except SimulatedAPIError as e:
            return UnifiedResponse(status="error", platform=self.platform, message=str(e))

    def obter_estatisticas(self, external_id: str) -> Estatisticas:
        try:
            metrics = self.api.stats(external_id)
            return Estatisticas(
                external_id=external_id,
                platform=self.platform,
                likes=metrics["likes"],
                comments=metrics["comments"],
                shares=metrics["shares"],
                views=metrics["views"],
            )
        except SimulatedAPIError as e:
            # Em um caso real, poderíamos lançar ou retornar um objeto com erro; aqui simplificamos:
            return Estatisticas(external_id=external_id, platform=self.platform)
