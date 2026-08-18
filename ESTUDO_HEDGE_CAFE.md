# Estudo de hedge de café arábica — cliente comprador/estocador

**Operação via XP Investimentos · B3 (contrato ICF e opções sobre ICF)**
Data-base do estudo: agosto/2026

> Documento de estudo técnico para uso do assessor. Não é recomendação de investimento.
> Todo número de mercado aqui é **exemplo com data**; atualizar na tela da XP antes de operar.

---

## 1. O risco do cliente, dito com precisão

O cliente **compra café do produtor, carrega estoque e revende depois**. Isso o deixa
**comprado (long) no físico**. O risco dele é um só:

> **O preço cair entre o dia em que ele compra e o dia em que ele revende.**

Cada R$ 1,00 de queda por saca é R$ 1,00 de prejuízo por saca em estoque. Com 1.500 sacas
carregadas, uma queda de 15% no café (~R$ 290/saca ao câmbio de 5,20) tira cerca de
**R$ 435 mil** do resultado — sem ele ter errado nada comercialmente.

**Consequência direta:** o hedge dele é **VENDER futuro** (ou **COMPRAR PUT**). Nunca comprar
futuro. Isso parece óbvio, mas é o erro nº 1 de quem "compra e vende" e se confunde sobre qual
ponta está descoberta.

### O que se protege não é o volume anual

Ele movimenta até 5.000 sacas/ano, mas **não está exposto a 5.000 sacas ao mesmo tempo**.
O que corre risco é o **estoque médio carregado** — se ele gira em ~3 meses, algo como
1.200 a 1.500 sacas por vez.

Hedgear 5.000 sacas quando só 1.500 estão em estoque não é proteção: são 3.500 sacas de
**posição vendida a descoberto**. Se o café subir, o cliente perde dinheiro de verdade, no
caixa, sem nenhum estoque valorizando do outro lado. Essa confusão é o que transforma
"hedge" em prejuízo e queima a relação com o cliente.

**Regra dura: o hedge se dimensiona pelo estoque exposto, não pelo faturamento.**

---

## 2. O instrumento: contrato ICF da B3

| Item | Especificação |
|---|---|
| Código | **ICF** + mês + ano (ex.: ICFZ26) |
| Tamanho | **100 sacas de 60 kg** por contrato |
| Cotação | **US$ por saca de 60 kg** |
| Vencimentos | Março (H), Maio (K), Julho (N), Setembro (U), Dezembro (Z) |
| Vencimento | 6º dia útil anterior ao último dia do mês |
| Tick | US$ 0,05 |
| Negociação | 9h–14h35, com after market 15h30–18h |
| Margem | ~4,88% do nocional citado publicamente — **confirmar com a XP** |

Referências de preço (exemplo, 03/08/2026):

- **ICF Set/26: US$ 391,60/saca**
- **ICF Dez/26: US$ 368,40/saca**
- Café C em NY (17/08/2026): ~321 c/lb
- USD/BRL (17/08/2026): ~5,20

Para 1.500 sacas seriam 15 contratos: nocional ≈ **R$ 2,87 milhões**, margem inicial estimada
≈ **R$ 140 mil**. Na razão de hedge de 80% (12 contratos): nocional **R$ 2,30 milhões**,
margem **R$ 112 mil**. Cabe num cliente desse porte, mas exige caixa reservado — ver seção 6.3.

---

## 3. O achado mais importante: o mercado está invertido

Repare na relação entre os vencimentos:

```
ICF Set/26  US$ 391,60   ← vencimento CURTO, preço MAIOR
ICF Dez/26  US$ 368,40   ← vencimento LONGO, preço MENOR
                -23,20   → o mercado paga MENOS pelo café futuro
```

Isso é **mercado invertido (backwardation)**, e significa uma coisa muito concreta:

> **O mercado está pagando o cliente para NÃO carregar estoque.**

Em números, ao câmbio de 5,20:

| | R$/saca |
|---|---|
| O que o mercado "paga" para carregar de set a dez | **–R$ 120,64** (cobra) |
| O que custa ao cliente carregar 3 meses (R$ 22/mês) | **–R$ 66,00** |
| **Resultado de carregar e travar em Dez** | **–R$ 186,64/saca** |

Ou seja: **travar preço em Dez/26 hoje carimba um preço R$ 120/saca abaixo do vencimento
curto, e ainda por cima o cliente paga R$ 66 de armazenagem para ter esse direito.**

**Três implicações práticas:**

1. **Girar estoque rápido vale mais que travar preço longo.** Em mercado invertido, a
   melhor "proteção" muitas vezes é operacional: comprar e revender em janela curta.
2. **Se for hedgear com futuro, use o vencimento mais próximo do giro real do estoque.**
   Vender Dez para proteger estoque que sai em Setembro é trocar risco de preço por
   perda contábil garantida.
3. **Este é o cenário em que a PUT ganha da venda de futuro.** A put custa prêmio, mas não
   carimba o desconto da curva invertida. Ver seção 5.

**Isso muda o estudo:** a resposta padrão ("vende futuro e pronto") está errada para
este cliente neste momento de mercado. Confira a curva na tela da XP no dia — se ela tiver
normalizado (Dez acima de Set), a conclusão inverte.

---

## 4. Dimensionamento — como calcular os contratos

```
Sacas a proteger  = estoque exposto  ×  razão de hedge
Contratos         = sacas a proteger ÷ 100   (arredondar)
```

Exemplo com os parâmetros do estudo:

| | |
|---|---|
| Estoque exposto | 1.500 sacas |
| Razão de hedge | 80% |
| Sacas alvo | 1.200 sacas |
| **Contratos a vender** | **12 contratos** |
| Cobertura efetiva | 80,0% |
| Sensibilidade residual | **–R$ 1.560** por US$ 1/saca de queda (ainda perde, nos 20% descobertos) |
| Redução de risco medida | **80,0%** da oscilação de resultado eliminada |

**Por que 80% e não 100%?** Três motivos, e vale dizer isso ao cliente:

- O contrato é indivisível (100 sacas), então 100% raramente é alcançável de forma exata.
- O basis (seção 6) faz o hedge nunca ser perfeito — hedge de 100% dá falsa sensação de zero risco.
- Deixar 20% livre preserva algum upside, o que ajuda o cliente a **sustentar a política**
  quando o café subir. Hedge de 100% que o cliente desmonta na primeira alta é pior que
  hedge de 70% que ele mantém.

---

## 5. As quatro estruturas — e o que cada uma custa de verdade

Esta é a resposta à sua pergunta sobre opções. Não existe "a melhor": existe o que o cliente
está disposto a pagar e a abrir mão.

### A) Não fazer nada
- Custo: zero. Upside: todo. Piso: **nenhum**.
- Serve para: cliente com caixa forte, giro muito rápido e tolerância real a prejuízo.

### B) Vender futuro ICF
- **Custo: zero de prêmio** (só corretagem/emolumentos).
- **Trava o preço nos dois sentidos.** Se o café subir 30%, o ganho do estoque é anulado.
- **Consome margem, e chama margem quando o café SOBE.** Ponto crítico: o estoque vale mais,
  mas o caixa aperta antes de o estoque ser vendido — descasamento clássico de fluxo.
- Hoje, com a **curva invertida**, ainda carimba o desconto do vencimento longo.

### C) Comprar PUT sobre futuro de ICF
- **Custo: prêmio pago, à vista.** É um seguro: o cliente paga e pronto.
- **Piso de preço garantido, upside preservado.** Se o café subir, ele perde só o prêmio.
- **Não consome margem de garantia e não gera chamada de margem.** Para um cerealista de
  porte médio isso é frequentemente mais valioso que o prêmio economizado.
- Prêmio teórico calculado (Black-76, vol 38%, 3 meses, futuro US$ 368,40):
  - PUT no dinheiro (US$ 375): **US$ 31,22/saca = R$ 162,33/saca** — 8,5% do futuro
  - PUT 95% do futuro (US$ 350): **US$ 18,76/saca = R$ 97,57/saca** — 5,1% do futuro

### D) Collar (comprar PUT + vender CALL) — "fence"
- **Custo: prêmio líquido, muito menor que a put seca; às vezes zero ou até crédito.**
- Cria **piso e teto**: o cliente troca a alta acima do strike da call pelo financiamento do seguro.
- **Volta a consumir margem** (pela call vendida), mas muito menos que o futuro cheio.
- É, na prática, **a estrutura mais usada por quem carrega estoque físico** — porque quem
  carrega estoque não precisa de alta ilimitada, precisa de margem previsível.

### Resumo comparativo

| | A) Sem hedge | B) Futuro | C) PUT | D) Collar |
|---|---|---|---|---|
| Prêmio a pagar | — | — | Alto | Baixo/zero |
| Piso de preço | não | sim (fixo) | sim | sim |
| Preserva alta | total | não | sim | até o teto |
| Consome margem | não | **sim, alta** | **não** | sim, média |
| Chama margem se café subir | não | **sim** | não | sim |
| Sofre com curva invertida | não | **sim** | não | pouco |

---

## 5.1 O segundo achado: a opção custa mais que a margem do cliente

Esta é a conta que precisa ser feita antes de qualquer recomendação, e quase nunca é.
Com os parâmetros do estudo, a **margem comercial** do cliente é:

```
Preço de revenda    = US$ 368,40 × 5,20 + R$ 40 (basis)  =  R$ 1.955,68/saca
Custo de compra                                          = –R$ 1.780,00/saca
Carrego 3 meses (R$ 22 × 3)                              = –R$    66,00/saca
                                                            ──────────────────
MARGEM COMERCIAL                                         =  R$   109,68/saca
```

Agora compare com o que cada proteção custa:

| Estrutura | Custo (R$/saca) | % da margem comercial | Viável? |
|---|---|---|---|
| PUT no dinheiro (375) | **R$ 162,33** | **148%** | **Não.** O seguro custa mais que o lucro. |
| PUT 95% (350) | **R$ 97,57** | **89%** | **Não.** Sobra R$ 12/saca de margem. |
| **Collar 350/405** | **R$ 22,89** | **21%** | **Sim.** Único que cabe. |
| Futuro vendido | R$ 0 de prêmio | — | Cabe, mas ver seção 3 (curva invertida). |

**Conclusão dura:** com a volatilidade do café em ~38% a.a., **comprar put seca é
economicamente inviável para este cliente.** O prêmio consome a margem inteira. Quem vende
put seca a um cerealista com margem de R$ 110/saca não está protegendo — está transferindo o
lucro dele para o vendedor da opção.

Isso não é opinião: é a razão pela qual **quem carrega estoque físico usa collar, não put
seca.** Quem carrega estoque não precisa de alta ilimitada; precisa de margem previsível.
E o teto da call é exatamente o que ele pode vender sem perder nada de essencial.

> **Atenção — os dois números que mudam essa conta:** se a margem comercial real do cliente
> for muito maior que R$ 110/saca (basis melhor, carrego menor, compra mais barata), a put
> seca volta ao jogo. E se a vol implícita da tela estiver bem abaixo de 38%, o prêmio cai
> junto. **Por isso as seções 6.1 e 9 pedem os números reais dele antes de fechar a estrutura.**

### Sobre "prêmio médio de opção" — um alerta de leitura

A aba `Opcoes` mostra um **prêmio médio de R$ 356/saca** ao longo da grade de strikes.
**Não use esse número como custo do hedge.** A média inclui puts muito dentro do dinheiro
(strike US$ 535 sobre futuro de US$ 368), que são caras por serem quase todo valor
intrínseco — o cliente jamais compraria. O número que importa é o **prêmio do strike que ele
vai efetivamente comprar**, e a métrica útil de comparação é **prêmio como % do futuro**
(régua: acima de 6–8% para 3 meses, está caro).

---

### Minha leitura para este cliente, neste mercado

**Collar (put comprada + call vendida) na razão de 70–80%**, e não put seca nem futuro cheio.
Três motivos que se somam:

1. A **curva invertida** (seção 3) penaliza a venda de futuro no vencimento longo.
2. A **put seca não cabe na margem** do cliente (seção 5.1).
3. O collar consome pouca margem de garantia e pouco caixa.

**Ressalva séria:** essa recomendação depende de haver **liquidez real** nas opções de ICF —
ver seção 6.4. Se a tela não tiver oferta, o caminho vira futuro no vencimento curto,
ou estrutura via balcão com a mesa da XP. **Não prometa collar ao cliente antes de
confirmar oferta firme.**

---

## 5.2 Qual opção vale mais a pena, e a partir de quanto ela paga

### O número que manda em tudo: o negócio dele já empata a –5,7%

Antes de escolher strike, essa conta:

```
ICF que zera a margem = (custo de compra + carrego − basis de venda) ÷ câmbio
                      = (1.846,00 − 40,00) ÷ 5,20
                      = US$ 347,31/saca
```

**O ICF está em US$ 368,40. Uma queda de apenas 5,7% já zera o lucro dele.**
É esse o intervalo do qual ele precisa se proteger — e é por isso que os strikes bem fora do
dinheiro (a proteção "barata") não servem: eles só começam a pagar quando o prejuízo já está feito.

### PUTs — o que cada strike entrega

| Strike | % do F | Prêmio | % da margem | Paga abaixo de | Breakeven | Queda até o breakeven | **Piso de margem** |
|---|---|---|---|---|---|---|---|
| US$ 320 | 87% | R$ 44,57 | 41% | US$ 320 | US$ 311,43 | **–15,5%** | –R$ 186,57 |
| US$ 330 | 90% | R$ 59,30 | 54% | US$ 330 | US$ 318,60 | –13,5% | –R$ 149,30 |
| US$ 340 | 92% | R$ 76,93 | 70% | US$ 340 | US$ 325,21 | –11,7% | –R$ 114,93 |
| US$ 350 | 95% | R$ 97,57 | 89% | US$ 350 | US$ 331,24 | –10,1% | –R$ 83,57 |
| US$ 360 | 98% | R$ 121,24 | 111% | US$ 360 | US$ 336,69 | –8,6% | –R$ 55,24 |
| US$ 368 | 100% | R$ 143,44 | 131% | US$ 368 | US$ 340,82 | –7,5% | –R$ 33,76 |
| US$ 385 | 105% | R$ 193,28 | 176% | US$ 385 | US$ 347,83 | –5,6% | +R$ 2,72 |

**O veredito é duro e vale ler com atenção:** **nenhuma put seca resolve o problema dele.**

- As baratas (320–340) só começam a se pagar depois de quedas de 12% a 15% — mas o lucro dele
  já morreu a 5,7%. **Ele paga o seguro e ainda leva o prejuízo.**
- As que realmente protegem a margem (385+) custam **176% a 207% da margem**. Comprar é destruir
  o lucro para proteger o lucro.
- O único strike com **piso positivo** é o 385, e ele garante… **+R$ 2,72/saca**. Ou seja: ele
  paga R$ 193/saca para garantir R$ 2,72/saca de lucro.

**Put seca está fora.** Não é questão de escolher o strike certo — a estrutura não serve para
uma margem de R$ 110/saca.

### COLLARS — aqui a conta fecha

| Put | Call | Custo líquido | % da margem | Breakeven | **PISO** | **TETO** | Veredito |
|---|---|---|---|---|---|---|---|
| **350** | **385** | **–R$ 10,32** (crédito) | **–9%** | US$ 351,98 | **+R$ 24,32** | R$ 206,32 | **Melhor relação** |
| 350 | 395 | R$ 7,51 | 7% | US$ 348,56 | +R$ 6,49 | R$ 240,49 | Quase zero custo, teto maior |
| 350 | 405 | R$ 22,89 | 21% | US$ 345,60 | –R$ 8,89 | R$ 277,11 | Mais upside, piso negativo |
| 360 | 395 | R$ 31,18 | 28% | US$ 354,00 | **+R$ 34,82** | R$ 216,82 | **Melhor piso** |
| 368 | 405 | R$ 68,76 | 63% | US$ 355,18 | **+R$ 40,92** | R$ 231,24 | Piso máximo, mas caro |

**As duas respostas à tua pergunta:**

**1. A mais vantajosa é o collar put 350 / call 385.** Ele **entra com crédito de R$ 10,32/saca**
(a call vendida paga mais que a put custa), garante **margem positiva de +R$ 24,32/saca** no pior
cenário possível, e ainda preserva alta até **R$ 206,32/saca**. É o clássico *zero-cost collar*,
aqui até melhor que zero. Se o cliente quiser piso mais alto, o **360/395** sobe o piso para
+R$ 34,82/saca ao custo de R$ 31,18.

**2. "A partir de quanto ele começa a ganhar" tem três respostas diferentes** — e a confusão
entre elas é o que gera briga com cliente depois. Para o collar 350/385:

| Pergunta | Resposta |
|---|---|
| A partir de quando a **put começa a pagar**? | ICF abaixo de **US$ 350** (–5,0%) |
| A partir de quando a **estrutura se paga**? | ICF abaixo de **US$ 351,98** (–4,5%) — porque entrou com crédito, ela já está paga desde o dia zero |
| Qual o **pior resultado possível** dele? | **+R$ 24,32/saca** de margem, aconteça o que acontecer |
| A partir de quando ele **para de ganhar mais**? | ICF acima de **US$ 385** (+4,5%), onde a call limita em R$ 206,32/saca |

**O que isso significa na prática:** sem hedge, uma queda de 35% leva a margem dele para
**–R$ 560,81/saca**. Com o collar 350/385, o pior caso é **+R$ 24,32/saca**. Em 1.500 sacas,
isso é **R$ 877 mil de prejuízo evitado** no cenário ruim — em troca de abrir mão do que
estivesse acima de R$ 206/saca no cenário bom.

### Ressalva séria: o crédito depende de uma hipótese que preciso que você confira

O modelo usa **uma volatilidade única de 38% para todos os strikes** (vol plana). O mercado real
tem **skew** — puts e calls fora do dinheiro negociam com vols diferentes. O crédito do collar
350/385 aparece porque, com vol plana, a call 385 está mais perto do dinheiro (16,6 pontos)
que a put 350 (18,4 pontos), então vale mais.

**Se na tela a put estiver com vol maior que a call, o crédito virá custo.** No café costuma
ocorrer o contrário (call com vol maior, por risco de quebra de safra), o que favoreceria ainda
mais o crédito — **mas isso tem que ser conferido, não presumido.** Peça à mesa da XP a vol de
cada strike, ou os prêmios de tela, e refaça a conta na aba `Breakeven opcoes`.
**Não prometa "collar de custo zero" ao cliente antes disso.**

---

## 5.3 E antes de tudo isso: a escolha do vencimento vale mais que a da estrutura

Este é o ponto que quase passou batido, e ele é maior que toda a discussão de opções:

| Vencimento | ICF | Carrego | Custo base | **Margem** | Em 1.500 sacas |
|---|---|---|---|---|---|
| **Set/26 (curto)** | US$ 391,60 | 1 mês (R$ 22) | R$ 1.802,00 | **R$ 274,32/saca** | **R$ 411.480** |
| Dez/26 (longo) | US$ 368,40 | 3 meses (R$ 66) | R$ 1.846,00 | R$ 109,68/saca | R$ 164.520 |
| | | | **Diferença** | **R$ 164,64/saca** | **R$ 246.960** |

**Girar o estoque em 1 mês em vez de 3 vale R$ 164,64/saca — mais que a margem inteira do
vencimento longo, e 7x o custo do melhor collar.** Vem de dois efeitos somados: a curva
invertida (Set paga US$ 23,20 mais que Dez) e dois meses menos de armazenagem.

**Ordem de prioridade, então:** (1) encurtar o ciclo comercial, (2) escolher o vencimento certo,
(3) só então escolher a estrutura de proteção. Otimizar o passo 3 antes dos passos 1 e 2 é
arrumar os móveis de uma casa com o telhado furado.

---

## 6. Os cinco riscos que o hedge NÃO elimina

Esta seção é a que separa um estudo honesto de uma apresentação de venda.

### 6.1 Basis — o risco que sobra sempre
O hedge protege o **preço da bolsa**. O cliente compra e vende **café físico, num local,
numa qualidade, num prazo**. A diferença entre os dois é o **basis**, e ele não é travado
pelo ICF. O ICF negocia **arábica tipo 4/5**; se o cliente opera outro tipo, bebida ou
região, o basis pode se mover contra ele mesmo com o hedge perfeito.

**Ação concreta:** pegue as notas fiscais reais dele dos últimos 12 meses, calcule
`preço praticado − ICF convertido em R$` na data de cada negócio, e meça a **dispersão**.
Se o basis oscila mais que o preço, o problema dele não é hedge de bolsa — é contrato comercial.
Sem esse número, o estudo fica no chute. **Peça a ele antes de fechar a política.**

### 6.2 Câmbio — o risco escondido
**O ICF é cotado em US$/saca. O cliente compra e vende em reais.** Ele tem, portanto, dois
riscos: café e dólar. Já vi hedge de café "funcionar" perfeitamente e o cliente perder
dinheiro porque o real valorizou.

A planilha separa "câmbio hoje" de "câmbio no vencimento" exatamente para você medir isso.
**Se o basis em reais do cliente for estável, considere hedge cambial (DOL/WDO) junto.**
Não incluí no escopo desta versão — vale uma conversa à parte.

### 6.3 Margem e fluxo de caixa
Futuro vendido **chama margem quando o café sobe**. O ajuste é diário e em dinheiro; o
estoque só vira caixa quando for vendido. Cliente que não reservou caixa é obrigado a
desmontar o hedge no pior momento possível — e aí fica com o prejuízo do hedge **e**
descoberto no físico.

A aba `Dimensionamento` calcula **quantos US$/saca de alta o colchão de caixa aguenta**.
Mostre esse número ao cliente antes de operar, não depois.

**E o número do exemplo é um alerta:** com colchão de 1,5x a margem inicial, o cliente aguenta
apenas **US$ 8,99/saca de alta — 2,4%**. Café com volatilidade de 38% a.a. faz 2,4% em um dia
ruim. Matematicamente, o colchão em % do nocional é `(multiplicador – 1) × % de margem`,
ou seja 0,5 × 4,88% = 2,44%. Para aguentar uma alta de 15% sem chamada, o multiplicador
precisaria ser de **cerca de 4x** a margem inicial.

**Por isso a planilha já vem com colchão de 3x**, o que sustenta ~9,8% de alta e exige
**R$ 337 mil** de caixa livre (contra R$ 168 mil no 1,5x). Para aguentar 15%, precisaria de ~4x.
Esse é o número que decide se o cliente pode ou não operar futuro — e é outro ponto a favor do
collar e da put: **opção comprada não chama margem.**

### 6.4 Liquidez das opções de café na B3 — atenção séria
As opções sobre futuro de ICF **existem** e foram criadas pela B3 justamente para gestão de
risco de produtor/indústria/trading, mas **a liquidez é fina**. Consequências reais:

- O prêmio de tela pode estar muito acima do teórico (spread largo).
- Pode não haver oferta no strike ou vencimento que você quer.
- Desmontar antes do vencimento pode ser difícil ou caro.

**Por isso os prêmios da planilha são TEÓRICOS.** Eles servem para você chegar na mesa
sabendo se o preço pedido é razoável — não para prometer preço ao cliente.

**Encaminhamento:** fale com a **mesa de agro/derivativos da XP** antes de desenhar a
estrutura final. Pergunte especificamente: (1) há oferta firme de put ICF nos vencimentos
H27/K27? (2) qual o spread? (3) a XP consegue estruturar via balcão/NDF se a tela não tiver
liquidez? (4) há acesso a opções de café C em NY (muito mais líquidas) para este cliente?

### 6.5 Risco de o cliente não aguentar a política
O mais subestimado. Hedge dói: em toda alta de preço, a posição de proteção mostra prejuízo
e o cliente liga perguntando por que você "apostou contra o café". Se a política não estiver
**escrita e assinada antes**, ela não sobrevive ao primeiro trimestre.

---

## 7. A resposta sobre "média de preço": trave em tranches

Você mencionou querer ver a média de preço. Essa é a parte mais valiosa do estudo, e não é
sobre média de prêmio de opção — é sobre **como travar**.

Travar 100% do hedge num único dia significa que **o acerto do estudo inteiro depende de um
preço de um dia**. Se travar no fundo, o cliente vai cobrar por 12 meses. A alternativa
profissional é um **programa de hedge em tranches**:

```
Divida o volume em 4 a 6 fatias
Defina os gatilhos ANTES  (preço alvo, data limite, ou margem mínima aceita)
Execute cada fatia quando o gatilho disparar
O resultado é um PREÇO MÉDIO travado
```

**O gatilho mais robusto não é preço — é margem.** Em vez de "travo se o ICF bater US$ 390",
use:

> "Travo sempre que o preço de bolsa garantir margem líquida de pelo menos
> **R$ X/saca** sobre custo de compra + carrego."

Assim o cliente para de tentar adivinhar o topo e passa a operar o próprio negócio.
A aba `Programa de hedge` calcula o preço médio ponderado das tranches e — mais importante —
a **margem travada por saca e em reais**. Se der negativo, a planilha está te dizendo que
o programa está carimbando prejuízo: não execute.

---

## 8. Política de hedge — o que colocar no papel com o cliente

Sugestão de política mínima, para assinar antes de operar:

1. **Objeto:** proteger o estoque de café adquirido e não vendido.
2. **Instrumento:** contratos ICF na B3 e/ou opções sobre ICF, via XP Investimentos.
3. **Base de cálculo:** estoque físico exposto (comprado e não revendido), medido semanalmente.
4. **Razão de hedge:** 70% a 80% do estoque exposto. Mínimo 50%, **máximo 100%**.
5. **Proibição expressa:** nenhuma posição vendida em derivativo pode exceder o estoque
   físico existente. Sem exceções, sem "aproveitar o mercado".
6. **Vencimento:** o mais próximo do giro real projetado do estoque.
7. **Gatilho de execução:** margem líquida mínima de R$ ___/saca sobre custo + carrego.
8. **Tranches:** 4 a 6 execuções, registradas na planilha com data, preço e volume.
9. **Caixa de margem:** manter 1,5x a margem inicial livre e não comprometida.
10. **Revisão:** mensal, com a planilha atualizada e o basis real remedido.
11. **Vedado:** operar volume acima do físico, day trade, ou alavancar a estrutura.

---

## 9. Próximos passos

**Com o cliente:**
- [ ] Estoque médio real carregado e prazo real de giro (substituir 1.500 sacas / 3 meses)
- [ ] Notas dos últimos 12 meses para calcular o **basis real** de compra e de venda
- [ ] Custo real de carrego (armazenagem, seguro, quebra, custo de capital)
- [ ] Caixa que ele consegue reservar para margem, sem apertar o capital de giro
- [ ] Tipo/bebida/região do café que ele opera (para medir aderência ao ICF 4/5)

**Com a XP:**
- [ ] Percentual de margem oficial para ICF na conta dele
- [ ] Corretagem e emolumentos por contrato (ICF e opções)
- [ ] **Liquidez real das opções ICF** — oferta firme, spread, vencimentos disponíveis
- [ ] Alternativa via balcão/estruturada se a tela não tiver liquidez
- [ ] Acesso a café C (ICE/NY) e a hedge cambial, se fizer sentido
- [ ] Cadastro de derivativos e limites operacionais aprovados

**Decisão a tomar depois desses dados:**
- Estrutura final: put seca vs collar vs futuro (a curva invertida hoje pesa contra o futuro)
- Incluir ou não hedge cambial
- Definir o número da margem mínima no gatilho

---

## Arquivos

| Arquivo | O que é |
|---|---|
| `saida/Estudo_Hedge_Cafe_ICF.xlsx` | Calculadora com 8 abas. Preencha só as células azuis/amarelas. |
| `modelo/gerar_calculadora_cafe.py` | Script que gera a planilha. Rode de novo para recriar do zero. |
| `modelo/validar_modelo.py` | Validação independente da matemática do modelo. |
| `modelo/analise_breakeven.py` | Análise de breakeven: qual strike vale a pena e a partir de quanto paga. |
| `ESTUDO_HEDGE_CAFE.md` | Este documento. |

Abas da planilha: `Leia-me` · `Parametros` · `Dimensionamento` · `Cenarios` · `Opcoes` ·
`Estruturas` · `Programa de hedge` · `Breakeven opcoes`

### Sobre a validação da planilha — leia antes de usar

O modelo foi validado por um script independente (`modelo/validar_modelo.py`), que replica em
Python a matemática de todas as 695 fórmulas e confere as identidades que precisam valer:
paridade put-call do Black-76, prêmios acima do valor intrínseco, redução de risco do hedge
igual à cobertura efetiva, ordenação dos payoffs das quatro estruturas, identidade do colchão
de margem, planicidade do piso da put e do piso/teto dos collars, breakeven da posição de
opção, e auditoria de que nenhuma fórmula aponta para célula vazia. **Todas as
verificações passam.**

**Uma limitação a declarar:** não foi possível rodar o recálculo automático via LibreOffice
neste ambiente — ele falha ao abrir arquivos .xlsx, inclusive um arquivo trivial de duas
células. **Consequência prática:** as fórmulas estão gravadas sem valores em cache, então
alguns visualizadores rápidos podem mostrar células em branco até você abrir o arquivo.
**Abra no Excel (ou no Google Sheets) uma vez e tudo calcula normalmente.** Evitei de
propósito funções pós-2007 e fórmulas matriciais, que são a causa usual de `#NAME?` nesses
casos — a auditoria confirma que nenhuma foi usada.

---

## Fontes das referências de mercado

- Especificações do contrato ICF — [B3](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/commodities/ficha-do-produto-8AA8D0CD95C8AFE30196115C00E925FC.htm), [Opere Futuros](https://www.operefuturos.com.br/contratos-futuros-bmf/contratos-futuros-especificacoes/cafe-arabica/), [ADVFN](https://br.advfn.com/investimentos/futuros/cafe)
- Opções sobre futuro de café arábica — [B3](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/commodities/ficha-do-produto-8AA8D0CD95C8AFE30196116387BC2ADE.htm)
- Preços ICF Set/26 e Dez/26 (03/08/2026) — [Cotação do Café](https://cotacaodocafe.com/cafe-arabica-na-bolsa/)
- Café C ICE (17/08/2026) — [Investing.com](https://www.investing.com/commodities/us-coffee-c)
- USD/BRL (17/08/2026) — [Investing.com](https://br.investing.com/currencies/usd-brl)
- Tarifas de café arábica — [B3](https://www.b3.com.br/pt_br/produtos-e-servicos/tarifas/listados-a-vista-e-derivativos/commodities/cafe/tarifas-de-cafe-arabica/)
