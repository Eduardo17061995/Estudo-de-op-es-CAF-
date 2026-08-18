# Estudo de opções e futuros de café — hedge para cliente comprador/estocador

Estudo de proteção de preço para cliente que **compra café, carrega estoque e revende**
(posição comprada no físico). Operação via **XP Investimentos**, com contrato futuro de café
arábica **ICF** e opções sobre ICF na **B3**.

## Onde começar

1. **[`ESTUDO_HEDGE_CAFE.md`](ESTUDO_HEDGE_CAFE.md)** — o estudo. Leia primeiro.
2. **`saida/Estudo_Hedge_Cafe_ICF.xlsx`** — a calculadora. Preencha só as células
   azuis com fundo amarelo, na aba `Parametros`.

## Os dois achados que mudam a recomendação padrão

**1. O mercado está invertido.** Nos preços de referência (03/08/2026), o ICF Set/26 está em
US$ 391,60 e o Dez/26 em US$ 368,40 — o mercado paga **menos** pelo café futuro. Vender futuro
no vencimento longo carimba um desconto de ~R$ 120/saca, e ainda se paga armazenagem por cima.
A resposta reflexa ("vende futuro e pronto") está errada neste momento de mercado.

**2. A put seca não cabe na margem do cliente.** Com vol implícita de ~38% a.a., a put no
dinheiro custa **R$ 162/saca** contra uma margem comercial de **R$ 110/saca** — 148% do lucro.
O collar (put comprada + call vendida) custa **R$ 23/saca**, 21% da margem, e é a única
estrutura de opção que fecha a conta.

**3. Nenhuma put seca resolve o problema dele.** O negócio dele já empata com uma queda de 5,7%
(ICF US$ 347,31), mas as puts baratas só se pagam depois de quedas de 12% a 15% — ele paga o
seguro e leva o prejuízo. As que protegem a margem custam 176% a 207% dela.

**Leitura do estudo:** **collar put 350 / call 385** — entra com crédito de R$ 10,32/saca,
garante margem positiva de +R$ 24,32/saca no pior caso e preserva alta até R$ 206,32/saca.
Condicionado a duas confirmações: liquidez real nas opções de ICF (fina na B3) e o skew de
volatilidade da tela, já que o crédito é calculado sob hipótese de vol plana.

**E antes de tudo:** girar o estoque em 1 mês em vez de 3 vale **R$ 164,64/saca** — mais que a
margem inteira do vencimento longo, e 7x o custo do melhor collar. A escolha do vencimento pesa
mais que a escolha da estrutura.

## Estrutura

```
ESTUDO_HEDGE_CAFE.md              o estudo completo
saida/Estudo_Hedge_Cafe_ICF.xlsx  calculadora, 8 abas
modelo/gerar_calculadora_cafe.py  gera a planilha do zero
modelo/validar_modelo.py          valida a matemática do modelo
modelo/analise_breakeven.py       qual strike vale a pena e a partir de quanto paga
```

Abas da planilha: `Leia-me` · `Parametros` · `Dimensionamento` · `Cenarios` · `Opcoes` ·
`Estruturas` · `Programa de hedge` · `Breakeven opcoes`

## Rodar

```bash
pip install openpyxl
python modelo/gerar_calculadora_cafe.py   # regera a planilha
python modelo/validar_modelo.py           # valida (todas as verificações passam)
python modelo/analise_breakeven.py        # tabelas de breakeven de puts e collars
```

## Avisos

- Os preços são **exemplos datados de agosto/2026**. Atualize na tela da XP antes de operar.
- Os prêmios de opção são **teóricos** (Black-76). O prêmio real é o da tela/mesa — a liquidez
  de opções de café na B3 é baixa e o spread pode ser largo.
- Margem, corretagem e emolumentos precisam ser **confirmados com a XP**.
- O ICF é cotado em **US$/saca**: existe risco cambial além do risco de café.
- Documento de estudo técnico. **Não é recomendação de investimento.**
