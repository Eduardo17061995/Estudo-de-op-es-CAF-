#!/usr/bin/env python3
"""
Gera o material explicativo para o CLIENTE (PDF), em linguagem simples.

Publico: comerciante de cafe que compra, estoca e revende. Nao e material
tecnico - nao usa jargao (hedge, basis, vol implicita, Black-76, delta).

Saida: saida/Material_Cliente_Protecao_Cafe.pdf

Os numeros vem dos mesmos parametros do estudo tecnico. Sao ILUSTRATIVOS e
estao marcados como tal no documento.
"""

import math
import os
import subprocess

# ------------------------------------------------------------------ premissas
F = 368.40             # ICF do vencimento, US$/saca
CAMBIO = 5.20           # R$/US$
BASIS_VENDA = 40.0      # R$/saca acima da bolsa na revenda
PRECO_COMPRA = 1780.0   # R$/saca
CARREGO = 66.0          # R$/saca em 3 meses
CUSTO_BASE = PRECO_COMPRA + CARREGO
ESTOQUE = 1500          # sacas expostas por vez

K_PUT = 350.0           # piso escolhido
K_CALL = 385.0          # teto escolhido
VOL = 0.38
T = 0.25
R = 0.0430

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def N(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def black76(K, tipo):
    st = VOL * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * VOL ** 2 * T) / st
    d2 = d1 - st
    desc = math.exp(-R * T)
    if tipo == "call":
        return desc * (F * N(d1) - K * N(d2))
    return desc * (K * N(-d2) - F * N(-d1))


PREM_PUT = black76(K_PUT, "put")
PREM_CALL = black76(K_CALL, "call")
CUSTO = (PREM_PUT - PREM_CALL) * CAMBIO      # negativo = credito
MARGEM_HOJE = F * CAMBIO + BASIS_VENDA - CUSTO_BASE
EQUILIBRIO = (CUSTO_BASE - BASIS_VENDA) / CAMBIO


def sem_protecao(icf):
    return icf * CAMBIO + BASIS_VENDA - CUSTO_BASE


def com_protecao(icf):
    return (sem_protecao(icf)
            + (max(K_PUT - icf, 0) - max(icf - K_CALL, 0)) * CAMBIO
            - CUSTO)


PISO = com_protecao(K_PUT - 1)
TETO = com_protecao(K_CALL + 1)


def mil(v):
    """Inteiro no formato pt-BR: 1500 -> 1.500"""
    return f"{v:,.0f}".replace(",", ".")


def usd(v, casas=2):
    """Numero no formato pt-BR, sem simbolo: 368.4 -> 368,40"""
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def brl(v, casas=0):
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−R$ " if v < 0 else "R$ ") + s


# ------------------------------------------------------------------- grafico
CW, CH = 660, 360
X0, X1 = 78, 636
Y0, Y1 = 28, 292
ICF_MIN, ICF_MAX = 280.0, 460.0
V_MIN, V_MAX = -420.0, 660.0


def px(icf):
    return X0 + (icf - ICF_MIN) / (ICF_MAX - ICF_MIN) * (X1 - X0)


def py(v):
    return Y1 - (v - V_MIN) / (V_MAX - V_MIN) * (Y1 - Y0)


def caminho(fn):
    pontos = []
    # amostragem densa + os pontos de quebra exatos, para o traco nao "cortar canto"
    grade = sorted(set([ICF_MIN, K_PUT, K_CALL, ICF_MAX]
                       + [ICF_MIN + i * (ICF_MAX - ICF_MIN) / 90 for i in range(91)]))
    for icf in grade:
        pontos.append(f"{px(icf):.1f},{py(fn(icf)):.1f}")
    return "M " + " L ".join(pontos)


grid_v = [-400, -200, 0, 200, 400, 600]
grid_x = [280, 310, 340, 370, 400, 430, 460]

svg_grid = ""
for v in grid_v:
    y = py(v)
    forte = (v == 0)
    svg_grid += (f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" '
                 f'stroke="{"#9a9891" if forte else "#e6e4dd"}" '
                 f'stroke-width="{1.5 if forte else 1}" '
                 f'{"" if forte else ""}/>')
    svg_grid += (f'<text x="{X0 - 10}" y="{y + 3.5:.1f}" text-anchor="end" '
                 f'class="tick">{brl(v)}</text>')
for icf in grid_x:
    x = px(icf)
    svg_grid += (f'<text x="{x:.1f}" y="{Y1 + 20:.1f}" text-anchor="middle" '
                 f'class="tick">{icf:.0f}</text>')

# faixas de referencia: piso e teto
svg_marcas = (
    f'<line x1="{px(K_PUT):.1f}" y1="{Y0}" x2="{px(K_PUT):.1f}" y2="{Y1}" '
    f'stroke="#c9c6bd" stroke-width="1" stroke-dasharray="3 3"/>'
    f'<line x1="{px(K_CALL):.1f}" y1="{Y0}" x2="{px(K_CALL):.1f}" y2="{Y1}" '
    f'stroke="#c9c6bd" stroke-width="1" stroke-dasharray="3 3"/>'
    f'<text x="{px(K_PUT):.1f}" y="{Y0 - 8}" text-anchor="middle" class="marca">'
    f'piso US$ {K_PUT:.0f}</text>'
    f'<text x="{px(K_CALL):.1f}" y="{Y0 - 8}" text-anchor="middle" class="marca">'
    f'teto US$ {K_CALL:.0f}</text>'
)

svg = f'''<svg viewBox="0 0 {CW} {CH}" class="gr" role="img"
  aria-label="Resultado por saca conforme o preco do cafe, com e sem protecao">
  <title>Resultado por saca conforme o preço do café</title>
  {svg_grid}
  {svg_marcas}
  <path d="{caminho(sem_protecao)}" fill="none" stroke="#eb6834"
        stroke-width="2" stroke-linejoin="round"/>
  <path d="{caminho(com_protecao)}" fill="none" stroke="#2a78d6"
        stroke-width="2" stroke-linejoin="round"/>
  <line x1="{px(F):.1f}" y1="{py(MARGEM_HOJE) - 9:.1f}"
        x2="{px(F):.1f}" y2="{py(MARGEM_HOJE) - 30:.1f}"
        stroke="#9a9891" stroke-width="1"/>
  <circle cx="{px(F):.1f}" cy="{py(MARGEM_HOJE):.1f}" r="4.5"
          fill="#0b0b0b" stroke="#fcfcfb" stroke-width="2"/>
  <text x="{px(F):.1f}" y="{py(MARGEM_HOJE) - 36:.1f}" text-anchor="middle"
        class="hoje">preço de hoje</text>
  <text x="{px(300):.1f}" y="{py(sem_protecao(300)) + 20:.1f}"
        class="rot rot-laranja">Sem proteção</text>
  <text x="{px(300):.1f}" y="{py(PISO) - 12:.1f}"
        class="rot rot-azul">Com proteção</text>
  <text x="{X0 - 10}" y="{Y0 - 8}" text-anchor="end" class="marca">R$/saca</text>
  <text x="{(X0 + X1) / 2:.1f}" y="{CH - 8}" text-anchor="middle" class="eixo">
    Preço do café na bolsa no vencimento (US$ por saca)</text>
</svg>'''

# ------------------------------------------------------------------ cenarios
cenarios = []
for v in (-0.25, -0.15, -0.05, 0.0, 0.05, 0.15, 0.25):
    icf = F * (1 + v)
    s, c = sem_protecao(icf), com_protecao(icf)
    cenarios.append((v, icf, s, c, c - s))

linhas_cen = ""
for v, icf, s, c, dif in cenarios:
    destaque = ' class="ref"' if abs(v) < 1e-9 else ""
    seta = "▲" if v > 0 else ("▼" if v < 0 else "=")
    cls_s = "neg" if s < 0 else "pos"
    cls_c = "neg" if c < 0 else "pos"
    cls_d = "gan" if dif > 0.5 else ("per" if dif < -0.5 else "neu")
    sinal = "+" if dif > 0.5 else ""
    linhas_cen += f'''<tr{destaque}>
      <td class="cen">{seta} {abs(v):.0%}{"" if v else " (hoje)"}</td>
      <td class="num">US$ {usd(icf, 0)}</td>
      <td class="num {cls_s}">{brl(s)}</td>
      <td class="num {cls_c}"><strong>{brl(c)}</strong></td>
      <td class="num {cls_d}">{sinal}{brl(dif)}</td>
    </tr>'''

pior_sem = sem_protecao(F * 0.65)
protegido_total = (PISO - pior_sem) * ESTOQUE

HTML = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Proteção de preço para o seu estoque de café</title>
<style>
  @page {{ size: A4; margin: 16mm 15mm 14mm 15mm; }}
  * {{ box-sizing: border-box; }}
  html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    color: #1a1a19; background: #fff;
    font-size: 10.5pt; line-height: 1.5; margin: 0;
  }}
  .pg {{ page-break-after: always; }}
  .pg:last-child {{ page-break-after: auto; }}

  h1 {{ font-size: 25pt; line-height: 1.15; margin: 0 0 10px; color: #16365c;
        letter-spacing: -0.4px; }}
  h2 {{ font-size: 15.5pt; margin: 0 0 4px; color: #16365c; letter-spacing: -0.2px; }}
  h3 {{ font-size: 11.5pt; margin: 0 0 5px; color: #16365c; }}
  p {{ margin: 0 0 9px; }}
  .lead {{ font-size: 12.5pt; color: #43423e; line-height: 1.45; }}
  .kicker {{ font-size: 8.5pt; letter-spacing: 1.4px; text-transform: uppercase;
             color: #7d7b73; margin: 0 0 14px; font-weight: bold; }}
  .sub {{ font-size: 9.5pt; color: #6b6a63; margin: -2px 0 16px; }}
  hr {{ border: 0; border-top: 2px solid #16365c; margin: 0 0 20px; }}

  /* capa */
  .capa {{ display: flex; flex-direction: column; min-height: 250mm; }}
  .capa-mid {{ flex: 1; display: flex; flex-direction: column;
               justify-content: center; padding: 6mm 0; }}
  .selo {{ display: inline-block; background: #16365c; color: #fff;
           font-size: 8.5pt; font-weight: bold; letter-spacing: 1.2px;
           padding: 5px 12px; border-radius: 3px; margin-bottom: 22mm;
           align-self: flex-start; }}
  .tres {{ margin-top: 16mm; }}
  .tres div {{ display: flex; gap: 12px; margin-bottom: 13px;
               font-size: 11.5pt; line-height: 1.4; }}
  .tres b {{ color: #16365c; font-size: 15pt; min-width: 20px;
             line-height: 1.1; }}

  /* caixas */
  .box {{ border: 1px solid #dedcd4; border-radius: 6px; padding: 13px 16px;
          margin: 0 0 12px; background: #fbfaf7; }}
  .box-al {{ border-left: 4px solid #eb6834; background: #fdf4ef;
             border-color: #f2d9c9; }}
  .box-ok {{ border-left: 4px solid #2a78d6; background: #f1f6fd;
             border-color: #cfe0f5; }}
  .box h3 {{ margin-bottom: 3px; }}
  .box p:last-child {{ margin-bottom: 0; }}

  /* numero grande */
  .hero {{ display: flex; gap: 8mm; margin: 0 0 16px; }}
  .hero-i {{ flex: 1; border-top: 3px solid #16365c; padding-top: 9px; }}
  .hero-n {{ font-size: 21pt; font-weight: bold; color: #16365c;
             line-height: 1.05; letter-spacing: -0.5px; }}
  .hero-n.al {{ color: #c0491c; }}
  .hero-l {{ font-size: 9pt; color: #6b6a63; line-height: 1.35; margin-top: 3px; }}

  /* conta */
  .conta {{ border: 1px solid #dedcd4; border-radius: 6px; overflow: hidden;
            margin: 0 0 14px; }}
  .conta div {{ display: flex; justify-content: space-between;
                padding: 8px 16px; font-size: 10.5pt;
                border-bottom: 1px solid #eceae3; }}
  .conta div:last-child {{ border-bottom: 0; }}
  .conta .tot {{ background: #16365c; color: #fff; font-weight: bold;
                 font-size: 11.5pt; }}
  .conta .v {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}

  /* tabela */
  table {{ width: 100%; border-collapse: collapse; font-size: 10pt;
           margin: 0 0 10px; }}
  th {{ background: #16365c; color: #fff; font-size: 8.5pt; padding: 8px 9px;
        text-align: right; font-weight: bold; line-height: 1.25; }}
  th:first-child {{ text-align: left; }}
  td {{ padding: 7px 9px; border-bottom: 1px solid #eceae3;
        font-variant-numeric: tabular-nums; }}
  td.cen {{ text-align: left; font-variant-numeric: normal; }}
  td.num {{ text-align: right; white-space: nowrap; }}
  tr.ref {{ background: #f4f3ee; }}
  tr.ref td {{ font-weight: bold; }}
  .neg {{ color: #c0491c; }}
  .gan {{ color: #1f6ac2; font-weight: bold; }}
  .per {{ color: #6b6a63; }}
  .neu {{ color: #8a8880; }}

  /* grafico */
  .gr {{ width: 100%; height: auto; display: block; margin: 2px 0 6px; }}
  .tick {{ font: 8.5pt Arial, sans-serif; fill: #7d7b73; }}
  .eixo {{ font: 9pt Arial, sans-serif; fill: #52514e; }}
  .marca {{ font: bold 8pt Arial, sans-serif; fill: #7d7b73; }}
  .hoje {{ font: bold 8.5pt Arial, sans-serif; fill: #1a1a19; }}
  .rot {{ font: bold 10pt Arial, sans-serif; }}
  .rot-laranja {{ fill: #c0491c; }}
  .rot-azul {{ fill: #1f6ac2; }}
  .leg {{ display: flex; gap: 20px; font-size: 9.5pt; color: #43423e;
          margin: 0 0 10px; }}
  .leg span {{ display: flex; align-items: center; gap: 7px; }}
  .sw {{ width: 22px; height: 3px; border-radius: 2px; display: inline-block; }}

  /* cards */
  .cards {{ display: flex; flex-direction: column; gap: 9px; margin: 0 0 12px; }}
  .card {{ border: 1px solid #dedcd4; border-radius: 6px; padding: 12px 15px; }}
  .card.rec {{ border: 2px solid #2a78d6; background: #f1f6fd; }}
  .card-t {{ display: flex; justify-content: space-between; align-items: baseline;
             gap: 10px; margin-bottom: 4px; }}
  .card-t h3 {{ margin: 0; }}
  .tag {{ font-size: 8pt; font-weight: bold; letter-spacing: 0.8px;
          text-transform: uppercase; padding: 3px 9px; border-radius: 10px;
          white-space: nowrap; }}
  .tag-rec {{ background: #2a78d6; color: #fff; }}
  .tag-no {{ background: #eceae3; color: #6b6a63; }}
  .card p {{ margin: 0 0 4px; font-size: 10pt; }}
  .card .como {{ color: #52514e; }}
  .card .quanto {{ font-weight: bold; color: #16365c; margin-bottom: 0; }}

  ul {{ margin: 0 0 10px; padding-left: 18px; }}
  li {{ margin-bottom: 6px; }}

  .passos {{ counter-reset: p; margin: 0 0 14px; }}
  .passos div {{ display: flex; gap: 11px; margin-bottom: 10px; }}
  .passos b {{ background: #16365c; color: #fff; width: 21px; height: 21px;
               min-width: 21px; border-radius: 50%; text-align: center;
               font-size: 9.5pt; line-height: 21px; }}

  .aviso {{ border-top: 1px solid #dedcd4; padding-top: 11px; margin-top: 16px;
            font-size: 8.5pt; color: #6b6a63; line-height: 1.45; }}
  .aviso strong {{ color: #43423e; }}
  .rodape {{ font-size: 8.5pt; color: #8a8880; margin-top: 10px; }}
</style></head><body>

<!-- ============================================== 1. CAPA -->
<section class="pg capa">
  <div class="capa-mid">
    <span class="selo">PROPOSTA DE ESTUDO</span>
    <h1>Como proteger o preço<br>do seu estoque de café</h1>
    <p class="lead" style="max-width: 148mm">
      Você compra café, guarda e revende depois. Entre a compra e a venda,
      o preço pode cair — e esse risco é hoje o maior da sua operação.
      Existe uma forma de travar um piso sem abrir mão de tudo que vem acima dele.
    </p>

    <div class="tres">
      <div><b>1</b><span>Hoje, uma queda de apenas <strong>5,7%</strong> no preço do
        café já zera o seu lucro em cada saca guardada.</span></div>
      <div><b>2</b><span>Dá para garantir um piso de <strong>{brl(PISO, 2)} por saca</strong>
        e continuar ganhando se o café subir — até um teto combinado.</span></div>
      <div><b>3</b><span>No cenário ruim, isso significa cerca de
        <strong>{brl(protegido_total)}</strong> de prejuízo evitado nas suas
        {mil(ESTOQUE)} sacas.</span></div>
    </div>
  </div>
  <p class="rodape">Material preparado pelo seu assessor de investimentos ·
    Operação via XP Investimentos · Agosto de 2026<br>
    Valores ilustrativos, calculados com os preços de mercado da data.
    Não constitui recomendação de investimento.</p>
</section>

<!-- ============================================== 2. O RISCO -->
<section class="pg">
  <p class="kicker">O que está em jogo</p>
  <h2>O seu risco não é o café ficar caro. É ele ficar barato.</h2>
  <p class="sub">Enquanto o café está no seu armazém, ele é seu — e o preço dele muda todos os dias.</p>
  <hr>

  <p>No dia em que você compra o café do produtor, você já pagou o preço daquele dia.
  Se o preço cair antes de você revender, a perda é sua. Não é uma questão de
  negociar melhor: o preço da bolsa muda sozinho, e o café que está parado no
  armazém muda de valor junto.</p>

  <div class="hero">
    <div class="hero-i">
      <div class="hero-n">{mil(ESTOQUE)} sacas</div>
      <div class="hero-l">é o que você costuma ter guardado ao mesmo tempo</div>
    </div>
    <div class="hero-i">
      <div class="hero-n al">−{brl(abs(ESTOQUE * (F * 0.15) * CAMBIO))}</div>
      <div class="hero-l">é o que uma queda de 15% no café tira do seu bolso
        nesse estoque</div>
    </div>
  </div>

  <div class="box box-al">
    <h3>E não é um cenário exótico</h3>
    <p>O café é uma das commodities que mais oscilam no mundo. Quedas de 15% em
    três meses acontecem com frequência — e nada garante que a próxima não
    aconteça exatamente enquanto o seu armazém está cheio.</p>
  </div>

  <h3 style="margin-top:16px">A parte que passa despercebida</h3>
  <p>Guardar café custa dinheiro. Armazenagem, seguro, quebra e o capital que fica
  preso na mercadoria somam cerca de <strong>{brl(CARREGO / 3, 2)} por saca a cada mês</strong>.
  Em três meses de estoque, são <strong>{brl(CARREGO, 2)} por saca</strong> que saem do
  seu resultado antes de qualquer variação de preço.</p>

  <p>É a combinação dos dois — a queda possível <em>mais</em> o custo de guardar —
  que aperta a sua margem. E é por isso que a conta da próxima página é tão apertada.</p>
</section>

<!-- ============================================== 3. A MARGEM -->
<section class="pg">
  <p class="kicker">A sua conta hoje</p>
  <h2>Quanto sobra em cada saca — e a que distância está o zero</h2>
  <p class="sub">Números ilustrativos, com os preços de mercado de agosto de 2026.</p>
  <hr>

  <div class="conta">
    <div><span>Preço de venda estimado (bolsa + o seu diferencial)</span>
      <span class="v">{brl(F * CAMBIO + BASIS_VENDA, 2)}</span></div>
    <div><span>Custo de compra no produtor</span>
      <span class="v">{brl(-PRECO_COMPRA, 2)}</span></div>
    <div><span>Custo de guardar por 3 meses</span>
      <span class="v">{brl(-CARREGO, 2)}</span></div>
    <div class="tot"><span>O que sobra para você, por saca</span>
      <span class="v">{brl(MARGEM_HOJE, 2)}</span></div>
  </div>

  <div class="box box-al">
    <h3>O número que muda a conversa</h3>
    <p>Com essa margem, o preço do café só precisa cair
    <strong>5,7%</strong> — de US$ {usd(F)} para US$ {usd(EQUILIBRIO)} por saca — para o seu
    lucro virar zero. Abaixo disso, você passa a vender com prejuízo cada saca
    que está no armazém.</p>
  </div>

  <p><strong>Por que isso importa na escolha da proteção:</strong> como o seu ponto de
  equilíbrio está perto, não serve comprar uma proteção "barata" que só começa a
  funcionar depois de uma queda de 12% ou 15%. Quando ela funcionasse, o prejuízo
  já estaria feito — e você teria pago pela proteção também.</p>

  <p>A proteção precisa começar a valer <strong>perto do preço de hoje</strong>. É esse o
  critério que usei para escolher a estrutura da próxima página.</p>

  <div class="box">
    <h3>Uma comparação que ajuda</h3>
    <p>É como o seguro do carro. Uma franquia altíssima deixa o seguro baratinho —
    e inútil, porque quase nenhum sinistro chega lá. O que você quer é a franquia
    que cobre o prejuízo que realmente te machuca, por um preço que caiba no mês.</p>
  </div>
</section>

<!-- ============================================== 4. AS OPCOES -->
<section class="pg">
  <p class="kicker">Os três caminhos</p>
  <h2>Como dá para se proteger — e o que cada um custa</h2>
  <p class="sub">Todos usam o mercado futuro de café da B3, pela XP. A diferença está no que você troca.</p>
  <hr>

  <div class="cards">
    <div class="card">
      <div class="card-t"><h3>1. Vender adiantado (travar o preço)</h3>
        <span class="tag tag-no">Trava tudo</span></div>
      <p class="como">Você fixa hoje o preço de venda do seu estoque. Fica sabendo
      exatamente quanto vai receber, aconteça o que acontecer.</p>
      <p class="como"><strong>O que você troca:</strong> se o café subir, você não
      participa. Nada. E precisa deixar dinheiro parado como garantia na
      corretora — dinheiro que pode ser chamado justamente quando o café sobe.</p>
      <p class="quanto">Resultado travado: {brl(MARGEM_HOJE, 2)} por saca, fixo.</p>
    </div>

    <div class="card">
      <div class="card-t"><h3>2. Comprar um seguro de preço</h3>
        <span class="tag tag-no">Caro demais hoje</span></div>
      <p class="como">Você paga um valor à vista e ganha o direito de vender a um
      preço mínimo. Se o café subir, você aproveita a alta e perde só o que pagou.</p>
      <p class="como"><strong>O problema:</strong> hoje esse seguro custa entre
      {brl(black76(K_PUT, "put") * CAMBIO, 2)} e {brl(black76(F, "put") * CAMBIO, 2)} por saca —
      ou seja, de 89% a 131% de tudo que você ganha na saca. O seguro custaria mais
      que o lucro que ele protege.</p>
      <p class="quanto">Não recomendo nas condições atuais de mercado.</p>
    </div>

    <div class="card rec">
      <div class="card-t"><h3>3. Seguro financiado: piso e teto</h3>
        <span class="tag tag-rec">Recomendado</span></div>
      <p class="como">Você compra o mesmo seguro do item 2, e paga por ele
      abrindo mão da alta acima de um teto combinado. Como o teto tem valor para
      quem compra, ele financia o seu seguro — e sobra troco.</p>
      <p class="como"><strong>Na prática:</strong> você garante um piso de
      <strong>{brl(PISO, 2)} por saca</strong> e continua ganhando se o café subir,
      até um teto de <strong>{brl(TETO, 2)} por saca</strong>. Acima do teto,
      o ganho extra fica com a outra ponta.</p>
      <p class="quanto">Custo estimado: nenhum — nas contas de hoje, a estrutura
      entra com um pequeno crédito a seu favor.</p>
    </div>
  </div>

  <div class="box">
    <h3>Por que abrir mão da alta não te machuca tanto</h3>
    <p>Você não vive de apostar na alta do café — vive de comprar e revender com
    margem. O teto só limita um ganho extraordinário que não faz parte do seu
    plano. O piso, ao contrário, protege exatamente aquilo de que o seu negócio
    depende para continuar rodando.</p>
  </div>
</section>

<!-- ============================================== 5. O GRAFICO -->
<section class="pg">
  <p class="kicker">O antes e o depois</p>
  <h2>O mesmo estoque, com e sem proteção</h2>
  <p class="sub">Quanto sobra para você em cada saca, conforme o preço do café no vencimento.</p>
  <hr>

  <div class="leg">
    <span><i class="sw" style="background:#eb6834"></i> Sem proteção</span>
    <span><i class="sw" style="background:#2a78d6"></i> Com proteção (piso e teto)</span>
  </div>

  {svg}

  <p>Leia a linha azul: ela <strong>não desce</strong> abaixo de {brl(PISO, 2)}, por mais
  que o café caia. E ela continua subindo junto com a laranja até o teto — só depois
  fica reta. A laranja não tem fundo: quanto mais o café cai, mais você perde.</p>

  <table>
    <thead><tr>
      <th>Se o café…</th><th>Preço na bolsa</th>
      <th>Sem proteção</th><th>Com proteção</th><th>Diferença</th>
    </tr></thead>
    <tbody>{linhas_cen}</tbody>
  </table>
  <p class="rodape">Valores em reais por saca de 60 kg, já descontados o custo de
  compra e de armazenagem. Ilustrativos.</p>
</section>

<!-- ============================================== 6. DECISAO -->
<section class="pg">
  <p class="kicker">O que eu preciso de você</p>
  <h2>Antes de montar: o que muda a conta, e o que a proteção não resolve</h2>
  <hr>

  <div class="box box-ok">
    <h3>Um ganho que vem antes da proteção — e vale mais que ela</h3>
    <p>Hoje o mercado paga <strong>menos</strong> pelo café entregue mais para a frente do
    que pelo café entregue logo. Somando isso à armazenagem que você economiza,
    <strong>girar o estoque em 1 mês em vez de 3 vale cerca de {brl(164.64, 2)} por
    saca</strong> — mais do que toda a sua margem atual, e muito mais do que qualquer
    proteção financeira entrega.</p>
    <p>Ou seja: antes de contratar proteção, vale olhar se o seu ciclo comercial
    pode ser encurtado. A proteção entra depois, para o estoque que
    inevitavelmente fica parado.</p>
  </div>

  <h3 style="margin-top:16px">O que a proteção não cobre — e você precisa saber</h3>
  <ul>
    <li><strong>O seu diferencial de preço local.</strong> A bolsa negocia um café
    padrão. O seu café tem tipo, bebida e região próprios, e a diferença entre o
    seu preço e o da bolsa continua variando. A proteção cobre a bolsa, não essa
    diferença.</li>
    <li><strong>O dólar.</strong> O contrato de café é cotado em dólar e você compra e
    vende em reais. Se o real se valorizar muito, isso mexe no seu resultado
    mesmo com a proteção de café funcionando. Podemos tratar disso separadamente.</li>
    <li><strong>Disponibilidade.</strong> As opções de café na B3 têm pouco movimento.
    Preciso confirmar com a mesa da XP se existe oferta firme nos preços que
    calculei antes de fechar qualquer coisa.</li>
  </ul>

  <h3 style="margin-top:16px">Para eu fechar os números com precisão, preciso de:</h3>
  <div class="passos">
    <div><b>1</b><span>Quantas sacas você costuma ter guardadas ao mesmo tempo, e
      em quanto tempo você gira o estoque na prática.</span></div>
    <div><b>2</b><span>Suas notas dos últimos 12 meses — de compra e de venda.
      É com elas que eu meço o seu diferencial real em vez de estimar.</span></div>
    <div><b>3</b><span>O seu custo real de guardar: armazenagem, seguro e quebra.</span></div>
    <div><b>4</b><span>Quanto de caixa você consegue deixar reservado sem apertar o
      capital de giro.</span></div>
  </div>

  <div class="box">
    <h3>Uma sugestão sobre como executar</h3>
    <p>Em vez de proteger tudo num único dia — e depender do preço daquele dia —
    o mais sensato é dividir em 4 a 6 partes, com um critério definido antes:
    <em>protejo sempre que o preço garantir uma margem mínima de X por saca</em>.
    Assim você para de tentar acertar o topo e passa a decidir pelo seu negócio.</p>
  </div>

  <div class="aviso">
    <strong>Informações importantes.</strong>
    Este material é um estudo elaborado para fins de discussão e não constitui
    recomendação de investimento, oferta ou promessa de resultado.
    Todos os valores são <strong>ilustrativos</strong> e foram calculados com preços de
    mercado de agosto de 2026 (café arábica na B3 e câmbio da data) e com estimativas
    de custo que ainda precisam ser confirmadas com você — os números finais mudam
    quando substituirmos as estimativas pelos seus dados reais.
    Os valores de prêmio das opções são <strong>teóricos</strong>: o preço efetivo depende
    da oferta disponível no mercado no momento da operação, que no caso das opções de
    café é limitada.
    Operações com derivativos envolvem riscos, inclusive de perda superior ao capital
    inicialmente aportado, e podem exigir depósito adicional de garantias (chamada de
    margem) ao longo da vida da operação.
    Leia a documentação da operação e converse com o seu assessor antes de decidir.
  </div>
</section>

</body></html>'''

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_path = os.path.join(raiz, "saida", "material_cliente.html")
pdf_path = os.path.join(raiz, "saida", "Material_Cliente_Protecao_Cafe.pdf")
os.makedirs(os.path.dirname(html_path), exist_ok=True)
with open(html_path, "w", encoding="utf-8") as fh:
    fh.write(HTML)

print(f"premio put {K_PUT:.0f} = US$ {PREM_PUT:.2f} | premio call {K_CALL:.0f} = US$ {PREM_CALL:.2f}")
print(f"custo liquido = {brl(CUSTO, 2)} (negativo = credito)")
print(f"margem hoje = {brl(MARGEM_HOJE, 2)} | piso = {brl(PISO, 2)} | teto = {brl(TETO, 2)}")
print(f"equilibrio do negocio = US$ {EQUILIBRIO:.2f} ({EQUILIBRIO/F-1:+.1%})")
print(f"prejuizo evitado no pior caso = {brl(protegido_total)}")

subprocess.run([
    CHROME, "--headless", "--no-sandbox", "--disable-gpu",
    "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
    f"file://{html_path}",
], check=True, capture_output=True, timeout=180)
print(f"\ngerado: {pdf_path}")
