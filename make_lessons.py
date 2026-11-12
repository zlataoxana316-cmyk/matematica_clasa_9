"""Conținut original de învățare și verificări formative."""
import json
from pathlib import Path
L=[]
def q(label,answer,hint,explain):return dict(label=label,answer=str(answer),hint=hint,explain=explain)
def lesson(id,topic,title,objective,rule,example,steps,mistake,checks,tool=None):
 L.append(dict(id=id,topic=topic,title=title,objective=objective,rule=rule,example=example,steps=steps,mistake=mistake,checks=checks,tool=tool))
lesson('reale-ordine',0,'Compararea numerelor reale','Compari numere negative, fracții și zecimale.',
 'Pe axa numerelor, numărul din dreapta este mai mare. Dintre două numere negative, este mai mare cel cu modulul mai mic.',
 'Ordonează crescător: −1,2; −5/4; 0,5.',
 ['Transformăm fracția: −5/4 = −1,25.','Comparăm: −1,25 < −1,20 < 0,50.','Rezultă: −5/4 < −1,2 < 0,5.'],
 'La numere negative, un modul mai mare înseamnă un număr mai mic.',
 [q('Care este mai mic: −1,6 sau −3/2? Scrie numărul mai mic.','-1.6','Transformă −3/2 în zecimal.','−3/2 = −1,5, iar −1,6 < −1,5.'),q('Care este mai mare: −7/4 sau −1,8? Scrie numărul mai mare.','-7/4','−7/4 = −1,75.','−1,75 se află la dreapta lui −1,8.'),q('Cât este distanța dintre −3 și 2 pe axă?','5','Calculează |2−(−3)|.','|2−(−3)| = |5| = 5.')])
lesson('reale-calcule',0,'Fracții și ordinea operațiilor','Respecți parantezele și calculezi cu fracții.',
 'Întâi parantezele, apoi puterile, înmulțirile și împărțirile, apoi adunările și scăderile. Operațiile de același rang se fac de la stânga la dreapta.',
 'Calculează 2 − 3·(1/2 − 5/6).',
 ['Aducem la numitor comun: 1/2−5/6 = 3/6−5/6 = −1/3.','Înmulțim: 3·(−1/3) = −1.','Scădem: 2−(−1) = 3.'],
 'Nu adunăm numitorii fracțiilor și nu omitem semnul minus din fața parantezei.',
 [q('Calculează 3/4 − 1/2.','1/4','Folosește numitorul comun 4.','3/4−2/4 = 1/4.'),q('Calculează (−2/3) : (4/9).','-3/2','Înmulțește cu inversa celei de-a doua fracții.','(−2/3)·(9/4) = −18/12 = −3/2.'),q('Calculează 5 − 2·(3−4).','7','Paranteza este −1.','5−2·(−1) = 5+2 = 7.')])
lesson('reale-modul',0,'Modulul și ecuațiile cu modul','Interpretezi modulul ca distanță și lucrezi pe cazuri.',
 '|u| = u pentru u ≥ 0 și |u| = −u pentru u < 0. Dacă c > 0, ecuația |u| = c are cazurile u = c și u = −c.',
 'Rezolvă |2x−3| = 5.',
 ['Primul caz: 2x−3 = 5, deci x = 4.','Al doilea caz: 2x−3 = −5, deci x = −1.','Verificăm: |8−3|=5 și |−2−3|=5. Ambele soluții sunt corecte.'],
 'Ecuația |u| = c nu are soluții dacă c < 0; pentru c = 0 rămâne doar u = 0.',
 [q('Calculează |−8|−|3|.','5','Modulul unui număr negativ este opusul lui.','8−3 = 5.'),q('Scrie soluția mai mică a ecuației |x−2| = 3.','-1','x−2 este 3 sau −3.','Soluțiile sunt 5 și −1; cea mai mică este −1.'),q('Câte soluții reale are |x+1| = −2?','0','Un modul este mereu nenegativ.','Nu poate fi egal cu −2, deci are 0 soluții.')])
lesson('radicali-existenta',1,'Condiții de existență și modul','Stabilești domeniul și simplifici √(u²) corect.',
 'În ℝ, √A există dacă A ≥ 0. Pentru orice u real, √(u²) = |u|.',
 'Simplifică √((x−4)²) pentru x < 4.',
 ['Aplicăm identitatea: √((x−4)²) = |x−4|.','Din x<4 rezultă x−4<0.','Prin definiția modulului: |x−4| = −(x−4) = 4−x.'],
 '√(u²) nu este întotdeauna u. De exemplu, √((−3)²)=3.',
 [q('Pentru √(x−5), care este cel mai mic x admis?','5','Radicandul x−5 trebuie să fie nenegativ.','x−5≥0 ⇔ x≥5. Valoarea minimă admisă este 5.'),q('Calculează √((−7)²).','7','Aplică √(u²)=|u|.','√49 = |−7| = 7.'),q('Pentru x=1, calculează √((x−4)²).','3','Înlocuiește x înainte de calcul.','√((1−4)²) = √9 = 3.')])
lesson('radicali-operatii',1,'Simplificarea și adunarea radicalilor','Extragi factorii pătrați perfecți și reduci radicalii asemenea.',
 'Pentru a,b ≥ 0, √(ab) = √a·√b. Se adună coeficienții numai pentru radicali asemenea.',
 'Simplifică √72 + √8 − √18.',
 ['√72 = √(36·2) = 6√2.','√8 = 2√2, iar √18 = 3√2.','6√2+2√2−3√2 = 5√2.'],
 'În general √(a+b) ≠ √a+√b. √9+√16=7, dar √25=5.',
 [q('În √75 = k√3, cât este k?','5','75 = 25·3.','√75 = 5√3.'),q('În 2√12−√27 = k√3, cât este k?','1','√12=2√3 și √27=3√3.','2·2√3−3√3 = √3, deci k=1.'),q('Calculează √6·√24.','12','Înmulțește radicandele.','√144 = 12.')])
lesson('radicali-rationalizare',1,'Raționalizarea numitorului','Elimini radicalul din numitor prin amplificare.',
 'Amplificăm cu radicalul simplu sau cu expresia conjugată. Folosim (u−v)(u+v)=u²−v². Numitorul inițial trebuie să fie nenul.',
 'Raționalizează 1/(√3−1).',
 ['Amplificăm cu √3+1.','Numitorul devine (√3−1)(√3+1)=3−1=2.','Rezultatul este (√3+1)/2.'],
 'Se amplifică atât numărătorul, cât și numitorul. Conjugata schimbă semnul dintre termeni.',
 [q('În 3/√5 = 3√5/n, cât este n?','5','Amplifică cu √5.','Numitorul √5·√5 este 5.'),q('Cât este (√7−2)(√7+2)?','3','Aplică diferența de pătrate.','7−4 = 3.'),q('În 1/(√5+1) = (√5−1)/n, cât este n?','4','Conjugata este √5−1.','(√5+1)(√5−1)=5−1=4.')])
lesson('puteri-intregi',2,'Exponent zero și exponenți negativi','Calculezi puteri cu exponenți întregi.',
 'Pentru a ≠ 0, a⁰=1 și a⁻ⁿ=1/aⁿ. Semnul unei puteri cu bază negativă depinde de paritatea exponentului.',
 'Calculează (−2)⁻³.',
 ['Baza este nenulă, deci puterea există.','(−2)⁻³ = 1/(−2)³.','(−2)³ = −8, deci rezultatul este −1/8.'],
 'Exponentul negativ nu face automat rezultatul negativ. De exemplu, 2⁻²=1/4.',
 [q('Calculează 7⁰.','1','Baza este nenulă.','Orice bază nenulă la puterea zero este 1.'),q('Calculează 3⁻².','1/9','Ia inversa lui 3².','3⁻²=1/9.'),q('Calculează (−2)⁻².','1/4','Exponentul 2 este par.','1/(−2)²=1/4.')])
lesson('puteri-proprietati',2,'Proprietățile puterilor','Alegi regula potrivită și păstrezi restricțiile.',
 'aᵐ·aⁿ=aᵐ⁺ⁿ; aᵐ:aⁿ=aᵐ⁻ⁿ (a≠0); (aᵐ)ⁿ=aᵐⁿ. Pentru exponenți negativi, baza trebuie să fie nenulă.',
 'Simplifică (a³)²:a⁴, a≠0.',
 ['Ridicăm puterea la putere: (a³)²=a⁶.','Împărțim puteri cu aceeași bază: a⁶:a⁴=a².','Restricția a≠0 rămâne necesară pentru expresia inițială.'],
 'La înmulțirea puterilor se adună exponenții; la puterea unei puteri se înmulțesc.',
 [q('În a³·a⁻⁵=aᵏ (a≠0), cât este k?','-2','Adună exponenții.','3+(−5)=−2.'),q('În (b²)⁴=bᵏ, cât este k?','8','Înmulțește exponenții.','2·4=8.'),q('În c⁷:c³=cᵏ (c≠0), cât este k?','4','Scade exponenții.','7−3=4.')])
lesson('puteri-comparare',2,'Compararea puterilor și aplicații','Aduci puterile la aceeași bază și modelezi creșterea.',
 'Pentru a>1, puterea cu exponent mai mare este mai mare. Pentru 0<a<1, ordinea se inversează.',
 'Compară 2⁸ și 4³.',
 ['Scriem 4³=(2²)³=2⁶.','Baza comună 2 este mai mare decât 1.','Deoarece 8>6, rezultă 2⁸>4³.'],
 'La o bază cuprinsă între 0 și 1, nu folosim aceeași ordine a exponenților ca la baza >1.',
 [q('Cât este raportul 2⁸/4³?','4','Transformă 4³ în 2⁶.','2⁸/2⁶=2²=4.'),q('O cantitate de 50 se dublează de 3 ori. Cât devine?','400','Calculează 50·2³.','50·8=400.'),q('Care este mai mare: (1/2)² sau (1/2)³? Scrie valoarea mai mare.','1/4','Pentru 0<a<1, creșterea exponentului micșorează puterea.','1/4 > 1/8.')])
lesson('liniara-valori',3,'Valori și apartenență la grafic','Calculezi f(x) și verifici un punct.',
 'Pentru f(x)=ax+b, a≠0, punctul (x₀;y₀) este pe grafic dacă și numai dacă y₀=f(x₀).',
 'Pentru f(x)=2x−3, verifică A(2;1).',
 ['Înlocuim x=2: f(2)=2·2−3.','Obținem f(2)=1.','Ordonata lui A este 1, deci A aparține graficului.'],
 'Prima coordonată este x, a doua este y. Nu le inversa la substituție.',
 [q('Pentru f(x)=3x−2, calculează f(0).','-2','Înlocuiește x cu 0.','3·0−2=−2.'),q('Pentru f(x)=3x−2, calculează f(−1).','-5','3·(−1)−2.','−3−2=−5.'),q('Punctul (2;y) este pe graficul f(x)=3x−2. Cât este y?','4','y=f(2).','3·2−2=4.')])
lesson('liniara-grafic',3,'Grafic, zero și monotonie','Explorezi efectul coeficienților a și b.',
 'Graficul este o dreaptă. Intersecțiile sunt (0;b) și (−b/a;0). Dacă a>0 funcția este strict crescătoare; dacă a<0 este strict descrescătoare.',
 'Studiază f(x)=2x−4.',
 ['Cu Oy: x=0 ⇒ y=−4, deci (0;−4).','Cu Ox: 2x−4=0 ⇒ x=2, deci (2;0).','Dreapta trece prin cele două puncte. Este crescătoare; f(x)<0 pentru x<2 și f(x)>0 pentru x>2.'],
 'La o dreaptă descrescătoare, semnul este pozitiv la stânga zeroului și negativ la dreapta.',
 [q('Care este zeroul funcției f(x)=2x−6?','3','Rezolvă 2x−6=0.','2x=6, deci x=3.'),q('Pentru f(x)=−3x+6, care este ordonata intersecției cu Oy?','6','Înlocuiește x cu zero.','f(0)=6.'),q('Pentru f(x)=−3x+6, cât este f(3)?','-3','Calculează −3·3+6.','−9+6=−3, deci la x=3 funcția este negativă.')],tool='line')
lesson('liniara-model',3,'Determinarea formulei și probleme','Găsești coeficienții și construiești un model liniar.',
 'Din două puncte cu abscise distincte, a=(y₂−y₁)/(x₂−x₁), apoi b=y₁−ax₁. Verificăm a≠0 dacă cerem o funcție de gradul I.',
 'O livrare costă 10 lei fix și 4 lei pentru fiecare kilometru.',
 ['Notăm distanța cu d≥0.','Costul este C(d)=4d+10.','Pentru 5 km: C(5)=4·5+10=30 lei.'],
 'Într-o problemă practică precizează unitățile și domeniul, de exemplu distanță nenegativă.',
 [q('O dreaptă trece prin (1;3) și (3;7). Care este a?','2','(7−3)/(3−1).','4/2=2.'),q('Dacă a=2 și f(1)=3, cât este b?','1','2·1+b=3.','b=3−2=1.'),q('Pentru C(d)=4d+10, ce distanță corespunde costului de 42 lei?','8','Rezolvă 4d+10=42.','4d=32 ⇒ d=8 km.')])
lesson('patratica-radacini',4,'Rădăcini și intersecții','Calculezi discriminantul și zerourile.',
 'Pentru f(x)=ax²+bx+c, a≠0: Δ=b²−4ac. Dacă Δ≥0, x₁,₂=(−b±√Δ)/(2a). Intersecția cu Oy este (0;c).',
 'Determină rădăcinile lui x²−5x+6.',
 ['a=1, b=−5, c=6; Δ=25−24=1.','x₁=(5−1)/2=2, x₂=(5+1)/2=3.','Intersecțiile cu Ox sunt (2;0), (3;0), iar cu Oy este (0;6).'],
 'Pentru Δ<0 nu există rădăcini reale. Semnul lui b trebuie păstrat la înlocuirea în formulă.',
 [q('Calculează Δ pentru x²−6x+8.','4','b²−4ac = 36−32.','Δ=4.'),q('Care este rădăcina mai mică a lui x²−6x+8?','2','(6−√4)/2.','(6−2)/2=2.'),q('Care este rădăcina mai mare a lui x²−6x+8?','4','(6+√4)/2.','(6+2)/2=4.')])
lesson('patratica-varf',4,'Vârf, simetrie și extrem','Explorezi parabola și afli minimul sau maximul.',
 'Vârful este V(−b/(2a);−Δ/(4a)). Axa de simetrie este x=−b/(2a). Pentru a>0 avem minim; pentru a<0 avem maxim.',
 'Studiază f(x)=x²−4x+3.',
 ['Completăm pătratul: f(x)=(x−2)²−1.','Vârful este V(2;−1), iar axa este x=2.','Minimul este −1 la x=2. Funcția descrește pe (−∞;2] și crește pe [2;+∞).'],
 'Abscisa vârfului este locul unde se atinge extremul; ordonata este valoarea extremă.',
 [q('Pentru f(x)=x²−6x+5, care este abscisa vârfului?','3','−b/(2a)=6/2.','xV=3.'),q('Care este valoarea minimă a lui x²−6x+5?','-4','Calculează f(3) sau completează pătratul.','f(3)=9−18+5=−4.'),q('Care este valoarea maximă a lui −(x−2)²+7?','7','Pătratul este nenegativ.','−(x−2)²≤0, deci maximul este 7 la x=2.')],tool='parabola')
lesson('patratica-semn',4,'Semnul funcției și aria maximă','Combini rădăcinile, semnul și un model geometric.',
 'Cu două rădăcini distincte, semnul este cel al lui a în exteriorul rădăcinilor și opus în interior. Pentru aria unui dreptunghi cu perimetru fix folosim o funcție de gradul al II-lea.',
 'Un dreptunghi are perimetrul 20 m. Găsește aria maximă.',
 ['Dacă o latură este x, cealaltă este 10−x, cu 0<x<10.','Aria A(x)=x(10−x)=−(x−5)²+25.','Aria maximă este 25 m², la dimensiunile 5 m × 5 m.'],
 'Domeniul geometric contează: laturile trebuie să fie pozitive. Un vârf trebuie interpretat în context.',
 [q('Calculează f(3) pentru f(x)=(x−2)(x−4).','-1','3 este între cele două rădăcini.','(3−2)(3−4)=1·(−1)=−1.'),q('Un dreptunghi are perimetrul 24 m. Cât este latura pătratului cu același perimetru?','6','Împarte perimetrul la 4.','24/4=6 m.'),q('Care este aria maximă a unui dreptunghi cu perimetrul 24 m?','36','Aria maximă se obține la pătrat.','6·6=36 m².')])
assert len(L)==15 and all(len(l['checks'])==3 for l in L)
Path(__file__).with_name('lessons.json').write_text(json.dumps(L,ensure_ascii=False,indent=2))
print('15 lecții, 45 verificări formative')
