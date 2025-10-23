
# Diagramas

## Pacotes / Fluxo

```mermaid
flowchart LR
  A[Conteudo] --> B[GerenciadorMidiaSocial]
  B -->|publicar/agendar| C1[TwitterAdapter]
  B --> C2[InstagramAdapter]
  B --> C3[LinkedInAdapter]
  B --> C4[TikTokAdapter]
  C1 --> D1[API Simulada]
  C2 --> D2[API Simulada]
  C3 --> D3[API Simulada]
  C4 --> D4[API Simulada]
  B -->|Strategy| S[Immediate/Queued]
  C1 --> R1[UnifiedResponse]
  C2 --> R2[UnifiedResponse]
  C3 --> R3[UnifiedResponse]
  C4 --> R4[UnifiedResponse]
```

## Classe `UnifiedResponse`

```mermaid
classDiagram
class UnifiedResponse {{
  +status: string
  +platform: string
  +message: string
  +external_id: string?
  +permalink: string?
  +extra: dict
}}
```
