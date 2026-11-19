# Carteira Reversa v32 — conferência visual e orientação de envio

**Data:** 19/11/2026  
**Estado:** versão técnica para homologação; **NÃO homologada com as bases reais**.  
**Base preservada:** v31 (o arquivo original não foi sobrescrito).

## HTML principal
`Carteira_Reversa_Gerencial_v32_Conferencia_Visual.html`

Baixe pelo GitHub usando **Download raw file**, abra o HTML no Edge/Chrome e importe **Order.zip** e **BASE_ESTOQUE 16.11.xlsx** em **Bases e redes**, no mesmo recorte de atualização. Não abra o conteúdo HTML como visualização do GitHub; use o arquivo local no navegador.

## Ajustes desenvolvidos
1. **Order / cancelamento:** linhas explicitamente marcadas com status/situação cancelada, ou data de cancelamento preenchida, são excluídas **antes** da consolidação de movimentos. Elas aparecem em auditoria própria com Pedido ERP, Cliente EG, SKU, arquivo/aba/linha quando identificáveis. Status ausente não é presumido como cancelamento.
2. **Conciliação por chave:** a investigação localiza Pedido ERP + Cliente EG + SKU, e exibe Original, Atualizada, Marcado/Carro com Remessa (um único movimento), Faturado, Carro sem Remessa, Pendente calculado e Pendente informado na fonte. Divergências e chaves ASCD/ASVD mistas são alertadas, não forçadas a fechar.
3. **Validade:** Vencidos, Hoje–3, 4–7, 8–14, 15–21, 22–30, >30 e Sem validade.
4. **Nomes de produtos:** exibe SKU EG + descrição quando presente na Order ou em de/para confiável (CAD/Produto). Se nome faltar, declara que a descrição não foi localizada; não inventa produto.
5. **Qualificação VD / CD:** detalhe por Pedido, SKU, nome, Cliente EG, origem, D1 físico VD em PLT, Grade CD em CX, necessidade, volume alocado/coberto e residual/não coberto. Estoque D1 é informativo/fixo e não é descontado sucessivamente por pedido.
6. **Complemento VD:** agrupa residual qualificado por Cliente EG + origem e lista SKUs e pedidos; indica diferença até 24 PLT e carros já formados na origem. Não mistura origens para completar carro.
7. **Envio:** passo a passo por rede/EG, validade, Excel do cliente, relatório PDF via impressão e rascunho de e-mail. Assunto usa **Carteira Reversa - Nome do cliente - Data de validade**.

## Testes técnicos feitos
- O arquivo v32 foi criado em novo caminho do repositório.
- Sintaxe JavaScript verificada em todos os **9 blocos `<script>`**: sem erro sintático.
- Estrutura das novas áreas e botões verificada por leitura do HTML.

## Testes pendentes e limites
- A Order.zip, a base de estoque e o CSV de histórico reais não foram executados no navegador por esta revisão. Portanto, os saldos específicos da SONDA **4801420253 / 44099 e 50294** não foram homologados.
- Confirmar o campo exato de status/data de cancelamento na Order real para garantir cobertura de todas as ocorrências.
- Conferir se as duas linhas da SONDA apresentam os mesmos componentes e unidades, distinguir Original de Atualizada e comparar o saldo informado pela fonte.
- Validar o zero de VD qualificado sem carga contra estoques por SKU/origem e carros propostos; a formação v31 continua podendo ser heurística para casos complexos.
- Exportar e **reabrir** os dois arquivos Excel para descartar corrupção, conferir detalhamento, unidades e totais.
- Imprimir PDF A4 horizontal e conferir que informações de auditoria/D1 interno não vazam para cliente.
- O HTML offline não envia e-mails e não anexa automaticamente ao Outlook. O botão abre o fluxo de preparação/rascunho, com anexo manual. Automação real dependeria de integração corporativa liberada.

**Não liberar envio comercial com divergências não investigadas.**
