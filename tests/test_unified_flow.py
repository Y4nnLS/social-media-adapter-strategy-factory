
from datetime import datetime, timedelta
from src.social_adapter.models import Conteudo
from src.social_adapter.manager import GerenciadorMidiaSocial
from src.social_adapter.factory import SocialMediaFactory
from src.social_adapter.config import ConfigLoader

def setup_manager():
    cfg = ConfigLoader().load()
    adapters = SocialMediaFactory().build(cfg)
    gm = GerenciadorMidiaSocial()
    for name, adapter in adapters.items():
        gm.registrar(name, adapter)
    return gm

def test_publicar_e_agendar():
    gm = setup_manager()
    conteudo = Conteudo(texto="Teste", midias=None)

    resp = gm.publicar(conteudo, ["twitter", "instagram", "linkedin", "tiktok"])
    assert all(r.platform in gm.adapters for r in resp)
    assert any(r.status == "success" for r in resp)

    when = datetime.utcnow() + timedelta(minutes=30)
    resp2 = gm.agendar(conteudo, when, ["twitter", "instagram"])
    assert all(r.status == "scheduled" for r in resp2)

def test_stats_de_primeiro_success():
    gm = setup_manager()
    conteudo = Conteudo(texto="Teste2")
    resp = gm.publicar(conteudo, gm.adapters.keys())
    ok = next((r for r in resp if r.status == "success" and r.external_id), None)
    assert ok is not None
    stats = gm.estatisticas(ok.platform, ok.external_id)
    assert stats.likes >= 0
