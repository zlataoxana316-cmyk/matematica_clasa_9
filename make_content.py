import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).parent
sheets=[]
def part(label,answer,points,solution=None,manual=False):

 if isinstance(answer,(int,float)): answer=str(Fraction(answer).limit_denominator(100000))
 return dict(label=label,answer=str(answer),points=points,solution=solution or str(answer),manual=manual)
def ex(prompt,*parts,graph=None):
 return dict(prompt=prompt,parts=list(parts),graph=graph)
def sheet(topic,v,items):
 assert [sum(p['points'] for p in e['parts']) for e in items]==[4,6,8,10,14,18]
 sheets.append(dict(id=f't{len(sheets)//2+1}v{v}',topic=topic,variant=v,minutes=60,exercises=items))
for v in [1,2]:
 k=v
 # Numeric values deliberately different; same operations and rubric.
 a,b=(-3,2) if v==1 else (-4,3)
 nums='−1,5; −7/4; 0; 2/3' if v==1 else '−2,5; −11/4; 0; 3/4'
 order='−7/4 < −1,5 < 0 < 2/3' if v==1 else '−11/4 < −2,5 < 0 < 3/4'
 r=4 if v==1 else 6
 sheet('Operații cu numere reale',v,[
 ex('Ordonați crescător numerele: '+nums+'. Justificați compararea numerelor negative.',part('Ordinea și justificarea',order,4,'Convertire la zecimale: 2 p; ordonare corectă: 2 p.',True)),
 ex(f'Calculați: a) |{a}| + |{b}|; b) |{a} − {b}| − |{b}|.',part('a)',abs(a)+abs(b),3),part('b)',abs(a-b)-abs(b),3)),
 ex(f'Calculați: a) {k}/2 + 0,75; b) (−{k+2}/4) : 1,5.',part('a)',k/2+.75,4,'0,75 = 3/4 (1 p); numitor comun (1 p); rezultat (2 p).'),part('b)',-(k+2)/6,4,'1,5 = 3/2 (1 p); înmulțire cu inversa (1 p); rezultat (2 p).')),
 ex(f'Calculați E = {r} − 2 · [3 − (−1,5 + 1/2)]. Arătați ordinea operațiilor.',part('Valoarea parantezei pătrate',4,4,'−1,5 + 1/2 = −1 (2 p); 3 − (−1) = 4 (2 p).'),part('E',r-8,6,'Înmulțirea 2·4 = 8 (3 p); scăderea finală (3 p).')),
 ex(f'Rezolvați ecuația |2x − {k}| = {k+4}. Explicați de ce sunt două cazuri.',part('Soluția mai mică',-2,5,'2x − k = −(k+4); izolarea lui x: 3 p; rezultat: 2 p.'),part('Soluția mai mare',k+2,5,'2x − k = k+4; izolarea lui x: 3 p; rezultat: 2 p.'),part('Justificare și verificare','Două cazuri ale modulului; ambele soluții verificate.',4,manual=True)),
 ex(f'Un rezervor este plin în proporție de 3/4. Se consumă {10*k} litri, apoi se adaugă {4*k} litri. Rezervorul este acum plin în proporție de 3/5. Determinați capacitatea și cantitatea finală.',part('Ecuația modelului','3C/4 − '+str(10*k)+' + '+str(4*k)+' = 3C/5',6,'Diferența fracțiilor este 3/20; pierderea netă este '+str(6*k)+' l.',True),part('Capacitatea în litri',40*k,8,'3C/20 = '+str(6*k)+' (4 p); C = '+str(40*k)+' (4 p).'),part('Cantitatea finală în litri',24*k,4))])
for v in [1,2]:
 k=v; A=12 if v==1 else 27; root=2 if v==1 else 3
 sheet('Radicali',v,[
 ex(f'Determinați condiția de existență în ℝ a expresiei √(x − {k+2}).',part('Condiția și mulțimea valorilor',f'x ≥ {k+2}',4,'Radicand nenegativ: 2 p; x ≥ '+str(k+2)+': 2 p.',True)),
 ex(f'Extrageți factorii de sub radical: a) √{A}; b) √{A*4}.',part('a) coeficientul lui √3',root,3,f'{A} = {root**2}·3 (1 p); {root}√3 (2 p).'),part('b) coeficientul lui √3',2*root,3,f'{A*4} = {(2*root)**2}·3 (1 p); {2*root}√3 (2 p).')),
 ex(f'a) Introduceți factorul {k+1} sub radical în ({k+1})√5. b) Simplificați √((x − {k})²), știind că x < {k}.',part('a) radicandul',5*(k+1)**2,4),part('b) expresia simplificată',f'{k} − x',4,f'√((x−{k})²) = |x−{k}| (2 p); pentru x<{k}, rezultă {k}−x (2 p).',True)),
 ex(f'Simplificați √{A*4} + √{A} − {k}√3 și calculați (√{A})·√3.',part('Coeficientul lui √3 în sumă',3*root-k,6,'Extragerea factorilor (3 p); adunarea coeficienților (3 p).'),part('Produsul',3*root,4)),
 ex(f'Raționalizați: a) {k+1}/√5; b) 1/(√{k+3} − 1).',part('a) rezultatul',f'{k+1}√5/5',6,'Amplificare cu √5 (3 p); simplificare (3 p).',True),part('b) rezultatul',f'(√{k+3}+1)/{k+2}',8,'Conjugata (3 p); numitor '+str(k+2)+' (3 p); rezultat (2 p).',True)),
 ex(f'Pentru x ≥ {k}, considerați E(x) = √((x − {k})²) + (x − {k})/(√{k+3} + 1). a) Simplificați E(x). b) Calculați E({k+1}).',part('a) justificarea și forma simplificată',f'(x−{k})(1+(√{k+3}−1)/{k+2})',10,'Modul și utilizarea lui x≥k (4 p); raționalizare (4 p); factorizare (2 p).',True),part('b) valoarea exactă',f'1+(√{k+3}−1)/{k+2}',8,'Substituție (4 p); rezultat exact (4 p).',True))])
for v in [1,2]:
 b=v+1
 sheet('Puteri',v,[
 ex(f'Calculați: a) (−{b})²; b) {b}⁰.',part('a)',b*b,2),part('b)',1,2)),
 ex(f'Calculați: a) {b}⁻²; b) (−{b})⁻³.',part('a)',1/b**2,3,'Inversa puterii pozitive (1 p); rezultat (2 p).'),part('b)',-1/b**3,3,'Semnul negativ (1 p); inversa (1 p); rezultat (1 p).')),
 ex(f'Simplificați și calculați: a) {b}³·{b}⁻¹; b) ({b}²)³ : {b}⁴.',part('a)',b*b,4,'Adunarea exponenților (2 p); rezultat (2 p).'),part('b)',b*b,4,'Înmulțirea exponenților (1 p); scăderea (1 p); rezultat (2 p).')),
 ex('Pentru a ≠ 0 și b ≠ 0, simplificați (a³b⁻²)² : (a⁴b⁻¹). Indicați exponenții finali și explicați restricțiile.',part('Exponentul lui a',2,3),part('Exponentul lui b',-3,3),part('Forma finală și restricțiile','a²/b³; a ≠ 0, b ≠ 0 în expresia inițială.',4,'Ridicare la putere: 2 p; împărțire și restricții: 2 p.',True)),
 ex(f'Comparați {b}⁸ și ({b*b})³. Apoi determinați cel mai mic întreg n pentru care {b}ⁿ > {b**4}.',part('Comparația justificată',f'{b}⁸ > {b}⁶',8,'Scriere în aceeași bază (4 p); compararea exponenților deoarece baza>1 (4 p).',True),part('n minim',5,6,'n>4 (3 p); cel mai mic întreg este 5 (3 p).')),
 ex(f'O cultură conține inițial {100*b} celule, iar numărul se dublează la fiecare oră. a) Scrieți N(t). b) După câte ore sunt {100*b*32} celule? c) Ce fracție din numărul de la ora 5 reprezintă numărul de la ora 2?',part('a) modelul',f'N(t)={100*b}·2^t, t întreg nenegativ',6,'Valoare inițială (2 p); factor de dublare (2 p); model (2 p).',True),part('b) numărul de ore',5,6,'2^t=32 (3 p); t=5 (3 p).'),part('c) fracția',.125,6,'Raportul 2²/2⁵ (3 p); 2⁻³=1/8 (3 p).'))])
for v in [1,2]:
 a=2 if v==1 else 3; b=-4 if v==1 else -3; z=-b/a
 graph={'type':'line','a':a,'b':b}
 sheet('Funcția de gradul I',v,[
 ex(f'Fie f(x) = {a}x {b:+}. Calculați f(0) și f(2).',part('f(0)',b,2),part('f(2)',2*a+b,2)),
 ex(f'Pentru f(x) = {a}x {b:+}, verificați dacă A(1; {a+b}) și B(2; {2*a+b+1}) aparțin graficului.',part('A și justificarea',f'Da, f(1)={a+b}',3,manual=True),part('B și justificarea',f'Nu, f(2)={2*a+b} ≠ {2*a+b+1}',3,manual=True)),
 ex(f'Pentru f(x) = {a}x {b:+}, determinați zeroul și intersecțiile cu axele.',part('Zeroul',z,4,'Ecuația ax+b=0 (2 p); soluție (2 p).'),part('Intersecțiile',f'Ox: ({z:g}; 0); Oy: (0; {b})',4,'Câte 2 p pentru fiecare punct.',True)),
 ex(f'Reprezentați grafic f(x) = {a}x {b:+}. Precizați monotonia.',part('Graficul','Dreapta prin intersecțiile cu axele.',8,'Axe și scară (2 p); două puncte corecte (4 p); dreapta (2 p).',True),part('Monotonia','Strict crescătoare pe ℝ deoarece a>0.',2,manual=True),graph=graph),
 ex(f'Determinați g(x)=mx+n, m≠0, știind că g(1)={v+2} și g(3)={5*v+2}. Stabiliți semnul lui g.',part('m',2*v,4),part('n',2-v,4),part('Semnul',f'Zero la {(v-2)/(2*v):g}; negativ la stânga, pozitiv la dreapta.',6,'Zero (2 p); cele două intervale (4 p).',True)),
 ex(f'Un taxi A solicită {8+v} lei pornirea și {3+v} lei/km. Taxiul B solicită {14+v} lei pornirea și {2+v} lei/km. a) Scrieți costurile. b) La ce distanță costurile sunt egale? c) Pentru ce distanțe este A mai ieftin?',part('a) modelele',f'A(d)={8+v}+{3+v}d; B(d)={14+v}+{2+v}d; d≥0.',6,'Câte 3 p pentru un model corect, cu domeniu.',True),part('b) distanța în km',6,6,'Egalarea (3 p); rezolvarea (3 p).'),part('c) intervalul justificat','0 ≤ d < 6 km',6,'Inecuație (2 p); rezolvare (2 p); domeniu (2 p).',True))])
for v in [1,2]:
 h=v+1;c=h*h-1; graph={'type':'parabola','a':1,'b':-2*h,'c':c}
 sheet('Funcția de gradul al II-lea',v,[
 ex(f'Fie f(x)=x²−{2*h}x+{c}. Calculați f(0) și f({h}).',part('f(0)',c,2),part(f'f({h})',-1,2)),
 ex(f'Determinați rădăcinile lui f(x)=x²−{2*h}x+{c}.',part('Rădăcina mai mică',h-1,3,'Δ=4 (1 p); formula și rădăcina (2 p).'),part('Rădăcina mai mare',h+1,3,'Formula (1 p); rădăcina (2 p).')),
 ex(f'Pentru f(x)=x²−{2*h}x+{c}, determinați intersecțiile cu axele și axa de simetrie.',part('Intersecțiile',f'Ox: ({h-1};0), ({h+1};0); Oy: (0;{c})',6,'Câte 2 p pentru fiecare punct.',True),part('Axa',h,2,'Axa are ecuația x='+str(h)+'.')),
 ex(f'Reprezentați grafic f(x)=x²−{2*h}x+{c}, marcând vârful și cel puțin alte patru puncte.',part('Graficul',f'V({h};−1), rădăcinile și două puncte simetrice.',10,'Axe și scară (2 p); vârf (2 p); patru puncte (4 p); curbă corectă (2 p).',True),graph=graph),
 ex(f'Pentru f(x)=x²−{2*h}x+{c}, stabiliți monotonia, semnul și valoarea minimă.',part('Monotonia',f'Descrescătoare pe (−∞;{h}], crescătoare pe [{h};+∞).',4,'Câte 2 p pe interval.',True),part('Semnul',f'Pozitivă pe (−∞;{h-1})∪({h+1};+∞), negativă pe ({h-1};{h+1}), nulă la {h-1} și {h+1}.',6,'Exterior (2 p); interior (2 p); zerouri (2 p).',True),part('Minimul',-1,4,'Forma (x−h)²−1 (2 p); minimul −1 la x=h (2 p).')),
 ex(f'Un dreptunghi are perimetrul {4*(h+2)} m. Notăm o latură cu x. a) Exprimați aria A(x) și domeniul geometric. b) Determinați aria maximă și dimensiunile corespunzătoare.',part('a) modelul',f'A(x)=x({2*(h+2)}−x); 0<x<{2*(h+2)}.',6,'Cealaltă latură (2 p); produs (2 p); domeniu (2 p).',True),part('b) aria maximă', (h+2)**2,6,'Vârf sau completarea pătratului (3 p); valoare (3 p).'),part('b) dimensiunile',f'{h+2} m × {h+2} m',6,'Valoarea x (2 p); cealaltă latură (2 p); interpretare ca pătrat (2 p).',True))])
(ROOT/'content.json').write_text(json.dumps(sheets,ensure_ascii=False,indent=2))
print(len(sheets),'fișe',sum(len(s['exercises']) for s in sheets),'exerciții')
