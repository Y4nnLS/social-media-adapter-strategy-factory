
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List


@dataclass(frozen=True)
class Conteudo:
    texto: str
    midias: Optional[List[str]] = None  # caminhos de arquivos (simulados)
    tags: Optional[List[str]] = None


@dataclass(frozen=True)
class Publicacao:
    platform: str
    external_id: str
    permalink: Optional[str] = None
    when: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class Estatisticas:
    external_id: str
    platform: str
    likes: int = 0
    comments: int = 0
    shares: int = 0
    views: int = 0
    extra: Dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class UnifiedResponse:
    status: str  # "success" | "scheduled" | "error"
    platform: str
    message: str
    external_id: Optional[str] = None
    permalink: Optional[str] = None
    extra: Dict[str, object] = field(default_factory=dict)
