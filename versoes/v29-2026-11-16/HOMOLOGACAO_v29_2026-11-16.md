# Parecer de homologação — Carteira Reversa v29
**Data:** 16/11/2026  
**Artefato auditado:** [HTML v29](Carteira_Reversa_Gerencial_v29_Conciliacao_Formacao_Origem.html)  
**SHA GitHub do arquivo validado:** `8b5964a0a249b68b852fceb5bd606836a9e96fff`  
**Escopo:** motor de pedidos, marcados, faturados, pendente, fill rate, CAD, Malha, estoque VD/CD, produção e potencial de 24 PLT.

## Resultado

**HOMOLOGAÇÃO TÉCNICA CONDICIONAL: APROVADA NOS TESTES CONTROLADOS.**  
**HOMOLOGAÇÃO OPERACIONAL DOS VALORES REAIS: PENDENTE / NÃO APROVADA.**

Nenhuma base Order operacional real foi localizada nos arquivos acessíveis desta execução. O arquivo **BASE_ESTOQUE 16.11.xlsx**, de 4.469.103 bytes, foi identificado no GitHub do projeto, mas seus bytes XLSX não puderam ser transferidos/lidos pelo acesso disponível nesta sessão (o acesso textual ao blob binário falhou). Portanto, **não foram auditados os volumes reais, pedidos reais, saldos reais, fill rates reais nem os cruzamentos efetivos dessa planilha**. Não substituir a base real por demo e não divulgar dados de cliente no repositório.

## Testes realizados no código

| ID | Regra/critério de teste | Evidência observada | Situação |
|---|---|---|---|
| H01 | Original único por Pedido ERP + EG Cliente + SKU EG | Exemplo com duas linhas: original = 100 CX, não 200 | Passou |
| H02 | Somar movimentos sem duplicar original | 100 + 50 CX atualizadas; marcado 5+15=20, faturado 10+20=30, pendente = (100−5−0−10)+(50−15−0−20)=100 CX | Passou |
| H03 | Fill rate exclusivamente faturado/original | Exemplo 30/100 = 30%; não inclui Marcado | Passou |
| H04 | Marcado e Carro com Remessa não se somam | Colunas simultâneas 30/40 disparam 1 conflito; marcado operacional calculado como 30, não 70 | Passou |
| H05 | Saldo por movimento | 100 atualizado −30 marcado−0 sem remessa−20 faturado = 50 CX | Passou |
| H06 | Origem/saldo de carro VD | Dois SKUs somam 25 PLT qualificados na **mesma origem** → 1 carro potencial de 24 PLT | Passou |
| H07 | Mesmo SKU consumindo D1 em vários pedidos | Dois pedidos de 15 PLT de um SKU com D1 20 PLT → potencial máximo de 20 PLT, sem duplicar estoque | Passou |
| H08 | Origem alternativa | SKU simultaneamente elegível em 892-VD e 952-VD aparece marcado como alternativo; não somar as origens | Passou |
| H09 | D1 zero | 0 PLT qualificado e 0 carro potencial | Passou |
| H10 | Carro sem remessa não é entrega comprovada | Atualizada 100, marcado 1, sem remessa 99, faturado 0, pendente 0 → **não** classifica como atendido | Falhou na versão inicial; corrigido e retestado |
| H11 | EG→SAP obrigatoriamente pela CAD | SKU EG da Order precisa existir na CAD; SAP da Order sozinho não faz o SKU cruzar outro produto | Corrigido e retestado |
| H12 | EG com zeros à esquerda | EG 111 encontra CAD 000111 por normalização numérica quando aplicável | Corrigido e retestado |
| H13 | Pendente informado independentemente pela Order | Calculado 50 vs informado 50 → delta 0 CX | Passou |
| H14 | Divergência calculado vs informado | Calculado 50 vs informado 60 → delta −10 CX com alerta | Passou |
| H15 | Campo Pendente inexistente na origem | Saldo fonte = N/D, não estimar nem reportar como 0 | Passou |
| H16 | Scripts JavaScript do painel | Compilação sintática dos scripts principais da versão final, sem erro | Passou |

Os testes foram executados com **fixtures controladas e inspeção do código real da v29**, não com movimentações reais. Não constituem teste de navegador integral, auditoria de todas as interações nem aprovação de resultados operacionais.

## Correções materiais efetuadas na v29 durante a revisão

1. **Original por cabeçalho**, eliminando fallback em letras/posições fixas da planilha.
2. **Faturado estrito**: não substitui automaticamente quantidade atendida, evitando distorção no fill rate.
3. **Marcado = Carro com Remessa**: usa uma só medida; alerta se os dois campos coexistem com valores diferentes.
4. **Possível sobreposição Marcado/Faturado**: sinaliza casos extremos sem alterar silenciosamente a fórmula. A inexistência do alerta não prova exclusividade das movimentações.
5. **CAD**: bloqueia fatores de conversão divergentes; EG→SAP da Malha só ocorre após identificação do SKU EG na CAD.
6. **Estoque VD/CD**: a qualificação considera D1 PLT por fábrica no VD e caixas na grade do CDD para CD; a produção não incrementa o estoque disponível.
7. **Itens atendidos**: diferencia atendido, parcialmente atendido e saldo zerado sem comprovação; carro sem remessa impede reconhecimento de atendimento integral.
8. **Formação VD**: limita D1 por SKU na mesma origem, distingue centros alternativos e calcula carros inteiros de 24 PLT sem somar fábricas.
9. **Conciliação interna independente**: compara pendente calculado com o **Pendente informado na Order** quando essa coluna existir; não usa apenas a identidade algébrica da própria fórmula como prova de correção.

## Regras de negócio e riscos ainda não homologados

| Pendência | Consequência | Evidência necessária |
|---|---|---|
| Order real indisponível | Impossível bater Original, Marcado, Faturado, Pendente e Fill Rate por pedido e rede | XLSX/CSV real da Order com cabeçalhos/movimentos |
| Estoque real indisponível ao processamento nesta sessão | Impossível validar CAD, Malha, D1, DPAR, Grade, produção e nomes das origens contra os registros reais | XLSX BASE_ESTOQUE 16.11 ou versão vigente |
| Semântica temporal de Marcado e Faturado | Se registros são snapshots acumulados, pode haver dupla dedução mesmo quando Marcado + Faturado <= Atualizada | Identificador do movimento, data e definições do ERP |
| D1 compartilhado entre pedidos e origens alternativas | Potencial por fábrica não equivale a reserva nem a programação garantida | Regras de alocação e compromisso de estoque |
| Atualização/validade/captação | Filtro de validade é inclusivo (>= data); captação usa criação mais antiga; impacto real não medido | Datas de criação e vencimento da Order real |
| Estado da interface e exportações com volumes reais | Não há aprovação visual/funcional end-to-end do navegador após o carregamento real | Importação da Order e estoque e confronto de Excel externo/interno |

**Sobre “a conta não fecha”:** a diferença `Original − Faturado − Pendente` não é necessariamente erro, pois a entrada original é uma quantidade única por chave e os movimentos são somados por linha. O controle útil é separar: (a) correspondência entre Pendente calculado e Pendente informado na fonte; (b) coerência dos eventos sem dupla dedução; (c) amarração de SKU / centro / unidades. A identidade `Atualizada − Marcado − Sem Remessa − Faturado − PendenteCalculado = 0`, por usar o mesmo pendente derivado, **não constitui prova independente**.

## Critério para homologação final

Aprovar somente após os dados reais passarem por: reconhecimento das abas/cabeçalhos sem ambiguidades; contagem por chave; conferência de marcado e faturado sem sobreposição; confronto do Pendente informado contra o calculado com divergências justificadas; CAD/EG/SAP e Malha por Comercial; estoques VD em PLT e CD em CX com unidades preservadas; produção como data; apuração independente das origens e carros de 24 PLT; resultados das exportações iguais ao recorte do painel; e checagem de segurança de envio somente da rede de destino.

**Conclusão:** motor técnico revisado e verificações controladas aprovadas; **não afirmar homologação operacional completa até receber e processar as bases reais**.
