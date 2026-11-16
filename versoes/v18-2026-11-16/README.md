# Carteira Reversa — v18 (16/11/2026)

## Uso
- Execute `INICIAR_CARTEIRA_REVERSA.bat` no Windows (Python 3) ou `python iniciar_carteira.py`, ambos na pasta desta versão. Também é possível abrir o HTML diretamente.
- Faça upload da Order e da BASE_ESTOQUE em `.xlsx`, `.csv` ou `.zip`; escolha as redes e configure VD/CD em lote e as exceções por loja. Não é preciso renomear arquivos ou cadastrar o de/para de centros.
- O painel e os arquivos são gerados no navegador. Os leitores XLSX e ZIP dependem das bibliotecas JS de CDN (internet necessária para carregá-las). **Não publica dados de clientes no GitHub**.

## Alterações em relação à v17
1. **Fill rate limitado a 100%** em todas as visões, Excel e PNG: `max(0, min(100, 100*faturado/inicial))`. Quando faturado excede o original, registra `Excesso faturado CX` na aba Conciliação e alerta por item, sem diminuir o faturado bruto nem corrigir automaticamente o saldo.
2. **SKU PCA = SKU EG**. A fábrica utiliza `Sku PCA` como preferência (e `Sku S4` como alternativa quando necessário); na produção `COD_PROD` é SKU EG. **Somente a Malha usa SAP** depois do de/para na CAD (`Cod S4_2` → `Cod_SAP`).
3. **PRODUÇÃO é data prevista**, não quantidade. Lê `PRODUÇÃO` como data em `ORIGEM + COD_PROD` e preserva `ESTOQUE` como campo distinto. Exibe data da mesma origem elegível VD ou mesmo CD/CDD. Sem quantidade futura informada, não soma previsão à cobertura.
4. **De/para fixo** com os 24 centros da regra fornecida, incluindo casos `BRDF` (424-VD / 475-CD) e `BR09` (893-VD / 902-CD). Na Malha lê o BR Origem; na Produção lê o nome da fábrica; ambos convergem para o mesmo centro, sem perguntar esse de/para no upload.
5. Estoque VD = **D1**, em PLT; comparação com pendente CX usa a CAD. Estoque CD = **SaldoDisponivel**, em CX, via DeParaCDD da loja e nome da aba da grade, sem criticidade VD.
6. Entrada original: apenas uma linha da chave `Pedido ERP + EG Cliente + SKU EG`, U/V/W. Pendente: soma de saldos calculados por linha e convertidos para CX. Fill rate/gerencial por pedido permanecem abertos por Rede + Pedido + EG Cliente + VD/CD.

## Testes e limites
- Sintaxe JavaScript validada e testes de navegador Chromium com sete abas fictícias com nomes de colunas reais: CAD, VD, Malha, Produção, Grade, DPAR, Order.
- Cenário controlado: pedido original 100 CX, faturado 125 CX => fill rate visível 100%, excesso 25 CX sinalizado; `Sku PCA` EG 1234567, Malha SAP-A, BR15 e Produção `F. Jundiai` resolvidos para 892-VD; estoque D1=48 PLT; `PRODUÇÃO=20/11/2026` interpretado como 20/11/2026, nunca 20 PLT.
- BRDF e BR09 separados por VD/CD testados. Teste de exportação com biblioteca XLSX simulada conferiu abas e estrutura, **não substitui homologação dos arquivos reais**.
- O conteúdo do ZIP original e as bases reais não foram validados linha a linha nesta execução. A versão é para homologação operacional antes de enviar relatórios externos.

## Material de layout
- [Referência Canva](https://canva.link/5heiji15tubdz3d).
- Histórico: manter a v17 em `versoes/v17-2026-11-16/` e publicar esta v18 em `versoes/v18-2026-11-16/` sem sobrescrever anteriores.