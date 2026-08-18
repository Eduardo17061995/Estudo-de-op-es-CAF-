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

**Leitura do estudo:** collar na razão de 70–80%, condicionado a haver liquidez real nas opções
de ICF — que é fina na B3 e precisa ser confirmada com a mesa de agro da XP antes de qualquer
promessa ao cliente.

## Estrutura

```
ESTUDO_HEDGE_CAFE.md              o estudo completo
saida/Estudo_Hedge_Cafe_ICF.xlsx  calculadora, 7 abas
modelo/gerar_calculadora_cafe.py  gera a planilha do zero
modelo/validar_modelo.py          valida a matemática do modelo
```

Abas da planilha: `Leia-me` · `Parametros` · `Dimensionamento` · `Cenarios` · `Opcoes` ·
`Estruturas` · `Programa de hedge`

## Rodar

```bash
pip install openpyxl
python modelo/gerar_calculadora_cafe.py   # regera a planilha
python modelo/validar_modelo.py           # valida (todas as verificações passam)
```

## Avisos

- Os preços são **exemplos datados de agosto/2026**. Atualize na tela da XP antes de operar.
- Os prêmios de opção são **teóricos** (Black-76). O prêmio real é o da tela/mesa — a liquidez
  de opções de café na B3 é baixa e o spread pode ser largo.
- Margem, corretagem e emolumentos precisam ser **confirmados com a XP**.
- O ICF é cotado em **US$/saca**: existe risco cambial além do risco de café.
- Documento de estudo técnico. **Não é recomendação de investimento.**
