# Carteira Reversa — Gerencial v26

## Execução
Abrir [Dashboard HTML v26](Carteira_Reversa_Gerencial_v26_Operacional_Notion.html) em um navegador. Importar a Order e a base de estoque vigente, `BASE_ESTOQUE 16.11.xlsx`. O botão do GitHub consulta o arquivo de estoque mais recente; a Order precisa ser fornecida separadamente.

## Regras incorporadas
- Original: uma linha por **Pedido ERP + EG Cliente + SKU EG**, U/V/W; captação = menor data de criação.
- Pendente: soma por linha de `Qtd Atualizada − Carro com remessa − Carro sem remessa − Faturado`, consolidada por chave. Célula vazia em campo existente é zero; cabeçalho ausente é falha de mapeamento.
- VD: CAD EG → SAP; Malha pelo SAP e Comercial; estoque D1 por origem autorizada em PLT, sem misturar fábricas.
- CD: DeParaCDD da loja, grade do CDD, `CodigoProduto` EG sem último dígito e `SaldoDisponivel` em CX.
- Produção: quatro colunas `ORIGEM | COD_PROD | NOME_PROD | PRODUÇÃO`; última coluna é **data de produção**.
- Agudos: `F. Agudos` corresponde a 893-VD; `CDD Agudos Int DC` corresponde a 902-CD.
- Shibata: CD Shibata (VD) e lojas Shibata (CD) separados por pedido, EG Cliente e fill rate.
- Qualificação de atendimento substitui faixas antigas de estoque; volumes D1 e saldo CD são restritos à visão interna.
- Busca e multisseleção de redes com seleção/limpeza de resultados.

## Testes
Validação sintática Node e testes de navegador Chromium com amostras representativas: original 100 CX, faturado 10 CX, pendente 170 CX por duas linhas; datas Agudos VD e CD; filtro de redes.

**Pendente:** homologar o motor com os arquivos operacionais reais completos, que não puderam ser extraídos do GitHub neste ambiente.

[Notion — Regras oficiais e pendências](https://app.notion.com/p/41a16626f20281d7ba6ef718c354a96f)
