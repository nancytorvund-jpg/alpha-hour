import math
P=4500
# per child per session
TB=150; MOT=40; SUP=15; SNACK=30; SHOW_CHILD=5; PROC=round(P*0.03); MKT=60
VARS=TB+MOT+SUP+SNACK+SHOW_CHILD+PROC+MKT; VAR=VARS*5
SHOW_CAMPUS=2000*5  # per campus per year
GUIDE=50000; FIXED_BASE=178000; FIXED=FIXED_BASE+SHOW_CAMPUS; CENTRAL=875000
print("var per session", VARS, "per year", VAR, "fixed/campus", FIXED)
def fixed_of(seats): return FIXED-50000 if seats==30 else FIXED
def site(seats):
    enr=seats*4; rev=enr*P*5; g=math.ceil(seats/10); cost_var=enr*VAR; gc=g*GUIDE; fx=fixed_of(seats)
    prof=rev-cost_var-gc-fx; return dict(seats=seats,enr=enr,rev=rev,var=cost_var,g=g,gc=gc,fx=fx,prof=prof,m=prof/rev)
names=[("NYC Maiden Lane",100),("NYC William St",30),("Greenwich",80),("Boston A",40),("Boston B",100),("Chicago launch",94),("Chicago 517",517)]
rows={n:site(s) for n,s in names}
for n,r in rows.items(): print(f"{n:16} seats {r['seats']:4} enr {r['enr']:5} rev {r['rev']/1e6:6.2f} var {r['var']/1e6:5.2f} guides {r['g']:3} gc {r['gc']/1e6:5.2f} fx {r['fx']/1e6:5.2f} profit {r['prof']/1e6:6.2f} m {r['m']:.1%}")
launch=[rows[n] for n,_ in names if n!="Chicago 517"]; exp=[rows[n] for n,_ in names if n!="Chicago launch"]
def tot(l): return {k:sum(r[k] for r in l) for k in ('seats','enr','rev','var','gc','fx','prof','g')}
L=tot(launch); E=tot(exp)
for lab,T in (("LAUNCH",L),("EXPANDED",E)): print(lab, {k:(round(v/1e6,2) if k in('rev','var','gc','fx','prof') else v) for k,v in T.items()}, "margin", f"{T['prof']/T['rev']:.1%}", "per-session rev", round(T['rev']/5/1e6,2), "per-session profit", round(T['prof']/5/1e6,2))
print("NYC alone profit", (rows["NYC Maiden Lane"]['prof']+rows["NYC William St"]['prof'])/1e6)
print("expanded net", (E['prof']-CENTRAL)/1e6)
def sess(l, fill, price=P):
    enr=sum(r['enr']*fill for r in l); rev=enr*price; var=enr*(VAR/5 - PROC + round(price*0.03))
    g=sum(math.ceil(r['seats']*fill/10) for r in l); gc=g*GUIDE/5; fx=sum(fixed_of(r['seats']) for r in l)/5
    return dict(enr=enr,rev=rev,var=var,g=g,gc=gc,fx=fx,prof=rev-var-gc-fx)
for lab,fills in (("CAP",[1,1,1,1]),("PLAN",[.6,.75,.9,1]),("FLOOR",[.25]*4)):
    T={k:0 for k in ('enr','rev','var','gc','fx','prof')}
    for i,f in enumerate(fills):
        s=sess(launch if i==0 else exp, f)
        for k in T: T[k]+=s[k]
        print(f"  {lab} S{i+2} fill {f:.0%}: enr {s['enr']:.0f} rev {s['rev']/1e6:.2f} var {s['var']/1e6:.2f} guides {s['g']} gc {s['gc']/1e6:.2f} fx {s['fx']/1e6:.2f} profit {s['prof']/1e6:.2f} m {s['prof']/s['rev']:.0%}")
    print(lab,"Y1:", {k:round(v/1e6,2) for k,v in T.items()}, "net", round((T['prof']-CENTRAL)/1e6,2))
contrib=(P-VARS)*5; print("contribution/yr", contrib, "after guides", contrib-1250, "break-even", (FIXED+2*GUIDE)/contrib, "min cost", FIXED+2*GUIDE)
print("== fill sens annual")
for f in (.25,.5,.75,1):
    s=sess(exp,f); print(f"{f:.0%}: enr {s['enr']:.0f} rev {s['rev']*5/1e6:.1f} profit {s['prof']*5/1e6:.1f} net {(s['prof']*5-CENTRAL)/1e6:.1f} m {s['prof']/s['rev']:.0%}")
print("== price sens")
for p in (3500,4000,4500,5000,5500):
    s=sess(exp,1,p); print(f"{p}: rev {s['rev']*5/1e6:.1f} profit {s['prof']*5/1e6:.1f}")
# national: previous site profit 223.3M with old model; recompute: 11,908 enrolled, seats 2977, ~40 campuses
nat_enr=11908; nat_seats=2977; nat_camp=40
nat_rev=nat_enr*P*5; nat_var=nat_enr*VAR; nat_gc=math.ceil(nat_seats/10)*GUIDE; nat_fx=nat_camp*FIXED
nat_prof=nat_rev-nat_var-nat_gc-nat_fx; print("NATIONAL rev", nat_rev/1e6, "profit", nat_prof/1e6, f"{nat_prof/nat_rev:.0%}", "net", (nat_prof-4e6)/1e6)
# cost lines at expanded capacity per year
e=E['enr']; print("== expanded cost lines/yr: timeback",e*TB*5/1e6,"motivation",e*MOT*5/1e6,"supplies",e*SUP*5/1e6,"snacks",e*SNACK*5/1e6,"showcase child",e*SHOW_CHILD*5/1e6,"showcase campus",6*SHOW_CAMPUS/1e6,"processing",e*PROC*5/1e6,"marketing",e*MKT*5/1e6,"guides",E['gc']/1e6,"fixed base",6*FIXED_BASE/1e6-50000/1e6)
# per 100-seat campus cost lines per year
s=rows["NYC Maiden Lane"]; e=400
print("== 100-seat campus/yr: rev",s['rev']/1e6,"timeback",e*750,"motivation",e*200,"supplies",e*75,"snacks",e*150,"showcase",e*25+10000,"processing",e*675,"marketing",e*300,"guides",s['gc'],"lead guide 75000 coordinator 50000 facility 45000 insurance 8000 -> profit",s['prof'],f"{s['m']:.1%}")
# Year 2/3 view: previous used 83% site margin approx; recompute margin at expanded ~
print("expanded margin", E['prof']/E['rev'])
y2=271e6; y3=356e6; print("Y2 net ~", (y2*E['prof']/E['rev']-4e6)/1e6, "Y3 net ~", (y3*E['prof']/E['rev']-4e6)/1e6)
print("Y1 network plan site profit ~ 94M x margin:", 94*E['prof']/E['rev'])
