
from datetime import datetime, timedelta
from src.social_adapter.models import Conteudo
from src.social_adapter.manager import GerenciadorMidiaSocial
from src.social_adapter.config import ConfigLoader
from src.social_adapter.factory import SocialMediaFactory
from src.social_adapter.strategy import ImmediateStrategy, QueuedScheduleStrategy

def bootstrap_manager() -> GerenciadorMidiaSocial:
    cfg = ConfigLoader().load()
    adapters = SocialMediaFactory().build(cfg)

    gm = GerenciadorMidiaSocial()
    for name, adapter in adapters.items():
        gm.registrar(name, adapter)
    return gm

def demo():
    gm = bootstrap_manager()
    conteudo = Conteudo(texto="Lançamento de campanha! #marketing", midias=["banner.png"])

    print("== Publicação imediata ==")
    strat = ImmediateStrategy()
    responses = strat.executar(conteudo, gm.adapters.values())
    for r in responses:
        print(r)

    print("\n== Agendamento para +1h ==")
    when = datetime.utcnow() + timedelta(hours=1)
    strat2 = QueuedScheduleStrategy(when=when)
    responses2 = strat2.executar(conteudo, gm.adapters.values())
    for r in responses2:
        print(r)

    # Estatísticas de um dos retornos de sucesso
    ok = next((r for r in responses if r.status == "success" and r.external_id), None)
    if ok and ok.external_id:
        stats = gm.estatisticas(ok.platform, ok.external_id)
        print("\n== Estatísticas ==")
        print(stats)

if __name__ == "__main__":
    demo()
