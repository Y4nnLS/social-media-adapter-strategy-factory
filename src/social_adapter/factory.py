
from __future__ import annotations
from typing import Dict
from .adapters.base import SocialMediaAdapter
from .adapters.twitter import TwitterAPI, TwitterAdapter
from .adapters.instagram import InstagramAPI, InstagramAdapter
from .adapters.linkedin import LinkedInAPI, LinkedInAdapter
from .adapters.tiktok import TikTokAPI, TikTokAdapter


class SocialMediaFactory:
    """Instancia adapters com base na configuração."""

    def build(self, cfg: dict) -> Dict[str, SocialMediaAdapter]:
        adapters: Dict[str, SocialMediaAdapter] = {}

        def maybe(platform_key: str, api_cls, adapter_cls):
            p = cfg.get(platform_key, {})
            enabled = bool(p.get("enabled", False))
            if not enabled:
                return
            api = api_cls(api_key=p.get("api_key", ""), api_secret=p.get("api_secret", ""), enabled=enabled)
            adapters[platform_key] = adapter_cls(api)

        maybe("twitter", TwitterAPI, TwitterAdapter)
        maybe("instagram", InstagramAPI, InstagramAdapter)
        maybe("linkedin", LinkedInAPI, LinkedInAdapter)
        maybe("tiktok", TikTokAPI, TikTokAdapter)
        return adapters
