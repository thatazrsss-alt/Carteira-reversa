# Carteira Reversa — Projeto em andamento

Gerencial de atendimento por pedido/EG Cliente/SKU com canais VD e CD, consolidação de original e pendente, consulta CAD/Malha, estoques e produção.

## Versões e arquivos

- **[Homologação real BASE_ESTOQUE 16.11 — 17/11/2026](versoes/v29-2026-11-16/HOMOLOGACAO_ESTOQUE_REAL_2026-11-17.md)**: CAD x Malha x fábrica e grades CD conferidos diretamente no GitHub Actions; exceções e limitações documentadas. **Order operacional ainda não disponível para fechar pedidos.**

- **[v29 · 16/11/2026 · conciliação de Marcado/Faturado, cobertura e carros por origem](versoes/v29-2026-11-16/README.md)**: versão recomendada; [abrir painel HTML v29](versoes/v29-2026-11-16/Carteira_Reversa_Gerencial_v29_Conciliacao_Formacao_Origem.html). Validação sintática e cenários controlados aprovados; bases reais ainda precisam de homologação.
- **[v28 · 16/11/2026 · qualificação e formação por origem](versoes/v28-2026-11-16/README.md)**: referência anterior preservada.

- **[v18 · 16/11/2026 · produção como data, SKU PCA/EG, fill rate ≤100%](versoes/v18-2026-11-16/README.md)**: HTML, inicializador Python/BAT, de-para interno de 24 origens e Excel de conciliação; [abrir HTML](versoes/v18-2026-11-16/Carteira_Reversa_Gerencial_v18_Producao_Data_FillRate.html).
- **[v17 · 16/11/2026 · Canva + cálculo revisado](versoes/v17-2026-11-16/README.md)**: painel HTML, inicializador Python, arquivo BAT para Windows, regras e histórico. [Abrir HTML](versoes/v17-2026-11-16/Carteira_Reversa_Gerencial_v17_Canva_Motor.html)
- **[Pacote original v15](analise-carteira-reversa%20(15).zip)**: referência técnica preservada, não substituída.
- **[Base de estoque](BASE_ESTOQUE.xlsx)**: CAD, Malha, fábrica, CDDs, DPAR e produção. Não publicar bases de clientes ou pedidos sensíveis.
- **[Referência visual Canva](https://canva.link/5heiji15tubdz3d)**.

## Regras atuais

Entrada original: uma linha por chave EG Cliente + SKU EG + Pedido ERP (U/V/W). Saldo pendente: soma dos valores calculados individualmente em todas as linhas da chave, em caixas. VD: SAP somente na Malha, estoque fábrica D1 por EG/VD; CD: DPAR loja/centro e grade em caixas; produção somente como data/informação, sem somar ao saldo; visão por pedido separada por cliente e canal. A análise não reserva estoque.

**Status:** fontes e chaves de estoque real auditadas parcialmente e correções incorporadas à v29; não homologado por pedido sem a Order operacional real.

## Próximas versões

Criar uma nova pasta em `versoes/vXX-AAAA-MM-DD/` para registrar alterações sem apagar entregas anteriores.
