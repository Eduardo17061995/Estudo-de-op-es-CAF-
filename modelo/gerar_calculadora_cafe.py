#!/usr/bin/env python3
"""
Gera a calculadora de hedge de cafe arabica (B3/ICF + opcoes sobre ICF).

Perfil modelado: cliente COMPRADOR / ESTOCADOR de cafe (long fisico).
Risco = queda de preco entre a compra e a revenda.
Hedge base = VENDER futuro ICF; alternativas com opcoes na aba Estruturas.

Todas as celulas azuis sao inputs. Todo o resto e formula.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment

# ---------------------------------------------------------------- estilos
ARIAL = "Arial"
AZUL = Font(name=ARIAL, size=10, color="0000FF")          # input digitado
PRETO = Font(name=ARIAL, size=10)                          # formula
VERDE = Font(name=ARIAL, size=10, color="008000")          # link entre abas
TITULO = Font(name=ARIAL, size=14, bold=True, color="1F3864")
SEC = Font(name=ARIAL, size=11, bold=True, color="1F3864")
CAB = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
NEGRITO = Font(name=ARIAL, size=10, bold=True)
ITAL = Font(name=ARIAL, size=9, italic=True, color="595959")

FILL_CAB = PatternFill("solid", fgColor="1F3864")
FILL_INPUT = PatternFill("solid", fgColor="FFFF00")
FILL_SEC = PatternFill("solid", fgColor="D9E2F3")
FILL_OK = PatternFill("solid", fgColor="E2EFDA")

BORDA = Border(*[Side(style="thin", color="BFBFBF")] * 4)

F_BRL = 'R$ #,##0.00;(R$ #,##0.00);-'
F_BRL0 = 'R$ #,##0;(R$ #,##0);-'
F_USD = 'US$ #,##0.00;(US$ #,##0.00);-'
F_PCT = '0.0%'
F_PCT2 = '0.00%'
F_NUM = '#,##0'
F_NUM2 = '#,##0.00'

wb = Workbook()


def escreve(ws, cel, valor, fonte=PRETO, fmt=None, fill=None, alin=None, borda=False):
    c = ws[cel]
    c.value = valor
    c.font = fonte
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if alin:
        c.alignment = Alignment(horizontal=alin, vertical="center", wrap_text=True)
    if borda:
        c.border = BORDA
    return c


def cabecalho(ws, linha, valores, col_ini=2):
    for i, v in enumerate(valores):
        c = ws.cell(row=linha, column=col_ini + i, value=v)
        c.font = CAB
        c.fill = FILL_CAB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDA


def larguras(ws, mapa):
    for col, w in mapa.items():
        ws.column_dimensions[col].width = w


# ================================================================ 1. LEIA-ME
ws = wb.active
ws.title = "Leia-me"
ws.sheet_view.showGridLines = False
larguras(ws, {"A": 2, "B": 34, "C": 96})

escreve(ws, "B2", "Estudo de hedge de cafe arabica - calculadora", TITULO)
escreve(ws, "B3", "Cliente comprador/estocador de cafe (long fisico) - operacao via XP Investimentos", ITAL)

escreve(ws, "B5", "COMO USAR", SEC, fill=FILL_SEC)
escreve(ws, "C5", "", fill=FILL_SEC)
passos = [
    ("1. Preencha a aba Parametros",
     "Todas as celulas AZUIS com fundo amarelo. Sao os unicos numeros que voce digita. O resto da planilha recalcula sozinho."),
    ("2. Confira Dimensionamento",
     "Quantos contratos ICF vender, quantas sacas ficam descobertas pelo arredondamento e quanto de margem a operacao consome."),
    ("3. Rode a aba Cenarios",
     "Mostra o resultado do fisico, do hedge e do combinado para quedas e altas de preco. E aqui que se ve o hedge funcionando."),
    ("4. Veja Opcoes e Estruturas",
     "Precos teoricos (Black-76) de put e call sobre o futuro, e a comparacao entre nao fazer nada, vender futuro, comprar put e montar collar."),
    ("5. Use Programa de hedge",
     "Constroi o PRECO MEDIO travado ao longo da safra, vendendo em tranches em vez de tudo de uma vez."),
]
r = 6
for a, b in passos:
    escreve(ws, f"B{r}", a, NEGRITO, alin="left")
    escreve(ws, f"C{r}", b, PRETO, alin="left")
    ws.row_dimensions[r].height = 30
    r += 1

r += 1
escreve(ws, f"B{r}", "LEGENDA DE CORES", SEC, fill=FILL_SEC)
escreve(ws, f"C{r}", "", fill=FILL_SEC)
r += 1
legenda = [
    ("Azul com fundo amarelo", "Input - voce digita. Unicas celulas que devem ser alteradas."),
    ("Preto", "Formula calculada nesta aba."),
    ("Verde", "Formula que busca valor em outra aba."),
]
for nome, desc in legenda:
    c = escreve(ws, f"B{r}", nome, alin="left")
    if "Azul" in nome:
        c.font = AZUL
        c.fill = FILL_INPUT
    elif nome == "Verde":
        c.font = VERDE
    escreve(ws, f"C{r}", desc, PRETO, alin="left")
    r += 1

r += 1
escreve(ws, f"B{r}", "AVISOS IMPORTANTES", SEC, fill=FILL_SEC)
escreve(ws, f"C{r}", "", fill=FILL_SEC)
r += 1
avisos = [
    "Os precos de referencia pre-preenchidos sao de agosto/2026 e servem apenas de exemplo. Atualize com a tela da XP antes de usar com o cliente.",
    "Os premios de opcao calculados aqui sao TEORICOS (modelo Black-76). O premio real e o que a mesa/tela da XP mostrar - a liquidez de opcao de cafe na B3 e baixa e o spread pode ser largo.",
    "Percentual de margem, corretagem e emolumentos precisam ser confirmados com a XP - variam por cliente e por contrato.",
    "O contrato ICF e cotado em US$/saca. Se o cliente compra e vende em reais, existe risco de cambio ALEM do risco de cafe. A aba Parametros separa cambio de hoje e cambio no vencimento justamente para voce medir isso.",
    "O basis (diferenca entre o preco local que o cliente pratica e o ICF convertido em reais) e o risco que o hedge NAO elimina. Preencha com os numeros reais do cliente, nao com estimativa.",
    "Esta planilha e ferramenta de estudo, nao recomendacao de investimento. A decisao de hedge e do cliente.",
]
for a in avisos:
    escreve(ws, f"B{r}", "-", PRETO, alin="center")
    escreve(ws, f"C{r}", a, PRETO, alin="left")
    ws.row_dimensions[r].height = 28
    r += 1


# ============================================================ 2. PARAMETROS
p = wb.create_sheet("Parametros")
p.sheet_view.showGridLines = False
larguras(p, {"A": 2, "B": 46, "C": 16, "D": 12, "E": 62})

escreve(p, "B2", "Parametros do estudo", TITULO)
escreve(p, "B3", "Digite somente nas celulas azuis/amarelas.", ITAL)

def bloco(ws, linha, titulo):
    escreve(ws, f"B{linha}", titulo, SEC, fill=FILL_SEC)
    for col in "CDE":
        escreve(ws, f"{col}{linha}", "", fill=FILL_SEC)


def param(ws, linha, rotulo, valor, unidade, fmt, nota, nome=None):
    escreve(ws, f"B{linha}", rotulo, PRETO, alin="left")
    c = escreve(ws, f"C{linha}", valor, AZUL, fmt=fmt, fill=FILL_INPUT, borda=True)
    escreve(ws, f"D{linha}", unidade, ITAL, alin="left")
    escreve(ws, f"E{linha}", nota, ITAL, alin="left")
    ws.row_dimensions[linha].height = 26
    return c


bloco(p, 5, "1. Posicao fisica do cliente")
param(p, 6, "Volume anual comprado", 5000, "sacas 60kg", F_NUM,
      "Informado: ate 5.000 sacas/ano.")
param(p, 7, "Estoque medio carregado por vez", 1500, "sacas 60kg", F_NUM,
      "Quantas sacas ficam expostas ao mesmo tempo. E ISSO que se protege, nao o volume anual.")
param(p, 8, "Preco medio de compra do fisico", 1780, "R$/saca", F_BRL,
      "Custo de aquisicao no produtor. Substituir pelo numero real do cliente.")
param(p, 9, "Prazo medio de carrego do estoque", 3, "meses", F_NUM2,
      "Tempo entre comprar e revender. Define qual vencimento ICF usar.")
param(p, 10, "Custo de carrego (armazenagem + financeiro)", 22, "R$/saca/mes",
      F_BRL, "Armazenagem, seguro, quebra e custo de capital. Confirmar com o cliente.")

bloco(p, 12, "2. Mercado - atualizar com a tela da XP")
param(p, 13, "ICF - preco do vencimento a ser vendido", 368.40, "US$/saca", F_USD,
      "Ref. Dez/26 em 03/08/2026 (exemplo). Cotado em US$ por saca de 60kg.")
param(p, 14, "ICF - vencimento mais curto (referencia)", 391.60, "US$/saca", F_USD,
      "Ref. Set/26 em 03/08/2026. Serve para medir se o mercado esta invertido.")
param(p, 15, "Cambio hoje (USD/BRL)", 5.20, "R$/US$", F_NUM2,
      "Ref. 17/08/2026 (exemplo). Atualizar.")
param(p, 16, "Cambio projetado no vencimento (USD/BRL)", 5.20, "R$/US$", F_NUM2,
      "Deixe igual ao de hoje para isolar o risco de cafe. Mude para estressar o cambio.")
param(p, 17, "Basis de compra (fisico pago - ICF em R$)", -30, "R$/saca", F_BRL,
      "Negativo = cliente compra abaixo da bolsa. Medir com as notas reais do cliente.")
param(p, 18, "Basis de venda (fisico recebido - ICF em R$)", 40, "R$/saca", F_BRL,
      "Positivo = cliente revende acima da bolsa. E a margem comercial dele.")

bloco(p, 20, "3. Politica de hedge")
param(p, 21, "Razao de hedge desejada", 0.80, "% do estoque", F_PCT,
      "Percentual do estoque exposto que sera protegido. 0% = sem hedge, 100% = hedge total.")
param(p, 22, "Sacas por contrato ICF", 100, "sacas", F_NUM,
      "Especificacao B3: 1 contrato ICF = 100 sacas de 60kg. Nao alterar.")
param(p, 23, "Margem de garantia exigida", 0.0488, "% do nocional", F_PCT2,
      "CONFIRMAR COM A XP. Valor de mercado citado publicamente ~4,88%, mas varia.")
param(p, 24, "Colchao de margem para chamada", 3.00, "x margem inicial", F_NUM2,
      "O colchao em % do nocional e (multiplicador-1) x % de margem. Com 1,5x o cliente "
      "aguenta so ~2,4% de alta - pouco para cafe. 3x a 4x e o razoavel.")
param(p, 25, "Custo por contrato (corretagem + emolumentos, ida e volta)", 25, "R$/contrato",
      F_BRL, "CONFIRMAR COM A XP.")

bloco(p, 27, "4. Opcoes sobre futuro de ICF (para Black-76)")
param(p, 28, "Volatilidade implicita", 0.38, "% a.a.", F_PCT,
      "Cafe costuma rodar entre 30% e 50% a.a. Pegar a vol da tela da XP quando houver oferta.")
param(p, 29, "Prazo ate o vencimento da opcao", 0.25, "anos", F_NUM2,
      "0,25 = 3 meses. Manter coerente com o prazo de carrego do estoque.")
param(p, 30, "Taxa de juros para desconto", 0.0430, "% a.a.", F_PCT2,
      "Juros em dolar (o contrato e cotado em US$). Ajustar conforme curva.")

bloco(p, 32, "5. Verificacoes automaticas")
escreve(p, "B33", "ICF do vencimento em reais", PRETO, alin="left")
escreve(p, "C33", "=C13*C15", NEGRITO, fmt=F_BRL, borda=True)
escreve(p, "E33", "Preco da bolsa convertido ao cambio de hoje.", ITAL, alin="left")

escreve(p, "B34", "Mercado invertido? (curto acima do longo)", PRETO, alin="left")
escreve(p, "C34", '=IF(C14>C13,"SIM - INVERTIDO","NAO - normal")', NEGRITO, alin="center", borda=True)
escreve(p, "E34", "Invertido: o mercado paga MENOS pelo cafe futuro. Carregar estoque destroi valor e travar preco longe fica caro. Ponto central do estudo.",
        ITAL, alin="left")
p.row_dimensions[34].height = 30

escreve(p, "B35", "Carrego embutido no mercado (curto -> longo)", PRETO, alin="left")
escreve(p, "C35", "=(C13-C14)*C15", NEGRITO, fmt=F_BRL, borda=True)
escreve(p, "E35", "Quanto o mercado paga (ou cobra) por carregar o estoque ate o vencimento longo, em R$/saca.",
        ITAL, alin="left")

escreve(p, "B36", "Custo proprio de carrego no mesmo prazo", PRETO, alin="left")
escreve(p, "C36", "=C10*C9", NEGRITO, fmt=F_BRL, borda=True)
escreve(p, "E36", "Custo real do cliente para carregar. Se for maior que o carrego do mercado, o estoque esta pagando para existir.",
        ITAL, alin="left")

escreve(p, "B37", "Veredito do carrego", PRETO, alin="left")
escreve(p, "C37", '=IF(C35>=C36,"Mercado paga o carrego","Mercado NAO paga o carrego")',
        NEGRITO, alin="center", borda=True)
escreve(p, "E37", "Se o mercado nao paga o carrego, girar estoque rapido vale mais que travar preco longo.",
        ITAL, alin="left")
p.row_dimensions[37].height = 28

p["C13"].comment = Comment(
    "Fonte do exemplo: ICF Dez/26 a US$368,40 em 03/08/2026 (cotacaodocafe.com).\n"
    "Substituir pela tela da XP no dia da operacao.", "Estudo")
p["C23"].comment = Comment(
    "Percentual de margem citado publicamente (~4,88% do nocional). "
    "Nao e valor oficial garantido - confirmar com a XP.", "Estudo")


# ========================================================= 3. DIMENSIONAMENTO
d = wb.create_sheet("Dimensionamento")
d.sheet_view.showGridLines = False
larguras(d, {"A": 2, "B": 48, "C": 18, "D": 12, "E": 60})

escreve(d, "B2", "Dimensionamento do hedge", TITULO)
escreve(d, "B3", "Quantos contratos vender e quanto caixa a operacao pede.", ITAL)


def linha_calc(ws, linha, rotulo, formula, unidade, fmt, nota, fonte=VERDE, destaque=False):
    escreve(ws, f"B{linha}", rotulo, NEGRITO if destaque else PRETO, alin="left")
    c = escreve(ws, f"C{linha}", formula, fonte, fmt=fmt, borda=True,
                fill=FILL_OK if destaque else None)
    if destaque:
        c.font = Font(name=ARIAL, size=10, bold=True, color="008000")
    escreve(ws, f"D{linha}", unidade, ITAL, alin="left")
    escreve(ws, f"E{linha}", nota, ITAL, alin="left")
    ws.row_dimensions[linha].height = 26


bloco(d, 5, "Sacas a proteger")
linha_calc(d, 6, "Estoque medio exposto", "=Parametros!C7", "sacas", F_NUM,
           "Vem de Parametros.")
linha_calc(d, 7, "Razao de hedge", "=Parametros!C21", "%", F_PCT, "Vem de Parametros.")
linha_calc(d, 8, "Sacas alvo de protecao", "=C6*C7", "sacas", F_NUM,
           "Estoque exposto x razao de hedge.")

bloco(d, 10, "Contratos ICF")
linha_calc(d, 11, "Contratos teoricos", "=C8/Parametros!C22", "contratos", F_NUM2,
           "Sacas alvo / 100 sacas por contrato.", fonte=PRETO)
linha_calc(d, 12, "Contratos a VENDER (arredondado)", "=ROUND(C11,0)", "contratos", F_NUM,
           "O contrato e indivisivel - arredonda para o inteiro mais proximo.",
           fonte=PRETO, destaque=True)
linha_calc(d, 13, "Sacas efetivamente protegidas", "=C12*Parametros!C22", "sacas", F_NUM,
           "", fonte=PRETO)
linha_calc(d, 14, "Sacas descobertas pelo arredondamento", "=C6-C13", "sacas", F_NUM,
           "Positivo = falta protecao. Negativo = hedge maior que o estoque (virou aposta, nao protecao).",
           fonte=PRETO)
linha_calc(d, 15, "Cobertura efetiva do estoque", "=IF(C6=0,0,C13/C6)", "%", F_PCT,
           "Cobertura real depois do arredondamento.", fonte=PRETO)

bloco(d, 17, "Exposicao e sensibilidade")
linha_calc(d, 18, "Nocional do hedge", "=C12*Parametros!C22*Parametros!C13*Parametros!C15",
           "R$", F_BRL0, "Contratos x 100 sacas x ICF x cambio.", fonte=PRETO)
linha_calc(d, 19, "Ganho/perda do hedge por US$1/saca de queda no ICF",
           "=C12*Parametros!C22*1*Parametros!C15", "R$", F_BRL0,
           "Estando vendido, queda de preco gera ganho no hedge.", fonte=PRETO)
linha_calc(d, 20, "Perda no fisico por US$1/saca de queda no ICF",
           "=-C6*1*Parametros!C15", "R$", F_BRL0,
           "O estoque perde valor na mesma direcao.", fonte=PRETO)
linha_calc(d, 21, "Exposicao liquida residual por US$1/saca", "=C19+C20", "R$", F_BRL0,
           "Quanto sobra de risco depois do hedge. Quanto mais perto de zero, mais neutro.",
           fonte=PRETO, destaque=True)

bloco(d, 23, "Caixa e margem")
linha_calc(d, 24, "Margem inicial estimada", "=C18*Parametros!C23", "R$", F_BRL0,
           "Nocional x percentual de margem. CONFIRMAR COM A XP.", fonte=PRETO)
linha_calc(d, 25, "Caixa recomendado (margem + colchao)", "=C24*Parametros!C24", "R$", F_BRL0,
           "Reserva para aguentar chamada de margem sem ter de desmontar o hedge no pior momento.",
           fonte=PRETO, destaque=True)
linha_calc(d, 26, "Custo operacional do hedge (ida e volta)",
           "=C12*Parametros!C25", "R$", F_BRL0, "Corretagem e emolumentos. CONFIRMAR COM A XP.",
           fonte=PRETO)
linha_calc(d, 27, "Custo operacional por saca protegida",
           "=IF(C13=0,0,C26/C13)", "R$/saca", F_BRL,
           "Diluicao do custo. Compare com a margem comercial do cliente.", fonte=PRETO)

bloco(d, 29, "Alerta de chamada de margem")
linha_calc(d, 30, "Alta de preco que consome o colchao de caixa",
           "=IF(C12=0,0,(C25-C24)/(C12*Parametros!C22*Parametros!C15))", "US$/saca", F_USD,
           "Estando VENDIDO, a alta de preco e que gera chamada de margem. Este e o quanto o ICF pode subir antes de o colchao acabar.",
           fonte=PRETO, destaque=True)
d.row_dimensions[30].height = 40
linha_calc(d, 31, "Alta equivalente em %",
           "=IF(Parametros!C13=0,0,C30/Parametros!C13)", "%", F_PCT,
           "Se o cafe subir mais que isso, prepare o cliente: o estoque vale mais, mas o caixa aperta antes.",
           fonte=PRETO)
d.row_dimensions[31].height = 30


# ============================================================== 4. CENARIOS
c = wb.create_sheet("Cenarios")
c.sheet_view.showGridLines = False
larguras(c, {"A": 2, "B": 13, "C": 13, "D": 15, "E": 15, "F": 15, "G": 15,
             "H": 15, "I": 15, "J": 15, "K": 15})

escreve(c, "B2", "Cenarios de preco - fisico x hedge", TITULO)
escreve(c, "B3", "Como o resultado do cliente muda se o cafe cair ou subir ate o vencimento. "
                 "O objetivo do hedge nao e ganhar - e achatar a coluna de resultado combinado.",
        ITAL)
c.row_dimensions[3].height = 28

escreve(c, "B5", "Referencias", SEC, fill=FILL_SEC)
for col in "CDEFGHIJK":
    escreve(c, f"{col}5", "", fill=FILL_SEC)
escreve(c, "B6", "ICF hoje (US$/saca)", PRETO, alin="left")
escreve(c, "C6", "=Parametros!C13", VERDE, fmt=F_USD, borda=True)
escreve(c, "E6", "Sacas em estoque", PRETO, alin="left")
escreve(c, "F6", "=Dimensionamento!C6", VERDE, fmt=F_NUM, borda=True)
escreve(c, "H6", "Contratos vendidos", PRETO, alin="left")
escreve(c, "I6", "=Dimensionamento!C12", VERDE, fmt=F_NUM, borda=True)

escreve(c, "B7", "Cambio no vencimento", PRETO, alin="left")
escreve(c, "C7", "=Parametros!C16", VERDE, fmt=F_NUM2, borda=True)
escreve(c, "E7", "Custo total de carrego", PRETO, alin="left")
escreve(c, "F7", "=Parametros!C10*Parametros!C9", VERDE, fmt=F_BRL, borda=True)
escreve(c, "H7", "Custo operacional total", PRETO, alin="left")
escreve(c, "I7", "=Dimensionamento!C26", VERDE, fmt=F_BRL0, borda=True)

cabs = [
    "Variacao\ndo ICF",
    "ICF no\nvencimento\n(US$/saca)",
    "Preco de\nrevenda\n(R$/saca)",
    "Resultado do\nfisico\n(R$)",
    "Resultado do\nhedge vendido\n(R$)",
    "Resultado\nCOMBINADO\n(R$)",
    "Margem\nSEM hedge\n(R$/saca)",
    "Margem\nCOM hedge\n(R$/saca)",
    "Preco de venda\nefetivo\n(R$/saca)",
]
cabecalho(c, 10, cabs, col_ini=2)
c.row_dimensions[10].height = 48

variacoes = [-0.35, -0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0.0,
             0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35]
r0 = 11
for i, v in enumerate(variacoes):
    r = r0 + i
    escreve(c, f"B{r}", v, AZUL, fmt=F_PCT, fill=FILL_INPUT, borda=True, alin="center")
    # ICF no vencimento
    escreve(c, f"C{r}", f"=$C$6*(1+B{r})", PRETO, fmt=F_USD, borda=True)
    # preco de revenda em R$/saca = ICF * cambio + basis de venda
    escreve(c, f"D{r}", f"=C{r}*$C$7+Parametros!$C$18", PRETO, fmt=F_BRL, borda=True)
    # resultado do fisico = (revenda - compra - carrego) * sacas
    escreve(c, f"E{r}", f"=(D{r}-Parametros!$C$8-$F$7)*$F$6", PRETO, fmt=F_BRL0, borda=True)
    # resultado do hedge vendido = (ICF entrada - ICF venc) * cambio * 100 * contratos - custo op
    escreve(c, f"F{r}", f"=($C$6-C{r})*$C$7*Parametros!$C$22*$I$6-$I$7",
            PRETO, fmt=F_BRL0, borda=True)
    escreve(c, f"G{r}", f"=E{r}+F{r}", NEGRITO, fmt=F_BRL0, borda=True, fill=FILL_OK)
    escreve(c, f"H{r}", f"=IF($F$6=0,0,E{r}/$F$6)", PRETO, fmt=F_BRL, borda=True)
    escreve(c, f"I{r}", f"=IF($F$6=0,0,G{r}/$F$6)", PRETO, fmt=F_BRL, borda=True)
    escreve(c, f"J{r}", f"=IF($F$6=0,0,G{r}/$F$6+Parametros!$C$8+$F$7)",
            PRETO, fmt=F_BRL, borda=True)

ru = r0 + len(variacoes)
escreve(c, f"B{ru+1}", "Resumo", SEC, fill=FILL_SEC)
for col in "CDEFGHIJK":
    escreve(c, f"{col}{ru+1}", "", fill=FILL_SEC)

resumo = [
    ("Pior resultado SEM hedge", f"=MIN(E{r0}:E{ru-1})", F_BRL0,
     "O tamanho do prejuizo que o cliente aceita hoje sem fazer nada."),
    ("Pior resultado COM hedge", f"=MIN(G{r0}:G{ru-1})", F_BRL0,
     "O piso que o hedge constroi."),
    ("Melhor resultado SEM hedge", f"=MAX(E{r0}:E{ru-1})", F_BRL0,
     "O upside que existe hoje."),
    ("Melhor resultado COM hedge", f"=MAX(G{r0}:G{ru-1})", F_BRL0,
     "O upside que o cliente abre mao ao vender futuro. Este e o preco real do hedge."),
    ("Amplitude SEM hedge", f"=MAX(E{r0}:E{ru-1})-MIN(E{r0}:E{ru-1})", F_BRL0,
     "Volatilidade do resultado sem protecao."),
    ("Amplitude COM hedge", f"=MAX(G{r0}:G{ru-1})-MIN(G{r0}:G{ru-1})", F_BRL0,
     "Volatilidade do resultado com protecao. Quanto menor, mais eficaz o hedge."),
    ("Reducao de risco do hedge",
     f"=IF((MAX(E{r0}:E{ru-1})-MIN(E{r0}:E{ru-1}))=0,0,"
     f"1-(MAX(G{r0}:G{ru-1})-MIN(G{r0}:G{ru-1}))/(MAX(E{r0}:E{ru-1})-MIN(E{r0}:E{ru-1})))",
     F_PCT, "Quanto da oscilacao de resultado foi eliminada. Tende a razao de hedge."),
]
rr = ru + 2
for rot, form, fmt, nota in resumo:
    escreve(c, f"B{rr}", rot, PRETO, alin="left")
    c.merge_cells(f"B{rr}:C{rr}")
    escreve(c, f"D{rr}", form, NEGRITO, fmt=fmt, borda=True)
    escreve(c, f"E{rr}", nota, ITAL, alin="left")
    c.merge_cells(f"E{rr}:J{rr}")
    c.row_dimensions[rr].height = 22
    rr += 1


# ================================================================ 5. OPCOES
o = wb.create_sheet("Opcoes")
o.sheet_view.showGridLines = False
larguras(o, {"A": 2, "B": 14, "C": 12, "D": 12, "E": 14, "F": 14, "G": 14,
             "H": 14, "I": 14, "J": 16, "K": 16, "L": 14})

escreve(o, "B2", "Opcoes sobre futuro de ICF - precos teoricos (Black-76)", TITULO)
escreve(o, "B3", "Premio TEORICO. Serve para saber se a tela da XP esta pedindo caro ou barato - nao substitui a cotacao real.",
        ITAL)

escreve(o, "B5", "Entradas do modelo", SEC, fill=FILL_SEC)
for col in "CDEFGHIJKL":
    escreve(o, f"{col}5", "", fill=FILL_SEC)

entradas = [
    ("F - futuro (US$/saca)", "=Parametros!C13", F_USD),
    ("Vol implicita (a.a.)", "=Parametros!C28", F_PCT),
    ("Prazo (anos)", "=Parametros!C29", F_NUM2),
    ("Juros (a.a.)", "=Parametros!C30", F_PCT2),
    ("Cambio no vencimento", "=Parametros!C16", F_NUM2),
]
rr = 6
for rot, form, fmt in entradas:
    escreve(o, f"B{rr}", rot, PRETO, alin="left")
    o.merge_cells(f"B{rr}:C{rr}")
    escreve(o, f"D{rr}", form, VERDE, fmt=fmt, borda=True)
    rr += 1
escreve(o, "B11", "sigma * raiz(T)", PRETO, alin="left")
o.merge_cells("B11:C11")
escreve(o, "D11", "=D7*SQRT(D8)", PRETO, fmt=F_NUM2, borda=True)
escreve(o, "F6", "Como ler esta tabela:", NEGRITO, alin="left")
escreve(o, "F7", "PUT = seguro contra QUEDA. E o que interessa ao cliente comprador/estocador.",
        ITAL, alin="left")
o.merge_cells("F7:L7")
escreve(o, "F8", "CALL = direito de comprar. Serve para quem esta vendido a fixar, ou para VENDER call e financiar a put (collar).",
        ITAL, alin="left")
o.merge_cells("F8:L8")
escreve(o, "F9", "Delta da put diz quantas sacas de protecao cada contrato de opcao realmente entrega hoje.",
        ITAL, alin="left")
o.merge_cells("F9:L9")
escreve(o, "F10", "Piso liquido = strike menos o premio pago, convertido em reais e somado ao basis de venda.",
        ITAL, alin="left")
o.merge_cells("F10:L10")

cabs_o = [
    "Strike\n(US$/saca)",
    "Strike\n% do futuro",
    "d1",
    "d2",
    "Premio PUT\n(US$/saca)",
    "Premio CALL\n(US$/saca)",
    "Delta da\nPUT",
    "Premio PUT\n(R$/saca)",
    "Premio PUT\n% do futuro",
    "Piso liquido\nda PUT\n(R$/saca)",
    "Premio PUT por\ncontrato\n(R$)",
]
cabs_o.append("aux:\n|strike - futuro|")
cabecalho(o, 14, cabs_o, col_ini=2)
o.row_dimensions[14].height = 48
o.column_dimensions["M"].width = 14

r0o = 15
n_strikes = 13
for i in range(n_strikes):
    r = r0o + i
    if i == 0:
        escreve(o, f"B{r}", "=ROUND($D$6*0.80/5,0)*5", AZUL, fmt=F_USD, fill=FILL_INPUT, borda=True)
    else:
        escreve(o, f"B{r}", f"=B{r-1}+ROUND($D$6*0.05/5,0)*5", PRETO, fmt=F_USD, borda=True)
    escreve(o, f"C{r}", f"=IF($D$6=0,0,B{r}/$D$6)", PRETO, fmt=F_PCT, borda=True)
    escreve(o, f"D{r}", f"=(LN($D$6/B{r})+0.5*$D$7^2*$D$8)/$D$11", PRETO, fmt=F_NUM2, borda=True)
    escreve(o, f"E{r}", f"=D{r}-$D$11", PRETO, fmt=F_NUM2, borda=True)
    # put = e^-rT [K N(-d2) - F N(-d1)]
    escreve(o, f"F{r}", f"=EXP(-$D$9*$D$8)*(B{r}*NORMSDIST(-E{r})-$D$6*NORMSDIST(-D{r}))",
            NEGRITO, fmt=F_USD, borda=True)
    # call = e^-rT [F N(d1) - K N(d2)]
    escreve(o, f"G{r}", f"=EXP(-$D$9*$D$8)*($D$6*NORMSDIST(D{r})-B{r}*NORMSDIST(E{r}))",
            PRETO, fmt=F_USD, borda=True)
    escreve(o, f"H{r}", f"=-EXP(-$D$9*$D$8)*NORMSDIST(-D{r})", PRETO, fmt=F_NUM2, borda=True)
    escreve(o, f"I{r}", f"=F{r}*$D$10", PRETO, fmt=F_BRL, borda=True)
    escreve(o, f"J{r}", f"=IF($D$6=0,0,F{r}/$D$6)", PRETO, fmt=F_PCT, borda=True)
    escreve(o, f"K{r}", f"=(B{r}-F{r})*$D$10+Parametros!$C$18", NEGRITO, fmt=F_BRL, borda=True,
            fill=FILL_OK)
    escreve(o, f"L{r}", f"=F{r}*$D$10*Parametros!$C$22", PRETO, fmt=F_BRL0, borda=True)
    # coluna auxiliar: distancia do strike ao futuro (usada para achar a opcao ATM
    # sem depender de formula matricial, que o LibreOffice nao avalia sem CSE)
    escreve(o, f"M{r}", f"=ABS(B{r}-$D$6)", ITAL, fmt=F_NUM2, borda=True)

ruo = r0o + n_strikes - 1
rr = ruo + 2
escreve(o, f"B{rr}", "Medias e leitura do custo do seguro", SEC, fill=FILL_SEC)
for col in "CDEFGHIJKL":
    escreve(o, f"{col}{rr}", "", fill=FILL_SEC)
rr += 1
medias = [
    ("Premio medio das PUTs listadas", f"=AVERAGE(F{r0o}:F{ruo})", F_USD,
     "ATENCAO: NAO use como custo do hedge. A media inclui puts muito dentro do dinheiro, "
     "que sao caras por serem valor intrinseco e que o cliente jamais compraria."),
    ("Premio medio das PUTs (R$/saca)", f"=AVERAGE(I{r0o}:I{ruo})", F_BRL,
     "Mesma ressalva acima. O numero que importa e o premio do strike que ele VAI comprar."),
    ("Premio medio como % do futuro", f"=AVERAGE(J{r0o}:J{ruo})", F_PCT,
     "Regra de bolso: acima de 6-8% do valor do futuro para 3 meses, a put esta cara."),
    ("Strike medio da tabela", f"=AVERAGE(B{r0o}:B{ruo})", F_USD,
     "Centro da grade de strikes."),
    ("Strike mais proximo do futuro (ATM)",
     f"=INDEX(B{r0o}:B{ruo},MATCH(MIN(M{r0o}:M{ruo}),M{r0o}:M{ruo},0))",
     F_USD, "Strike da grade mais colado no futuro."),
    ("Premio da PUT no dinheiro (ATM aprox.)",
     f"=INDEX(F{r0o}:F{ruo},MATCH(MIN(M{r0o}:M{ruo}),M{r0o}:M{ruo},0))",
     F_USD, "Put com strike mais proximo do futuro. Referencia classica de 'quanto custa a vol'."),
    ("Piso liquido dessa PUT ATM (R$/saca)",
     f"=INDEX(K{r0o}:K{ruo},MATCH(MIN(M{r0o}:M{ruo}),M{r0o}:M{ruo},0))",
     F_BRL, "Preco minimo de revenda que o cliente garante comprando essa put."),
    ("Margem garantida por saca com a PUT ATM",
     f"=INDEX(K{r0o}:K{ruo},MATCH(MIN(M{r0o}:M{ruo}),M{r0o}:M{ruo},0))"
     "-Parametros!C8-Parametros!C10*Parametros!C9",
     F_BRL, "Piso liquido menos custo de compra e carrego. Se der negativo, a put nao protege a margem - so limita o prejuizo."),
]
for rot, form, fmt, nota in medias:
    escreve(o, f"B{rr}", rot, PRETO, alin="left")
    o.merge_cells(f"B{rr}:D{rr}")
    escreve(o, f"E{rr}", form, NEGRITO, fmt=fmt, borda=True)
    escreve(o, f"F{rr}", nota, ITAL, alin="left")
    o.merge_cells(f"F{rr}:L{rr}")
    o.row_dimensions[rr].height = 26
    rr += 1

rr += 1
escreve(o, f"B{rr}", "As formulas de premio usam Black-76 (opcao sobre futuro): "
                     "PUT = e^(-rT) x [K x N(-d2) - F x N(-d1)]. Modelo padrao de mercado para opcao sobre commodity futura.",
        ITAL, alin="left")
o.merge_cells(f"B{rr}:L{rr}")


# ============================================================ 6. ESTRUTURAS
e = wb.create_sheet("Estruturas")
e.sheet_view.showGridLines = False
larguras(e, {"A": 2, "B": 30, "C": 15, "D": 15, "E": 15, "F": 15, "G": 15,
             "H": 15, "I": 15, "J": 46})

escreve(e, "B2", "Comparacao de estruturas de protecao", TITULO)
escreve(e, "B3", "Mesmo estoque, quatro caminhos. Resultado por saca no vencimento, ja liquido de premio, carrego e custo de compra.",
        ITAL)

escreve(e, "B5", "Escolha dos strikes", SEC, fill=FILL_SEC)
for col in "CDEFGHIJ":
    escreve(e, f"{col}5", "", fill=FILL_SEC)

escreve(e, "B6", "Strike da PUT comprada (US$/saca)", PRETO, alin="left")
escreve(e, "C6", "=ROUND(Parametros!C13*0.95/5,0)*5", AZUL, fmt=F_USD, fill=FILL_INPUT, borda=True)
escreve(e, "E6", "Premio da PUT (US$/saca)", PRETO, alin="left")
escreve(e, "F6", "=EXP(-Parametros!C30*Parametros!C29)*(C6*NORMSDIST(-(( LN(Parametros!C13/C6)"
                 "+0.5*Parametros!C28^2*Parametros!C29)/(Parametros!C28*SQRT(Parametros!C29))"
                 "-Parametros!C28*SQRT(Parametros!C29)))-Parametros!C13*NORMSDIST(-((LN(Parametros!C13/C6)"
                 "+0.5*Parametros!C28^2*Parametros!C29)/(Parametros!C28*SQRT(Parametros!C29)))))",
        PRETO, fmt=F_USD, borda=True)
escreve(e, "H6", "Premio PUT (R$/saca)", PRETO, alin="left")
escreve(e, "I6", "=F6*Parametros!C16", PRETO, fmt=F_BRL, borda=True)

escreve(e, "B7", "Strike da CALL vendida (US$/saca)", PRETO, alin="left")
escreve(e, "C7", "=ROUND(Parametros!C13*1.10/5,0)*5", AZUL, fmt=F_USD, fill=FILL_INPUT, borda=True)
escreve(e, "E7", "Premio da CALL (US$/saca)", PRETO, alin="left")
escreve(e, "F7", "=EXP(-Parametros!C30*Parametros!C29)*(Parametros!C13*NORMSDIST((LN(Parametros!C13/C7)"
                 "+0.5*Parametros!C28^2*Parametros!C29)/(Parametros!C28*SQRT(Parametros!C29)))"
                 "-C7*NORMSDIST((LN(Parametros!C13/C7)+0.5*Parametros!C28^2*Parametros!C29)"
                 "/(Parametros!C28*SQRT(Parametros!C29))-Parametros!C28*SQRT(Parametros!C29)))",
        PRETO, fmt=F_USD, borda=True)
escreve(e, "H7", "Premio CALL (R$/saca)", PRETO, alin="left")
escreve(e, "I7", "=F7*Parametros!C16", PRETO, fmt=F_BRL, borda=True)

escreve(e, "B8", "Custo liquido do COLLAR (R$/saca)", NEGRITO, alin="left")
escreve(e, "C8", "=I6-I7", NEGRITO, fmt=F_BRL, borda=True, fill=FILL_OK)
escreve(e, "E8", "Se negativo, o collar entra com credito: a call vendida paga mais que a put comprada.",
        ITAL, alin="left")
e.merge_cells("E8:I8")

escreve(e, "B10", "Bases por saca", SEC, fill=FILL_SEC)
for col in "CDEFGHIJ":
    escreve(e, f"{col}10", "", fill=FILL_SEC)
escreve(e, "B11", "Custo de compra + carrego (R$/saca)", PRETO, alin="left")
escreve(e, "C11", "=Parametros!C8+Parametros!C10*Parametros!C9", VERDE, fmt=F_BRL, borda=True)
escreve(e, "E11", "ICF hoje (US$/saca)", PRETO, alin="left")
escreve(e, "F11", "=Parametros!C13", VERDE, fmt=F_USD, borda=True)
escreve(e, "H11", "Cambio no vencimento", PRETO, alin="left")
escreve(e, "I11", "=Parametros!C16", VERDE, fmt=F_NUM2, borda=True)
escreve(e, "B12", "Razao de hedge aplicada", PRETO, alin="left")
escreve(e, "C12", "=Parametros!C21", VERDE, fmt=F_PCT, borda=True)
escreve(e, "E12", "Basis de venda (R$/saca)", PRETO, alin="left")
escreve(e, "F12", "=Parametros!C18", VERDE, fmt=F_BRL, borda=True)

cabs_e = [
    "ICF no\nvencimento\n(US$/saca)",
    "A) Sem hedge\n(R$/saca)",
    "B) Futuro\nvendido\n(R$/saca)",
    "C) PUT\ncomprada\n(R$/saca)",
    "D) Collar\nput + call\n(R$/saca)",
    "Melhor\nestrutura no\ncenario",
]
cabecalho(e, 15, cabs_e, col_ini=2)
e.row_dimensions[15].height = 48

var_e = [-0.35, -0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0.0,
         0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35]
r0e = 16
for i, v in enumerate(var_e):
    r = r0e + i
    escreve(e, f"B{r}", f"=$F$11*(1+{v})", PRETO, fmt=F_USD, borda=True)
    # A) sem hedge: revenda - custo
    escreve(e, f"C{r}", f"=B{r}*$I$11+$F$12-$C$11", PRETO, fmt=F_BRL, borda=True)
    # B) futuro vendido na razao de hedge
    escreve(e, f"D{r}", f"=C{r}+($F$11-B{r})*$I$11*$C$12", PRETO, fmt=F_BRL, borda=True)
    # C) put comprada na razao de hedge: payoff = max(K - F, 0) - premio
    escreve(e, f"E{r}", f"=C{r}+(MAX($C$6-B{r},0)*$I$11-$I$6)*$C$12", PRETO, fmt=F_BRL, borda=True)
    # D) collar: put comprada + call vendida
    escreve(e, f"F{r}", f"=C{r}+(MAX($C$6-B{r},0)*$I$11-MAX(B{r}-$C$7,0)*$I$11-$C$8)*$C$12",
            PRETO, fmt=F_BRL, borda=True)
    escreve(e, f"G{r}",
            f"=INDEX($L$16:$L$19,MATCH(MAX(C{r}:F{r}),C{r}:F{r},0))",
            PRETO, borda=True, alin="center")

# rotulos auxiliares usados pelo INDEX da coluna G (evita constante matricial,
# que o LibreOffice nao avalia sem entrada como matriz)
escreve(e, "L15", "aux: rotulos", ITAL, alin="left")
for k, rot in enumerate(["A) Sem hedge", "B) Futuro", "C) PUT", "D) Collar"]):
    escreve(e, f"L{16+k}", rot, ITAL, alin="left")
e.column_dimensions["L"].width = 16

rue = r0e + len(var_e) - 1
rr = rue + 2
escreve(e, f"B{rr}", "Leitura das estruturas", SEC, fill=FILL_SEC)
for col in "CDEFGHIJ":
    escreve(e, f"{col}{rr}", "", fill=FILL_SEC)
rr += 1

cabecalho(e, rr, ["Indicador", "A) Sem hedge", "B) Futuro", "C) PUT", "D) Collar", "Comentario"],
          col_ini=2)
e.row_dimensions[rr].height = 30
rr += 1

indicadores = [
    ("Pior caso (R$/saca)", "MIN",
     "O piso de cada estrutura. E o numero que decide se o cliente dorme."),
    ("Melhor caso (R$/saca)", "MAX",
     "Quanto de alta cada estrutura preserva. O futuro entrega o pior numero aqui."),
    ("Resultado medio (R$/saca)", "AVERAGE",
     "Media simples dos cenarios - nao e probabilidade, e so o centro da tabela."),
]
for rot, func, nota in indicadores:
    escreve(e, f"B{rr}", rot, PRETO, alin="left")
    for j, col in enumerate("CDEF"):
        escreve(e, f"{col}{rr}", f"={func}({col}{r0e}:{col}{rue})", PRETO, fmt=F_BRL, borda=True)
    escreve(e, f"G{rr}", nota, ITAL, alin="left")
    e.merge_cells(f"G{rr}:J{rr}")
    e.row_dimensions[rr].height = 24
    rr += 1

escreve(e, f"B{rr}", "Amplitude (melhor - pior)", NEGRITO, alin="left")
for col in "CDEF":
    escreve(e, f"{col}{rr}", f"=MAX({col}{r0e}:{col}{rue})-MIN({col}{r0e}:{col}{rue})",
            NEGRITO, fmt=F_BRL, borda=True, fill=FILL_OK)
escreve(e, f"G{rr}", "Quanto menor, mais previsivel o resultado. Previsibilidade e o produto que o hedge vende.",
        ITAL, alin="left")
e.merge_cells(f"G{rr}:J{rr}")
rr += 1

escreve(e, f"B{rr}", "Custo da estrutura (R$/saca)", PRETO, alin="left")
escreve(e, f"C{rr}", 0, PRETO, fmt=F_BRL, borda=True)
escreve(e, f"D{rr}", "=Dimensionamento!C27", VERDE, fmt=F_BRL, borda=True)
escreve(e, f"E{rr}", "=I6*C12+Dimensionamento!C27", PRETO, fmt=F_BRL, borda=True)
escreve(e, f"F{rr}", "=C8*C12+Dimensionamento!C27", PRETO, fmt=F_BRL, borda=True)
escreve(e, f"G{rr}", "Desembolso para montar. Futuro nao paga premio mas consome margem; put paga premio e nao chama margem.",
        ITAL, alin="left")
e.merge_cells(f"G{rr}:J{rr}")
e.row_dimensions[rr].height = 28
rr += 1

escreve(e, f"B{rr}", "Consome margem de garantia?", PRETO, alin="left")
escreve(e, f"C{rr}", "Nao", PRETO, borda=True, alin="center")
escreve(e, f"D{rr}", "Sim - alta", PRETO, borda=True, alin="center")
escreve(e, f"E{rr}", "Nao", PRETO, borda=True, alin="center")
escreve(e, f"F{rr}", "Sim - pela call", PRETO, borda=True, alin="center")
escreve(e, f"G{rr}", "Ponto pratico decisivo: put comprada nao gera chamada de margem, futuro vendido gera se o cafe subir.",
        ITAL, alin="left")
e.merge_cells(f"G{rr}:J{rr}")
e.row_dimensions[rr].height = 28

# ---- teste de viabilidade: a protecao cabe na margem comercial do cliente?
rr += 2
escreve(e, f"B{rr}", "Teste de viabilidade: a protecao cabe na margem do cliente?",
        SEC, fill=FILL_SEC)
for col in "CDEFGHIJ":
    escreve(e, f"{col}{rr}", "", fill=FILL_SEC)
rr += 1
lin_margem = rr
escreve(e, f"B{rr}", "Margem comercial bruta (R$/saca)", NEGRITO, alin="left")
e.merge_cells(f"B{rr}:D{rr}")
escreve(e, f"E{rr}", f"=$F$11*$I$11+$F$12-$C$11", NEGRITO, fmt=F_BRL, borda=True, fill=FILL_OK)
escreve(e, f"F{rr}", "Preco de revenda ao preco de hoje, menos custo de compra e carrego. "
                     "E o lucro que existe para ser protegido.", ITAL, alin="left")
e.merge_cells(f"F{rr}:J{rr}")
e.row_dimensions[rr].height = 26
rr += 1

cabecalho(e, rr, ["Estrutura", "Custo (R$/saca)", "% da margem", "Veredito"], col_ini=2)
e.row_dimensions[rr].height = 26
rr += 1

viab = [
    ("PUT comprada (strike da celula C6)", "=$I$6"),
    ("Collar (put + call vendida)", "=$C$8"),
    ("Futuro vendido (so custo operacional)", "=Dimensionamento!C27"),
]
for rot, form in viab:
    escreve(e, f"B{rr}", rot, PRETO, alin="left")
    escreve(e, f"C{rr}", form, PRETO, fmt=F_BRL, borda=True)
    escreve(e, f"D{rr}", f"=IF($E${lin_margem}<=0,\"\",C{rr}/$E${lin_margem})",
            PRETO, fmt=F_PCT, borda=True)
    escreve(e, f"E{rr}",
            f'=IF($E${lin_margem}<=0,"Sem margem para proteger - revise compra/carrego",'
            f'IF(D{rr}>1,"INVIAVEL - custa mais que o lucro",'
            f'IF(D{rr}>0.5,"CARO - come mais da metade da margem",'
            f'IF(D{rr}>0.25,"ACEITAVEL","CONFORTAVEL"))))',
            NEGRITO, borda=True, alin="left")
    e.merge_cells(f"E{rr}:J{rr}")
    e.row_dimensions[rr].height = 24
    rr += 1

rr += 1
escreve(e, f"B{rr}", "Regra de bolso: protecao que consome mais de 50% da margem comercial "
                     "transfere o lucro do cliente para quem vende a opcao. Nesse caso, "
                     "reduza a razao de hedge, va para strike mais fora do dinheiro, "
                     "ou financie a put vendendo call (collar).", ITAL, alin="left")
e.merge_cells(f"B{rr}:J{rr}")
e.row_dimensions[rr].height = 32


# ====================================================== 7. PROGRAMA DE HEDGE
g = wb.create_sheet("Programa de hedge")
g.sheet_view.showGridLines = False
larguras(g, {"A": 2, "B": 16, "C": 14, "D": 14, "E": 16, "F": 14, "G": 16,
             "H": 16, "I": 18, "J": 44})

escreve(g, "B2", "Programa de hedge - preco medio travado", TITULO)
escreve(g, "B3", "Em vez de travar tudo num dia, trava em tranches. O resultado e um PRECO MEDIO - "
                 "menos sorte, menos arrependimento, menos briga com o cliente depois.", ITAL)
g.row_dimensions[3].height = 28

escreve(g, "B5", "Tranches", SEC, fill=FILL_SEC)
for col in "CDEFGHIJ":
    escreve(g, f"{col}5", "", fill=FILL_SEC)

cabs_g = [
    "Tranche",
    "Data/gatilho",
    "Sacas\ntravadas",
    "Contratos\nICF",
    "ICF travado\n(US$/saca)",
    "Cambio\ntravado",
    "Preco travado\n(R$/saca)",
    "Sacas\nacumuladas",
    "Preco medio\nacumulado\n(R$/saca)",
]
cabecalho(g, 7, cabs_g, col_ini=2)
g.row_dimensions[7].height = 48

exemplos = [
    ("Tranche 1", "Ja executada (exemplo)", 300, 368.40, 5.20),
    ("Tranche 2", "A definir", 300, 368.40, 5.20),
    ("Tranche 3", "A definir", 300, 368.40, 5.20),
    ("Tranche 4", "A definir", 300, 368.40, 5.20),
    ("Tranche 5", "A definir", 0, 368.40, 5.20),
    ("Tranche 6", "A definir", 0, 368.40, 5.20),
]
r0g = 8
for i, (nome, data, sacas, icf, cam) in enumerate(exemplos):
    r = r0g + i
    escreve(g, f"B{r}", nome, PRETO, borda=True, alin="left")
    escreve(g, f"C{r}", data, AZUL, fill=FILL_INPUT, borda=True, alin="left")
    escreve(g, f"D{r}", sacas, AZUL, fmt=F_NUM, fill=FILL_INPUT, borda=True)
    escreve(g, f"E{r}", f"=D{r}/Parametros!$C$22", PRETO, fmt=F_NUM2, borda=True)
    escreve(g, f"F{r}", icf, AZUL, fmt=F_USD, fill=FILL_INPUT, borda=True)
    escreve(g, f"G{r}", cam, AZUL, fmt=F_NUM2, fill=FILL_INPUT, borda=True)
    escreve(g, f"H{r}", f"=F{r}*G{r}+Parametros!$C$18", PRETO, fmt=F_BRL, borda=True)
    escreve(g, f"I{r}", f"=SUM($D${r0g}:D{r})", PRETO, fmt=F_NUM, borda=True)
    escreve(g, f"J{r}", f"=IF(I{r}=0,0,SUMPRODUCT($D${r0g}:D{r},$H${r0g}:H{r})/I{r})",
            NEGRITO, fmt=F_BRL, borda=True, fill=FILL_OK)

rug = r0g + len(exemplos) - 1
escreve(g, f"B{rug+1}", "TOTAL", NEGRITO, borda=True, alin="left")
escreve(g, f"D{rug+1}", f"=SUM(D{r0g}:D{rug})", NEGRITO, fmt=F_NUM, borda=True)
escreve(g, f"E{rug+1}", f"=SUM(E{r0g}:E{rug})", NEGRITO, fmt=F_NUM2, borda=True)
escreve(g, f"H{rug+1}", f"=IF(D{rug+1}=0,0,SUMPRODUCT(D{r0g}:D{rug},H{r0g}:H{rug})/D{rug+1})",
        NEGRITO, fmt=F_BRL, borda=True, fill=FILL_OK)
escreve(g, f"I{rug+1}", "<- preco medio travado do programa", ITAL, alin="left")
g.merge_cells(f"I{rug+1}:J{rug+1}")

rr = rug + 3
escreve(g, f"B{rr}", "Diagnostico do programa", SEC, fill=FILL_SEC)
for col in "CDEFGHIJ":
    escreve(g, f"{col}{rr}", "", fill=FILL_SEC)
rr += 1

diag = [
    ("Volume anual do cliente", "=Parametros!C6", F_NUM,
     "Referencia de quanto ha para travar no ano."),
    ("% do volume anual ja travado", f"=IF(Parametros!C6=0,0,D{rug+1}/Parametros!C6)", F_PCT,
     "Nao passe de 100%: travar mais do que se tem deixa de ser hedge e passa a ser posicao."),
    ("Preco medio travado (R$/saca)", f"=H{rug+1}", F_BRL,
     "Media ponderada por sacas de todas as tranches."),
    ("Custo de compra + carrego (R$/saca)", "=Parametros!C8+Parametros!C10*Parametros!C9", F_BRL,
     "Base de comparacao."),
    ("Margem travada (R$/saca)", f"=H{rug+1}-Parametros!C8-Parametros!C10*Parametros!C9", F_BRL,
     "Se positivo, o programa ja garantiu lucro. Se negativo, esta travando prejuizo - revise antes de executar."),
    ("Margem travada total (R$)", f"=(H{rug+1}-Parametros!C8-Parametros!C10*Parametros!C9)*D{rug+1}",
     F_BRL0, "Resultado em reais que o programa carimba, independente do que o cafe fizer."),
    ("Sacas ainda descobertas no ano", f"=Parametros!C6-D{rug+1}", F_NUM,
     "O que continua exposto ao preco."),
]
for rot, form, fmt, nota in diag:
    escreve(g, f"B{rr}", rot, PRETO, alin="left")
    g.merge_cells(f"B{rr}:D{rr}")
    escreve(g, f"E{rr}", form, NEGRITO, fmt=fmt, borda=True)
    escreve(g, f"F{rr}", nota, ITAL, alin="left")
    g.merge_cells(f"F{rr}:J{rr}")
    g.row_dimensions[rr].height = 26
    rr += 1

rr += 1
escreve(g, f"B{rr}", "Regra pratica: divida o volume em 4 a 6 tranches, defina os gatilhos ANTES "
                     "(preco alvo, data limite, ou margem minima aceita) e registre cada execucao aqui. "
                     "Gatilho escrito antes evita a pior conversa do hedge: explicar depois por que nao travou.",
        ITAL, alin="left")
g.merge_cells(f"B{rr}:J{rr}")
g.row_dimensions[rr].height = 32


# ---------------------------------------------------------------- salvar
import os
destino = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "saida", "Estudo_Hedge_Cafe_ICF.xlsx")
wb.save(destino)
print(f"gerado: {destino}")
