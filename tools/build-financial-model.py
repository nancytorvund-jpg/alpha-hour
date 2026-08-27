from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.utils import get_column_letter
wb = Workbook()
INK="12100C"; BRASS="9A6A22"; CREAM="F6F1E7"; LINE="D9D2C3"
hdr_font=Font(bold=True, color="FFFFFF"); hdr_fill=PatternFill("solid", fgColor=INK)
sec_font=Font(bold=True, size=13, color=INK); note_font=Font(italic=True, color="6B6459")
input_fill=PatternFill("solid", fgColor="FFF4DA"); total_font=Font(bold=True)
thin=Side(style="thin", color=LINE); box=Border(bottom=thin)
USD='"$"#,##0'; USDM='"$"#,##0.00,,"M"'; PCT='0%'; NUM='#,##0'
def header(ws, row, cols):
    for i,c in enumerate(cols,1):
        cell=ws.cell(row=row, column=i, value=c); cell.font=hdr_font; cell.fill=hdr_fill; cell.alignment=Alignment(wrap_text=True, vertical="center")
def widths(ws, w):
    for i,x in enumerate(w,1): ws.column_dimensions[get_column_letter(i)].width=x
def title(ws, text, sub=None):
    ws["A1"]=text; ws["A1"].font=Font(bold=True, size=16, color=INK)
    if sub: ws["A2"]=sub; ws["A2"].font=note_font

# ---------------- Assumptions ----------------
A = wb.active; A.title="Assumptions"
title(A, "Alpha Hours financial model: assumptions", "Yellow cells are inputs. Every other tab is formulas off this one. Session-based plan, August 27, 2026.")
rows=[
 ("PRICING",None,None),
 ("Price per session, premium markets",4500,USD),
 ("Price per session, standard markets",3500,USD),
 ("Sessions per year",5,NUM),
 ("Cohorts per seat (enrolled = seats x this)",4,NUM),
 ("Current Alpha family discount",0.05,PCT),
 ("Continuation rate from sixth session, premium",5000,USD),
 ("Deposit at sign-up",500,USD),
 ("Break week price",4500,USD),
 ("VARIABLE COST PER CHILD PER SESSION",None,None),
 ("Timeback license",150,USD),
 ("Extrinsic motivation model (Alpha bucks, Emporium at cost)",40,USD),
 ("Supplies",15,USD),
 ("Snacks (about $2 a weekday block x14, $4 a Saturday block x7)",30,USD),
 ("AlphaTest Showcase, per child (printed mastery map, certificate)",5,USD),
 ("Payment processing rate",0.03,PCT),
 ("Local marketing",60,USD),
 ("Variable cost per child per session","=B11+B12+B13+B14+B15+B16*B2+B17",USD),
 ("Variable cost per child per year","=B18*B4",USD),
 ("GUIDES",None,None),
 ("Guide salary, part-time, per year",50000,USD),
 ("Students per guide (ratio 1:10)",10,NUM),
 ("Guide cost per enrolled child per year at even fill","=B21/(B22*B5)",USD),
 ("FIXED COST PER CAMPUS PER YEAR",None,None),
 ("Lead Guide",75000,USD),
 ("Campus Coordinator (50 percent role)",50000,USD),
 ("Facility (custodial, HVAC, security after hours)",45000,USD),
 ("Insurance",8000,USD),
 ("AlphaTest Showcase events, per campus per session",2000,USD),
 ("Fixed cost per campus per year","=B25+B26+B27+B28+B29*B4",USD),
 ("Minimum operating cost (fixed plus two guides)","=B30+2*B21",USD),
 ("Contribution per child per year before guides","=(B2-B18)*B4",USD),
 ("Break-even students per campus","=ROUNDUP(B31/B32,0)",NUM),
 ("CENTRAL",None,None),
 ("Central team, fully loaded, Year 1",875000,USD),
 ("Central team at full network",4000000,USD),
 ("PLAN FILL BY SESSION",None,None),
 ("Session 2 (Oct 19 to Dec 18, 2026)",0.6,PCT),
 ("Session 3 (Jan 4 to Feb 19, 2027)",0.75,PCT),
 ("Session 4 (Feb 24 to Apr 16, 2027)",0.9,PCT),
 ("Session 5 (Apr 26 to Jun 18, 2027)",1.0,PCT),
 ("Floor case fill, every session",0.25,PCT),
 ("LANE MIX",None,None),
 ("Stay (never enrolling)",0.70,PCT),
 ("Considering",0.15,PCT),
 ("Path to yes",0.05,PCT),
 ("Current Alpha families",0.10,PCT),
 ("Lifetime tuition per conversion, midpoint",240000,USD),
]
r=4
for label,val,fmt in rows:
    A.cell(row=r,column=1,value=label)
    if val is None: A.cell(row=r,column=1).font=sec_font
    else:
        c=A.cell(row=r,column=2,value=val); c.number_format=fmt
        if not (isinstance(val,str) and val.startswith("=")): c.fill=input_fill
    r+=1
widths(A,[62,18])
# map of key cells (row numbers as placed): verify by construction
K={ "price":"Assumptions!$B$5", "price_std":"Assumptions!$B$6", "sess":"Assumptions!$B$7", "coh":"Assumptions!$B$8", "disc":"Assumptions!$B$9",
    "var_s":"Assumptions!$B$21", "var_y":"Assumptions!$B$22", "guide":"Assumptions!$B$24", "ratio":"Assumptions!$B$25",
    "coord":"Assumptions!$B$29", "fixed":"Assumptions!$B$33", "mincost":"Assumptions!$B$34", "contrib":"Assumptions!$B$35",
    "central":"Assumptions!$B$38", "central_nat":"Assumptions!$B$39", "f2":"Assumptions!$B$41","f3":"Assumptions!$B$42","f4":"Assumptions!$B$43","f5":"Assumptions!$B$44","ffloor":"Assumptions!$B$45",
    "stay":"Assumptions!$B$47","cons":"Assumptions!$B$48","pty":"Assumptions!$B$49","cur":"Assumptions!$B$50","ltv":"Assumptions!$B$51",
    "proc":"Assumptions!$B$19","tb":"Assumptions!$B$14","mot":"Assumptions!$B$15","sup":"Assumptions!$B$16","snk":"Assumptions!$B$17","shw":"Assumptions!$B$18","mkt":"Assumptions!$B$20","shw_ev":"Assumptions!$B$32","lg":"Assumptions!$B$28","fac":"Assumptions!$B$30","ins":"Assumptions!$B$31"}
# sanity: check labels at those rows
chk={5:"Price per session, premium",21:"Variable cost per child per session",22:"Variable cost per child per year",24:"Guide salary",25:"Students per guide",29:"Campus Coordinator",33:"Fixed cost per campus per year",34:"Minimum operating",35:"Contribution",38:"Central team, fully",39:"Central team at full",41:"Session 2",45:"Floor case",47:"Stay",51:"Lifetime"}
for rr,lab in chk.items(): assert str(A.cell(row=rr,column=1).value).startswith(lab), (rr, A.cell(row=rr,column=1).value)

# ---------------- Campuses ----------------
C=wb.create_sheet("Campuses")
title(C,"Pilot campuses at capacity","Enrolled = seats x cohorts. Guides = seats / 10, rounded up. William Street shares New York's coordinator.")
header(C,4,["Campus","Seats","Shares coordinator (1 = yes)","Enrolled","Revenue / year","Variable cost","Guides","Guide cost","Fixed cost","Site profit","Margin"])
camps=[("New York, 180 Maiden Lane",100,0),("New York, 156 William Street",30,1),("Greenwich (Armonk)",80,0),("Boston A",40,0),("Boston B",100,0),("Chicago, at launch (94 seats)",94,0),("Chicago, from January 2027 (517 seats)",517,0)]
for i,(n,s,sh) in enumerate(camps):
    r=5+i
    C.cell(row=r,column=1,value=n); C.cell(row=r,column=2,value=s).fill=input_fill; C.cell(row=r,column=3,value=sh).fill=input_fill
    C.cell(row=r,column=4,value=f"=B{r}*{K['coh']}")
    C.cell(row=r,column=5,value=f"=D{r}*{K['price']}*{K['sess']}")
    C.cell(row=r,column=6,value=f"=D{r}*{K['var_y']}")
    C.cell(row=r,column=7,value=f"=ROUNDUP(B{r}/{K['ratio']},0)")
    C.cell(row=r,column=8,value=f"=G{r}*{K['guide']}")
    C.cell(row=r,column=9,value=f"={K['fixed']}-C{r}*{K['coord']}")
    C.cell(row=r,column=10,value=f"=E{r}-F{r}-H{r}-I{r}")
    C.cell(row=r,column=11,value=f"=J{r}/E{r}")
# totals: launch = rows 5-10 ; expanded = rows 5-9 + 11
def tot_row(r,label,rows_expr):
    C.cell(row=r,column=1,value=label).font=total_font
    for col in "BDEFGHIJ":
        C[f"{col}{r}"]=f"=SUM({rows_expr(col)})"; C[f"{col}{r}"].font=total_font
    C[f"K{r}"]=f"=J{r}/E{r}"; C[f"K{r}"].font=total_font
tot_row(13,"Launch total, Session 2 (Chicago at 94)", lambda c: f"{c}5:{c}10")
tot_row(14,"Expanded total, Session 3 onward (Chicago at 517)", lambda c: f"{c}5:{c}9,{c}11")
C["A16"]="New York alone (two buildings)"; C["E16"]="=E5+E6"; C["J16"]="=J5+J6"
C["A17"]="Revenue per session at capacity, launch / expanded"; C["E17"]=f"=E13/{K['sess']}"; C["J17"]=f"=J13/{K['sess']}"
C["A18"]="Site profit per session at capacity, launch / expanded"; C["E18"]=f"=E14/{K['sess']}"; C["J18"]=f"=J14/{K['sess']}"
C["A19"]="Expanded run rate, net after central team"; C["J19"]=f"=J14-{K['central']}"
for r in range(5,20):
    for col,f in (("D",NUM),("E",USD),("F",USD),("G",NUM),("H",USD),("I",USD),("J",USD),("K",PCT)): C[f"{col}{r}"].number_format=f
widths(C,[44,8,14,10,15,14,8,13,12,14,9])

# ---------------- Year 1 ----------------
Y=wb.create_sheet("Year 1")
title(Y,"Year 1 by session: capacity, plan, floor","Session 2 runs on the launch footprint (444 seats), Sessions 3 to 5 on the expanded footprint (867 seats). Guides are hired to sold seats: per campus, seats x fill / 10, rounded up.")
def block(start,label,fills,seats_ref_launch,seats_ref_exp):
    Y.cell(row=start,column=1,value=label).font=sec_font
    header(Y,start+1,["Session","Dates","Fill","Seats","Enrolled","Revenue","Variable cost","Guides","Guide cost","Fixed cost","Site profit","Margin"])
    dates=["Oct 19 to Dec 18, 2026","Jan 4 to Feb 19, 2027","Feb 24 to Apr 16, 2027","Apr 26 to Jun 18, 2027"]
    for i in range(4):
        r=start+2+i; launch=(i==0)
        rng="Campuses!$B$5:$B$10" if launch else "Campuses!$B$5:$B$9,Campuses!$B$11"
        Y.cell(row=r,column=1,value=f"Session {i+2}"); Y.cell(row=r,column=2,value=dates[i]); Y.cell(row=r,column=3,value=fills[i])
        Y.cell(row=r,column=4,value="=Campuses!B13" if launch else "=Campuses!B14")
        Y.cell(row=r,column=5,value=f"=ROUND(D{r}*{K['coh']}*C{r},0)")
        Y.cell(row=r,column=6,value=f"=E{r}*{K['price']}")
        Y.cell(row=r,column=7,value=f"=E{r}*{K['var_s']}")
        if launch: Y.cell(row=r,column=8,value=f"=SUMPRODUCT(ROUNDUP(Campuses!$B$5:$B$10*C{r}/{K['ratio']},0))")
        else: Y.cell(row=r,column=8,value=f"=SUMPRODUCT(ROUNDUP(Campuses!$B$5:$B$9*C{r}/{K['ratio']},0))+ROUNDUP(Campuses!$B$11*C{r}/{K['ratio']},0)")
        Y.cell(row=r,column=9,value=f"=H{r}*{K['guide']}/{K['sess']}")
        Y.cell(row=r,column=10,value=f"=(Campuses!$I$13)/{K['sess']}")
        Y.cell(row=r,column=11,value=f"=F{r}-G{r}-I{r}-J{r}")
        Y.cell(row=r,column=12,value=f"=K{r}/F{r}")
    t=start+6
    Y.cell(row=t,column=1,value="Year 1 total").font=total_font
    for col in "EFGIJK": Y[f"{col}{t}"]=f"=SUM({col}{start+2}:{col}{start+5})"; Y[f"{col}{t}"].font=total_font
    Y[f"L{t}"]=f"=K{t}/F{t}"
    Y.cell(row=t+1,column=1,value="Central team (charged in full)"); Y[f"K{t+1}"]=f"=-{K['central']}"
    Y.cell(row=t+2,column=1,value="Net").font=total_font; Y[f"K{t+2}"]=f"=K{t}+K{t+1}"; Y[f"K{t+2}"].font=total_font
    for r in range(start+2,t+3):
        for col,f in (("C",PCT),("D",NUM),("E",NUM),("F",USD),("G",USD),("H",NUM),("I",USD),("J",USD),("K",USD),("L",PCT)): Y[f"{col}{r}"].number_format=f
    return t+2
e1=block(4,"Plan (the number the Head is held to)",[f"={K['f2']}",f"={K['f3']}",f"={K['f4']}",f"={K['f5']}"],None,None)
e2=block(e1+2,"Capacity (every seat sold)",[1,1,1,1],None,None)
e3=block(e2+2,"Floor (25 percent fill all year)",[f"={K['ffloor']}"]*4,None,None)
s=e3+2
Y.cell(row=s,column=1,value="Summary").font=sec_font
header(Y,s+1,["Case","","","","","Revenue","","","","","Site profit","Net"])
for i,(lab,t) in enumerate((("Capacity",e2-2),("Plan",e1-2),("Floor",e3-2))):
    r=s+2+i; Y.cell(row=r,column=1,value=lab); Y[f"F{r}"]=f"=F{t}"; Y[f"K{r}"]=f"=K{t}"; Y[f"L{r}"]=f"=K{t+2}"
    for col in "FKL": Y[f"{col}{r}"].number_format=USD
widths(Y,[34,24,8,8,10,14,13,8,12,12,14,10])

# ---------------- Campus P&L (100 seats) ----------------
P=wb.create_sheet("100-seat campus")
title(P,"A 100-seat campus at capacity, line by line, per year","Change the seats in B4 to see any campus.")
P["A4"]="Seats"; P["B4"]=100; P["B4"].fill=input_fill
P["A5"]="Enrolled"; P["B5"]=f"=B4*{K['coh']}"
lines=[("Revenue",f"=B5*{K['price']}*{K['sess']}"),("Timeback",f"=-B5*{K['tb']}*{K['sess']}"),("Extrinsic motivation model (Emporium)",f"=-B5*{K['mot']}*{K['sess']}"),("Supplies",f"=-B5*{K['sup']}*{K['sess']}"),("Snacks",f"=-B5*{K['snk']}*{K['sess']}"),("AlphaTest Showcase (per child reports plus campus events)",f"=-(B5*{K['shw']}*{K['sess']}+{K['shw_ev']}*{K['sess']})"),("Payment processing",f"=-B7*{K['proc']}"),("Local marketing",f"=-B5*{K['mkt']}*{K['sess']}"),("Guides (seats / 10, rounded up, at guide salary)",f"=-ROUNDUP(B4/{K['ratio']},0)*{K['guide']}"),("Lead Guide",f"=-{K['lg']}"),("Campus Coordinator",f"=-{K['coord']}"),("Facility",f"=-{K['fac']}"),("Insurance",f"=-{K['ins']}")]
for i,(lab,f) in enumerate(lines):
    r=7+i; P.cell(row=r,column=1,value=lab); P.cell(row=r,column=2,value=f).number_format=USD
P["A21"]="Total cost"; P["B21"]="=SUM(B8:B19)"; P["A22"]="Site profit"; P["B22"]="=B7+B21"; P["A23"]="Margin"; P["B23"]="=B22/B7"
for r in (21,22): P[f"B{r}"].number_format=USD; P[f"A{r}"].font=total_font; P[f"B{r}"].font=total_font
P["B23"].number_format=PCT
P["A25"]="Motivation model, snacks and showcase together"; P["B25"]="=-(B9+B11+B12)"; P["B25"].number_format=USD
P["A26"]="As a share of revenue"; P["B26"]="=B25/B7"; P["B26"].number_format='0.0%'
widths(P,[56,16])

# ---------------- Sensitivity ----------------
S=wb.create_sheet("Sensitivity")
title(S,"Sensitivity on the expanded footprint (867 seats), annual")
S["A4"]="Fill"; S["A4"].font=sec_font
header(S,5,["Fill","Enrolled","Revenue","Variable cost","Guides","Guide cost","Fixed cost","Site profit","Net after central","Margin"])
for i,f in enumerate((0.25,0.5,0.75,1.0)):
    r=6+i; S.cell(row=r,column=1,value=f).fill=input_fill
    S[f"B{r}"]=f"=ROUND(Campuses!$B$14*{K['coh']}*A{r},0)"; S[f"C{r}"]=f"=B{r}*{K['price']}*{K['sess']}"; S[f"D{r}"]=f"=B{r}*{K['var_y']}"
    S[f"E{r}"]=f"=SUMPRODUCT(ROUNDUP(Campuses!$B$5:$B$9*A{r}/{K['ratio']},0))+ROUNDUP(Campuses!$B$11*A{r}/{K['ratio']},0)"
    S[f"F{r}"]=f"=E{r}*{K['guide']}"; S[f"G{r}"]="=Campuses!$I$14"; S[f"H{r}"]=f"=C{r}-D{r}-F{r}-G{r}"; S[f"I{r}"]=f"=H{r}-{K['central']}"; S[f"J{r}"]=f"=H{r}/C{r}"
    for col,fm in (("A",PCT),("B",NUM),("C",USD),("D",USD),("E",NUM),("F",USD),("G",USD),("H",USD),("I",USD),("J",PCT)): S[f"{col}{r}"].number_format=fm
S["A12"]="Price (at capacity; processing scales with price)"; S["A12"].font=sec_font
header(S,13,["Session price","Enrolled","Revenue","Variable cost","","Guide cost","Fixed cost","Site profit","Net after central","Margin"])
for i,p in enumerate((3500,4000,4500,5000,5500)):
    r=14+i; S.cell(row=r,column=1,value=p).fill=input_fill
    S[f"B{r}"]="=Campuses!$D$14"; S[f"C{r}"]=f"=B{r}*A{r}*{K['sess']}"
    S[f"D{r}"]=f"=B{r}*({K['var_s']}-{K['proc']}*{K['price']}+{K['proc']}*A{r})*{K['sess']}"
    S[f"F{r}"]="=Campuses!$H$14"; S[f"G{r}"]="=Campuses!$I$14"; S[f"H{r}"]=f"=C{r}-D{r}-F{r}-G{r}"; S[f"I{r}"]=f"=H{r}-{K['central']}"; S[f"J{r}"]=f"=H{r}/C{r}"
    for col,fm in (("A",USD),("B",NUM),("C",USD),("D",USD),("F",USD),("G",USD),("H",USD),("I",USD),("J",PCT)): S[f"{col}{r}"].number_format=fm
S["A20"]="Every $500 on the session price, at capacity"; S["C20"]=f"=Campuses!$D$14*500*{K['sess']}*(1-{K['proc']})"; S["C20"].number_format=USD
widths(S,[30,10,14,13,8,12,12,14,16,9])

# ---------------- Lanes ----------------
L=wb.create_sheet("Lanes")
title(L,"Revenue by lane at expanded capacity","The plan is sized on Stay. Mix is an assumption Session 2 replaces.")
header(L,4,["Lane","Share","Families","Session revenue / year","Value beyond the session fee (modeled)","Basis"])
lanes=[("Stay (the business)",K['stay'],f"=C5*({K['price']}*{K['sess']}*1+{K['cont'] if False else 'Assumptions!$B$10'}*{K['sess']}*2)","Three years: year one at list, years two and three at the continuation rate"),
       ("Considering (upside)",K['cons'],f"=C6*({K['price']}*2+0.2*{K['ltv']})","Two sessions plus a 20 percent conversion at the lifetime tuition midpoint"),
       ("Path to yes (upside)",K['pty'],f"=C7*({K['price']}*3+0.2*{K['ltv']})","Three sessions plus a 20 percent admit rate at the lifetime tuition midpoint"),
       ("Current Alpha families",K['cur'],"","Retention of a family already paying full tuition")]
for i,(n,share,val,basis) in enumerate(lanes):
    r=5+i; L.cell(row=r,column=1,value=n); L[f"B{r}"]=f"={share}"; L[f"C{r}"]=f"=ROUND(Campuses!$D$14*B{r},0)"
    L[f"D{r}"]=f"=C{r}*{K['price']}*{K['sess']}" if i<3 else f"=C{r}*{K['price']}*{K['sess']}*(1-{K['disc']})"
    if val: L[f"E{r}"]=val
    L[f"F{r}"]=basis
    for col,fm in (("B",PCT),("C",NUM),("D",USD),("E",USD)): L[f"{col}{r}"].number_format=fm
L["A9"]="Total"; L["A9"].font=total_font; L["B9"]="=SUM(B5:B8)"; L["C9"]="=SUM(C5:C8)"; L["D9"]="=SUM(D5:D8)"
for col,fm in (("B",PCT),("C",NUM),("D",USD)): L[f"{col}9"].number_format=fm
L["A11"]="Feeder sensitivity (upside), expanded pilot base"; L["A11"].font=sec_font
header(L,12,["Conversion rate","Enrollments","Lifetime tuition"])
for i,c in enumerate((0.04,0.08,0.12)):
    r=13+i; L[f"A{r}"]=c; L[f"A{r}"].fill=input_fill; L[f"B{r}"]=f"=ROUND(Campuses!$D$14*A{r},0)"; L[f"C{r}"]=f"=B{r}*{K['ltv']}"
    L[f"A{r}"].number_format=PCT; L[f"B{r}"].number_format=NUM; L[f"C{r}"].number_format=USD
widths(L,[28,9,10,20,30,62])

# ---------------- National ----------------
N=wb.create_sheet("National")
title(N,"The national build, capacity figures, K-8 blocks, premium price")
header(N,4,["Wave","Session","Campuses added","Campuses (count)","Seats added","Enrolled added","Run rate added","Network run rate"])
waves=[("Pilot","Session 2, Oct 2026","New York (2), Greenwich, Boston (2), Chicago",6,"=Campuses!B13"),("Wave 2","Session 3, Jan 2027","Chicago expansion (+423), Austin 300, Miami 150, Palm Beach 60, Miami Beach 50",4,"=423+300+150+60+50"),("Wave 3","Session 4, Feb 2027","Every remaining campus, about 30, at 50 seats each",30,"=30*50")]
for i,(w,sess,c,cnt,seats) in enumerate(waves):
    r=5+i; N[f"A{r}"]=w; N[f"B{r}"]=sess; N[f"C{r}"]=c; N[f"D{r}"]=cnt; N[f"E{r}"]=seats; N[f"F{r}"]=f"=E{r}*{K['coh']}"; N[f"G{r}"]=f"=F{r}*{K['price']}*{K['sess']}"; N[f"H{r}"]=f"=SUM($G$5:G{r})"
    for col,fm in (("D",NUM),("E",NUM),("F",NUM),("G",USD),("H",USD)): N[f"{col}{r}"].number_format=fm
N["A9"]="Full network at capacity"; N["A9"].font=sec_font
items=[("Campuses","=SUM(D5:D7)",NUM),("Seats","=SUM(E5:E7)",NUM),("Enrolled","=SUM(F5:F7)",NUM),("Revenue",f"=B12*{K['price']}*{K['sess']}",USD),("Variable cost",f"=-B12*{K['var_y']}",USD),("Guide cost",f"=-ROUNDUP(B11/{K['ratio']},0)*{K['guide']}",USD),("Fixed cost",f"=-B10*{K['fixed']}",USD),("Site profit","=B13+B14+B15+B16",USD),("Margin","=B17/B13",PCT),("Central team at full network",f"=-{K['central_nat']}",USD),("Net","=B17+B19",USD)]
for i,(lab,f,fm) in enumerate(items):
    r=10+i; N[f"A{r}"]=lab; N[f"B{r}"]=f; N[f"B{r}"].number_format=fm
N["A17"].font=total_font; N["B17"].font=total_font; N["A20"].font=total_font; N["B20"].font=total_font
N["A22"]="Three-year view (network held at 40 campuses; evening block and break weeks as additions)"; N["A22"].font=sec_font
header(N,23,["Year","K-8 fill","K-8 revenue","Evening block share of its ceiling","Evening block revenue","Break weeks share","Break week revenue (2 weeks)","Total revenue","Net (about, at network margin)"])
yrs=[("Year 2, SY27-28",0.75,0.40,0.60),("Year 3, SY28-29",0.90,0.70,0.80)]
for i,(y,kf,ef,bf) in enumerate(yrs):
    r=24+i; N[f"A{r}"]=y; N[f"B{r}"]=kf; N[f"D{r}"]=ef; N[f"F{r}"]=bf
    for col in "BDF": N[f"{col}{r}"].fill=input_fill; N[f"{col}{r}"].number_format=PCT
    N[f"C{r}"]=f"=$B$13*B{r}"; N[f"E{r}"]=f"=$B$13*0.5*D{r}"; N[f"G{r}"]=f"=$B$11*2*Assumptions!$B$12*F{r}"; N[f"H{r}"]=f"=C{r}+E{r}+G{r}"; N[f"I{r}"]=f"=H{r}*$B$18-{K['central_nat']}"
    for col in "CEGHI": N[f"{col}{r}"].number_format=USD
widths(N,[30,20,60,10,12,14,16,16,20])

# ---------------- Launch budget ----------------
B=wb.create_sheet("Launch budget")
title(B,"One-time launch budget, before Session 2")
header(B,4,["Item","Basis","Cost"])
items=[("Guide training cohort","45 guides and 6 Lead Guides, two paid weeks at the part-time rate",f"=(Campuses!G13+6)*{K['guide']}/52*2"),("State exemption filings and legal","New York, Connecticut, Massachusetts, Illinois",60000),("Launch marketing","$40K per market, four markets",160000),("Loaner device pool","20 percent of launch seats at $600","=Campuses!B13*0.2*600"),("Insurance deposits","Six sites",24000),("Emporium opening inventory","$25 a seat","=Campuses!B13*25"),("Registration and payments stack","Stripe, HubSpot, roster tooling",30000)]
for i,(a,b,c) in enumerate(items):
    r=5+i; B[f"A{r}"]=a; B[f"B{r}"]=b; B[f"C{r}"]=c; B[f"C{r}"].number_format=USD
    if not isinstance(c,str): B[f"C{r}"].fill=input_fill
B["A12"]="Total"; B["A12"].font=total_font; B["C12"]="=SUM(C5:C11)"; B["C12"].number_format=USD; B["C12"].font=total_font
B["A14"]="Session 2 deposits on plan enrollment"; B["C14"]=f"='Year 1'!E6*Assumptions!$B$11"; B["C14"].number_format=USD
B["A15"]="Deposits cover the launch budget"; B["C15"]='=IF(C14>=C12,"Yes","No")'
widths(B,[36,64,14])

for ws in wb.worksheets:
    ws.freeze_panes="A4" if ws.title!="Assumptions" else "A4"
    ws.sheet_view.showGridLines=True
wb.save("/Users/nancytorvund/alpha-hour/Alpha-Hours-Financial-Model.xlsx")
print("saved", [ws.title for ws in wb.worksheets])
