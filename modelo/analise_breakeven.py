#!/usr/bin/env python3
"""
Responde duas perguntas, com numeros:

  1. Quais opcoes sao mais vantajosas para o cliente comprador/estocador?
  2. A partir de que preco ele comeca a ganhar com elas?

"Comecar a ganhar" tem quatro leituras distintas, e todas sao calculadas aqui:
  (a) exercicio      - abaixo do strike a opcao passa a ter valor
  (b) breakeven      - abaixo de (strike - premio) a opcao se paga
  (c) piso de margem - o pior resultado do negocio que a estrutura garante
  (d) teto (collar)  - acima de que preco ele para de ganhar

Rodar: python modelo/analise_breakeven.py
"""

import math

# ---------------------------------------------------- inputs (= aba Parametros)
F = 368.40            # ICF Dez/26, US$/saca
VOL = 0.38            # vol implicita a.a.
T = 0.25              # 3 meses
R = 0.0430            # juros a.a.
CAMBIO = 5.20         # USD/BRL no vencimento
BASIS_VENDA = 40.0    # R$/saca
PRECO_COMPRA = 1780.0
CARREGO = 22.0 * 3    # R$/saca em 3 meses
CUSTO_BASE = PRECO_COMPRA + CARREGO          # R$ 1.846,00/saca
MARGEM = F * CAMBIO + BASIS_VENDA - CUSTO_BASE   # R$ 109,68/saca


def N(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def black76(K, tipo):
    st = VOL * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * VOL ** 2 * T) / st
    d2 = d1 - st
    desc = math.exp(-R * T)
    if tipo == "call":
        return desc * (F * N(d1) - K * N(d2)), desc * N(d1)
    return desc * (K * N(-d2) - F * N(-d1)), -desc * N(-d1)


def margem_em(icf):
    """Margem comercial bruta (R$/saca) se o ICF terminar em icf."""
    return icf * CAMBIO + BASIS_VENDA - CUSTO_BASE


print("=" * 100)
print("SITUACAO DE PARTIDA")
print("=" * 100)
print(f"  ICF Dez/26 ................ US$ {F:.2f}/saca  (R$ {F*CAMBIO:,.2f}/saca)")
print(f"  Custo de compra + carrego . R$ {CUSTO_BASE:,.2f}/saca")
print(f"  Basis de venda ............ R$ {BASIS_VENDA:,.2f}/saca")
print(f"  MARGEM COMERCIAL HOJE ..... R$ {MARGEM:,.2f}/saca")
print(f"  Preco de equilibrio do negocio (margem zero):")
be_negocio = (CUSTO_BASE - BASIS_VENDA) / CAMBIO
print(f"    ICF de US$ {be_negocio:.2f}/saca  ->  queda de {be_negocio/F-1:.1%} ja zera o lucro dele")

# ============================================================ PUTS
print()
print("=" * 100)
print("1. PUTS - o que cada strike entrega")
print("=" * 100)
print(f"  {'Strike':>8} {'% do F':>7} {'Premio':>9} {'Premio':>11} {'% da':>7} "
      f"{'Paga a':>9} {'Breakeven':>10} {'queda p/':>9} {'PISO de':>11}")
print(f"  {'US$':>8} {'':>7} {'US$':>9} {'R$/saca':>11} {'margem':>7} "
      f"{'partir de':>9} {'US$':>10} {'breakeven':>9} {'margem R$':>11}")
print("  " + "-" * 96)

puts = []
for K in [320, 330, 340, 350, 360, 368.40, 375, 385, 395]:
    prem, delta = black76(K, "put")
    prem_brl = prem * CAMBIO
    breakeven = K - prem
    piso = margem_em(K) - prem_brl        # abaixo do strike a put compensa 1:1
    puts.append((K, prem, prem_brl, breakeven, piso, delta))
    print(f"  {K:>8.2f} {K/F:>7.0%} {prem:>9.2f} {prem_brl:>11.2f} "
          f"{prem_brl/MARGEM:>7.0%} {K:>9.2f} {breakeven:>10.2f} "
          f"{breakeven/F-1:>9.1%} {piso:>11.2f}")

print()
print("  Como ler:")
print("    'Paga a partir de'  = abaixo desse ICF a put comeca a ter valor de exercicio.")
print("    'Breakeven'         = abaixo desse ICF a put se paga (ja cobriu o premio).")
print("    'PISO de margem'    = pior resultado por saca que essa put garante, liquido de premio.")
print("                          Negativo = a put limita o prejuizo, mas nao salva o lucro.")

# ============================================================ COLLARS
print()
print("=" * 100)
print("2. COLLARS - put comprada financiada por call vendida")
print("=" * 100)
print(f"  {'Put':>7} {'Call':>7} {'Premio':>9} {'Premio':>9} {'Custo liq':>10} "
      f"{'% da':>6} {'Breakeven':>10} {'queda p/':>9} {'PISO':>9} {'TETO':>9}")
print(f"  {'US$':>7} {'US$':>7} {'put US$':>9} {'call US$':>9} {'R$/saca':>10} "
      f"{'margem':>6} {'US$':>10} {'breakeven':>9} {'R$/saca':>9} {'R$/saca':>9}")
print("  " + "-" * 96)

collars = []
for Kp, Kc in [(350, 385), (350, 395), (350, 405), (350, 420),
               (360, 395), (360, 405), (360, 420),
               (368.40, 405), (368.40, 420), (368.40, 440)]:
    prem_p, _ = black76(Kp, "put")
    prem_c, _ = black76(Kc, "call")
    custo = (prem_p - prem_c) * CAMBIO
    custo_usd = prem_p - prem_c
    breakeven = Kp - custo_usd
    piso = margem_em(Kp) - custo
    teto = margem_em(Kc) - custo
    collars.append((Kp, Kc, custo, breakeven, piso, teto))
    print(f"  {Kp:>7.2f} {Kc:>7.2f} {prem_p:>9.2f} {prem_c:>9.2f} {custo:>10.2f} "
          f"{custo/MARGEM:>6.0%} {breakeven:>10.2f} {breakeven/F-1:>9.1%} "
          f"{piso:>9.2f} {teto:>9.2f}")

print()
print("  PISO = pior margem garantida.  TETO = melhor margem possivel (a call limita acima).")

# =============================================== COMPARACAO NOS CENARIOS
print()
print("=" * 100)
print("3. QUEM GANHA EM CADA CENARIO (margem R$/saca, hedge de 100% para comparar limpo)")
print("=" * 100)

# candidatas escolhidas
prem_350, _ = black76(350, "put")
prem_360, _ = black76(360, "put")
prem_c405, _ = black76(405, "call")
prem_c395, _ = black76(395, "call")
custo_collar_350_405 = (prem_350 - prem_c405) * CAMBIO
custo_collar_360_395 = (prem_360 - prem_c395) * CAMBIO

print(f"  {'ICF venc':>9} {'variacao':>9} {'Sem hedge':>11} {'Futuro':>10} "
      f"{'Put 350':>10} {'Collar':>10} {'Collar':>10}")
print(f"  {'US$':>9} {'':>9} {'':>11} {'vendido':>10} "
      f"{'seca':>10} {'350/405':>10} {'360/395':>10}")
print("  " + "-" * 82)

for v in [-0.35, -0.25, -0.20, -0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15, 0.25, 0.35]:
    icf = F * (1 + v)
    sem = margem_em(icf)
    fut = sem + (F - icf) * CAMBIO
    put = sem + max(350 - icf, 0) * CAMBIO - prem_350 * CAMBIO
    c1 = sem + (max(350 - icf, 0) - max(icf - 405, 0)) * CAMBIO - custo_collar_350_405
    c2 = sem + (max(360 - icf, 0) - max(icf - 395, 0)) * CAMBIO - custo_collar_360_395
    melhor = max(sem, fut, put, c1, c2)
    marca = {sem: "sem hedge", fut: "futuro", put: "put 350",
             c1: "collar 350/405", c2: "collar 360/395"}[melhor]
    print(f"  {icf:>9.2f} {v:>9.0%} {sem:>11.2f} {fut:>10.2f} {put:>10.2f} "
          f"{c1:>10.2f} {c2:>10.2f}   <- {marca}")

print()
print("  " + "-" * 82)
for nome, vals in (
    ("Sem hedge", [margem_em(F * (1 + v)) for v in [-0.35, 0.35]]),
    ("Futuro vendido", [margem_em(F * (1 + v)) + (F - F * (1 + v)) * CAMBIO
                        for v in [-0.35, 0.35]]),
):
    pass

# amplitudes
def serie(fn):
    return [fn(F * (1 + v)) for v in
            [-0.35, -0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0.0,
             0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35]]

estruturas = {
    "Sem hedge": lambda icf: margem_em(icf),
    "Futuro vendido": lambda icf: margem_em(icf) + (F - icf) * CAMBIO,
    "Put 350 seca": lambda icf: margem_em(icf) + max(350 - icf, 0) * CAMBIO - prem_350 * CAMBIO,
    "Collar 350/405": lambda icf: margem_em(icf) + (max(350 - icf, 0)
                                                    - max(icf - 405, 0)) * CAMBIO - custo_collar_350_405,
    "Collar 360/395": lambda icf: margem_em(icf) + (max(360 - icf, 0)
                                                    - max(icf - 395, 0)) * CAMBIO - custo_collar_360_395,
}
print(f"  {'Estrutura':<18}{'PIOR':>10}{'MELHOR':>10}{'Amplitude':>11}{'Custo':>9}")
print("  " + "-" * 60)
for nome, fn in estruturas.items():
    s = serie(fn)
    custo = {"Sem hedge": 0.0, "Futuro vendido": 0.0, "Put 350 seca": prem_350 * CAMBIO,
             "Collar 350/405": custo_collar_350_405,
             "Collar 360/395": custo_collar_360_395}[nome]
    print(f"  {nome:<18}{min(s):>10.2f}{max(s):>10.2f}{max(s)-min(s):>11.2f}{custo:>9.2f}")

print()
print("=" * 100)
print("4. A CONTA QUE RESPONDE 'A PARTIR DE QUANTO ELE GANHA'")
print("=" * 100)
piso_collar = margem_em(350) - custo_collar_350_405
teto_collar = margem_em(405) - custo_collar_350_405
print(f"  Collar 350/405 (custo R$ {custo_collar_350_405:.2f}/saca = "
      f"{custo_collar_350_405/MARGEM:.0%} da margem):")
print(f"    - A put comeca a pagar abaixo de ......... US$ 350,00  ({350/F-1:+.1%})")
print(f"    - O collar se paga abaixo de ............. "
      f"US$ {350-custo_collar_350_405/CAMBIO:.2f}  ({(350-custo_collar_350_405/CAMBIO)/F-1:+.1%})")
print(f"    - Piso de margem garantido .............. R$ {piso_collar:.2f}/saca")
print(f"    - Teto de margem (call limita) .......... R$ {teto_collar:.2f}/saca")
print(f"    - Faixa de resultado: de R$ {piso_collar:.2f} a R$ {teto_collar:.2f}/saca")
print()
print(f"  Sem hedge, na queda de 35%, a margem vira R$ {margem_em(F*0.65):.2f}/saca.")
print(f"  O collar transforma isso em R$ {piso_collar:.2f}/saca -> "
      f"protege R$ {piso_collar - margem_em(F*0.65):,.2f}/saca no pior caso.")
print(f"  Em 1.500 sacas: R$ {(piso_collar - margem_em(F*0.65))*1500:,.0f} de prejuizo evitado.")
