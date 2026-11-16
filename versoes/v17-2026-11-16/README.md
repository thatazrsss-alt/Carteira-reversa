# Carteira Reversa | v17 — 16/11/2026

**Status:** protótipo operacional validado com testes sintéticos, **não homologado contra arquivos reais**.

## Como executar

- Baixe esta pasta e dê dois cliques em `INICIAR_CARTEIRA_REVERSA.bat` no Windows com Python 3 instalado.
- Alternativa: `python iniciar_carteira.py` ou abra o HTML diretamente no navegador.
- Carregue a Order e BASE_ESTOQUE.xlsx (Excel, CSV, ZIP); selecione as redes; revise canais VD/CD; exporte Excel e PNG individuais.
- Bibliotecas JavaScript XLSX e ZIP carregam por CDN; a primeira abertura requer acesso à internet. O processamento das bases ocorre no navegador.
- [Design Canva](https://canva.link/5heiji15tubdz3d).

## Regras v17

**Original (U/V/W):** uma linha por `EG Cliente + SKU EG + Pedido ERP`; referência para entrada inicial em HL/PLT/CX. Menor criação e, em empate, menor vencimento; sem data, primeira ocorrência com alerta.

**Pendente:** calcular **por linha** `Qtd. Atualizada − Carro com Remessa − Carro sem Remessa − Faturado` e **somar os saldos calculados de todas as linhas por chave**. Faturado e movimentos somados; não se aplica deduplicação de linhas à parte do pendente. Exibição em caixas, com conversão por CAD quando a unidade da linha for explicitamente PLT. Na ausência de unidade, o padrão da Order é interpretado como CX e precisa de homologação com os dados reais.

**VD:** código EG → CAD → SAP somente para Malha e comercial; estoque D1 em PLT na origem autorizada, convertido em CX pelo fator da CAD; alternativas por fábrica e prioridade maior estoque/próximo de 26 PLT. Qualificação VD = sem estoque/ muito crítico <20 / crítico 20–<50 / intermediário 50–100 / OK >100.

**CD:** lojas → DPAR → CDD correspondente pelo título da grade e códigos de centro internos, SKU grade = EG sem último dígito, saldo em CX; sem faixas de criticidade. Produção CD somente se vinculada ao mesmo SKU/CDD e apresentada separadamente como informativa quando não houver previsão temporal.

**Rede mista:** consolidar por `Rede + Pedido ERP + EG Cliente + Canal`; lojas Shibata CD por padrão e CD Shibata VD. Não pressupõe que um mesmo pedido esteja nos dois canais.

**Relatórios:** HTML com KPIs e aberturas por rede/pedido/SKU/origem, Excel por rede com resumo, pedidos, itens, origens VD e Order original filtrada, PNG por rede para corpo de email.

## Histórico e validação

- Original `analise-carteira-reversa (15).zip` mantido sem alterações na raiz do repositório.
- v16: layout adotado a partir de Canva, Malha SAP e D1.
- v17: separar original único de pendente somado, incluir por EG Cliente/canal e produção CD vinculada, otimização para grande volume, pacote de execução.
- Sintaxe JS e navegador Chromium com dados sintéticos verificados: entradas repetidas 120 CX, saldos somados 85 CX, faturado 15 CX; canal CD de loja separado do VD do CD Shibata.
- A análise com arquivos reais e as regras de produção CD ainda aguardam homologação.
