
from __future__ import annotations
import os, yaml
from typing import Any, Dict


class ConfigLoader:
    def __init__(self, env_var: str = "APP_ENV", base_path: str = "config"):
        self.env = os.getenv(env_var, "dev")
        self.base_path = base_path

    def load(self) -> Dict[str, Any]:
        path = os.path.join(self.base_path, f"{self.env}.yaml")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo de config não encontrado: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data
