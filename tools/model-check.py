"""Reference model for the Alpha Hours session-based plan, staggered rollout (Aug 27, 2026 revision).
Rollout: S2 NYC only; S3 + Greenwich, Boston A, Boston B; S4 + Chicago (517) + Miami, Palm Beach, Miami Beach; S5 same; S1 Fall 2027 national."""
import math
P=4500; TB=150; MOT=40; SUP=15; SNACK=30; SHOW_CHILD=5; PROC=round(P*0.03); MKT=60
VARS=TB+MOT+SUP+SNACK+SHOW_CHILD+PROC+MKT; VAR=VARS*5
GUIDE=50000; FIXED=75000+50000+45000+8000+2000*5; CENTRAL=875000
CAMPS=[("New York, 180 Maiden Lane",100,2,False),("New York, 156 William Street",30,2,True),
       ("Greenwich (Armonk)",80,3,False),("Boston A",40,3,False),("Boston B",100,3,False),
       ("Chicago",517,4,False),("Miami",150,4,False),("Palm Beach",60,4,False),("Miami Beach",50,4,False)]
def fixed_of(c): return FIXED-50000 if c[3] else FIXED
def site(c):
    s=c[1]; enr=s*4; rev=enr*P*5; g=math.ceil(s/10); return dict(name=c[0],seats=s,enr=enr,rev=rev,var=enr*VAR,g=g,gc=g*GUIDE,fx=fixed_of(c),prof=rev-enr*VAR-g*GUIDE-fixed_of(c))
rows=[site(c) for c in CAMPS]
print(f"{'campus':30} seats enr   rev    var   g  gc    fx    profit  m")
for r in rows: print(f"{r['name']:30} {r['seats']:5} {r['enr']:5} {r['rev']/1e6:6.2f} {r['var']/1e6:5.2f} {r['g']:3} {r['gc']/1e6:5.2f} {r['fx']/1e6:5.2f} {r['prof']/1e6:6.2f} {r['prof']/r['rev']:.1%}")
def tot(l): return {k:sum(r[k] for r in l) for k in ('seats','enr','rev','var','gc','fx','prof','g')}
for lab,sess in (("S2 footprint (NYC)",2),("S3 footprint (+Greenwich, Boston)",3),("S4/S5 footprint (+Chicago, Florida)",4)):
    T=tot([r for r,c in zip(rows,CAMPS) if c[2]<=sess]); print(lab, {k:(round(v/1e6,2) if k in('rev','var','gc','fx','prof') else v) for k,v in T.items()}, f"margin {T['prof']/T['rev']:.1%}", "per-session rev", round(T['rev']/5/1e6,2), "profit", round(T['prof']/5/1e6,2), "net/yr", round((T['prof']-CENTRAL)/1e6,2))
RAMP=[0.6,0.75,0.9,1.0]
def session(n, case):
    open_=[(r,c) for r,c in zip(rows,CAMPS) if c[2]<=n]
    enr=rev=var=gc=fx=0; g=0
    for r,c in open_:
        k=n-c[2]
        f={"cap":1.0,"plan":RAMP[min(k,3)],"floor":0.25}[case]
        e=round(r['seats']*4*f); enr+=e; rev+=e*P; var+=e*VARS; gg=math.ceil(r['seats']*f/10); g+=gg; gc+=gg*GUIDE/5; fx+=fixed_of(c)/5
    return dict(enr=enr,rev=rev,var=var,g=g,gc=gc,fx=fx,prof=rev-var-gc-fx,open=len(open_))
for case in ("plan","cap","floor"):
    T={k:0 for k in ('enr','rev','var','gc','fx','prof')}
    for n in (2,3,4,5):
        s=session(n,case)
        for k in T: T[k]+=s[k]
        print(f"  {case:5} S{n}: campuses {s['open']} enr {s['enr']:5} rev {s['rev']/1e6:6.2f} var {s['var']/1e6:5.2f} guides {s['g']:3} gc {s['gc']/1e6:5.2f} fx {s['fx']/1e6:5.2f} profit {s['prof']/1e6:6.2f} m {s['prof']/s['rev']:.0%}")
    print(f"{case} Y1: rev {T['rev']/1e6:.2f} var {T['var']/1e6:.2f} gc {T['gc']/1e6:.2f} fx {T['fx']/1e6:.2f} site profit {T['prof']/1e6:.2f} net {(T['prof']-CENTRAL)/1e6:.2f}")
contrib=(P-VARS)*5; print("contribution/yr", contrib, "after guides", contrib-1250, "min cost", FIXED+2*GUIDE, "break-even", (FIXED+2*GUIDE)/contrib)
E=tot(rows); print("== fill sens, expanded footprint annual (seats", E['seats'], ")")
for f in (.25,.5,.75,1):
    enr=sum(round(r['seats']*4*f) for r in rows); rev=enr*P*5; var=enr*VAR; gc=sum(math.ceil(r['seats']*f/10) for r in rows)*GUIDE; fx=E['fx']; prof=rev-var-gc-fx
    print(f"{f:.0%}: enr {enr} rev {rev/1e6:.1f} profit {prof/1e6:.1f} net {(prof-CENTRAL)/1e6:.1f} m {prof/rev:.0%}")
print("== price sens at capacity")
for p in (3500,4000,4500,5000,5500):
    enr=E['enr']; vs=VARS-PROC+round(p*.03); rev=enr*p*5; prof=rev-enr*vs*5-E['gc']-E['fx']; print(f"{p}: rev {rev/1e6:.1f} profit {prof/1e6:.1f}")
print("every $500 at capacity:", E['enr']*500*5*(1-.03)/1e6)
# lanes
enr=E['enr']
for lab,sh in (("Stay",.7),("Considering",.15),("Path to yes",.05),("Current",.10)):
    fam=round(enr*sh); rev=fam*P*5*(0.95 if lab=="Current" else 1); print(f"lane {lab}: {fam} fam, ${rev/1e6:.1f}M")
for c in (.04,.08,.12): print(f"feeder {c:.0%}: {round(enr*c)} enrollments, ${round(enr*c)*240000/1e6:.0f}M")
# additions
print("break week Apr 2027 on", E['seats'], "seats:", E['seats']*4500/1e6, "M; evening block ML+Greenwich S4-S5:", 180*2*4500*2/1e6, "M inside Y1; full year", 180*2*4500*5/1e6)
# national
nat_seats=2977; nat_enr=nat_seats*4; nat_camp=40
nat_rev=nat_enr*P*5; nat_prof=nat_rev-nat_enr*VAR-math.ceil(nat_seats/10)*GUIDE-nat_camp*FIXED
print("NATIONAL", nat_seats, nat_enr, "rev", nat_rev/1e6, "site profit", nat_prof/1e6, f"{nat_prof/nat_rev:.0%}", "net", (nat_prof-4e6)/1e6, "; wave S1 fall 2027 adds seats", nat_seats-E['seats'], "enrolled", (nat_seats-E['seats'])*4, "run rate", (nat_seats-E['seats'])*4*P*5/1e6)
for c in (.04,.08,.12): print(f"national feeder {c:.0%}: ${round(nat_enr*c)*240000/1e6:.0f}M")
m=E['prof']/E['rev']; print("expanded margin", m)
for y,kf,ef,bf in (("Y2",.75,.4,.6),("Y3",.9,.7,.8)):
    k8=nat_rev*kf; ev=nat_rev*.5*ef; bw=nat_seats*2*4500*bf; totr=k8+ev+bw; print(y, "k8", k8/1e6, "evening", ev/1e6, "break", bw/1e6, "total", totr/1e6, "net", (totr*m-4e6)/1e6)
# launch budget NYC
g=sum(r['g'] for r in rows[:2]); print("NYC launch budget: training", (g+2)*GUIDE/52*2, "filing 15000 marketing 40000 devices", 130*.2*600, "insurance 8000 emporium", 130*25, "stack 30000 total", (g+2)*GUIDE/52*2+15000+40000+130*.2*600+8000+130*25+30000, "; S2 deposits plan", round(520*.6)*500)
