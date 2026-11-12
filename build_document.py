from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from docx import Document
from docx.shared import Cm,Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).parent
sheets=json.loads((ROOT/'content.json').read_text())
assets=ROOT/'assets';assets.mkdir(exist_ok=True)
def graph(path,g=None):
 fig,ax=plt.subplots(figsize=(5.3,4.2));ax.set_xlim(-8,8);ax.set_ylim(-8,8);ax.set_aspect('equal');ax.set_xticks(range(-8,9));ax.set_yticks(range(-8,9));ax.tick_params(labelsize=7);ax.grid(color='.80',linewidth=.5)
 for name in ['left','bottom']:ax.spines[name].set_position('zero');ax.spines[name].set_linewidth(.8)
 for name in ['right','top']:ax.spines[name].set_visible(False)
 ax.text(7.6,.5,'x');ax.text(.4,7.5,'y')
 if g:
  x=np.linspace(-8,8,1000);y=g['a']*x+g['b'] if g['type']=='line' else g['a']*x*x+g['b']*x+g['c'];ax.plot(x,y,'k',linewidth=1.5)
  if g['type']=='line':pts=[(0,g['b']),(-g['b']/g['a'],0)]
  else:
   h=-g['b']/(2*g['a']);pts=[(h,-1),(h-1,0),(h+1,0),(h-2,3),(h+2,3)]
  for x,y in pts:ax.plot(x,y,'ko',markersize=3)
 fig.tight_layout(pad=.2);fig.savefig(path,dpi=180);plt.close(fig)
graph(assets/'grid.png')
for s in sheets:
 for e in s['exercises']:
  if e['graph']:graph(assets/(s['id']+'.png'),e['graph'])
doc=Document();sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2)
style=doc.styles['Normal'];style.font.name='DejaVu Sans';style.font.size=Pt(12);style.paragraph_format.space_after=Pt(5)
style.paragraph_format.line_spacing=1.05
for n,size in [('Title',17),('Heading 1',16),('Heading 2',13)]:
 st=doc.styles[n];st.font.name='DejaVu Sans';st.font.size=Pt(size);st.font.color.rgb=__import__('docx').shared.RGBColor(0,0,0)
footer=sec.footer.paragraphs[0];footer.alignment=2
footer.add_run('Matematică • clasa a IX-a | ')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
def para(text,bold=False,size=None):
 p=doc.add_paragraph();r=p.add_run(text);r.bold=bold
 if size:r.font.size=Pt(size)
 return p
def keep(p):p.paragraph_format.keep_together=True
for si,s in enumerate(sheets):
 for page in range(2):
  if si or page:doc.add_page_break()
  doc.add_heading(s['topic'],0 if page==0 else 1)
  para(f"Varianta {'I' if s['variant']==1 else 'II'} • Clasa a IX-a"+(' • continuare' if page else ''),True)
  para('Numele și prenumele: ____________________________________')
  if not page:
   para('Data: ______________    Timp de lucru: 45–60 minute')
   para('Total: 60 de puncte. Fără puncte din oficiu. Justificați rezolvările.',size=10)
  for i in range(page*3,page*3+3):
   e=s['exercises'][i];points=sum(p['points'] for p in e['parts'])
   p=para(f'{i+1}. {e["prompt"]} ({points} p)',True);keep(p)
   for part in e['parts']:
    p=para(f'{part["label"]} — {part["points"]} p',size=10);keep(p)
   if e['graph']:
    doc.add_picture(str(assets/'grid.png'),width=Cm(10.1))
   else:
    count=5 if i<3 else (4 if any(x['graph'] for x in s['exercises']) else 6)
    for _ in range(count):para('________________________________________________________________',size=10)
  para('Punctaj obținut: ______ / 60     Nota: ______' if page else 'Continuați pe pagina următoare.',size=10)
doc.add_page_break();doc.add_heading('Rezolvări și barem de corectare și notare',0)
para('Material de pregătire pentru elevii clasei a IX-a. Rezolvările și criteriile de mai jos însoțesc cele zece fișe. Nu se afirmă conformitatea cu un curriculum oficial verificat.')
para('Se acordă punctaj parțial pentru etapele corecte, în limitele indicate. Se acceptă metode alternative corecte și forme echivalente ale răspunsurilor. O eroare de calcul nu se penalizează repetat dacă etapele următoare sunt corecte pentru valoarea obținută și nu simplifică nejustificat sarcina. Nu se acordă puncte din oficiu.')
para('În site, răspunsurile numerice primesc inițial punctaj automat numai pentru rezultatul exact. Profesorul verifică toate etapele, justificările și graficele și ajustează punctajul înainte de nota finală. Rezultatul automat este provizoriu.')
doc.add_heading('Grilă orientativă propusă',1)
para('Intervalele includ toate punctajele întregi de la 0 la 60, fără goluri sau suprapuneri. Grila nu este prezentată drept barem oficial al Republicii Moldova.')
t=doc.add_table(rows=1, cols=2);t.style='Table Grid';t.rows[0].cells[0].text='Punctaj';t.rows[0].cells[1].text='Nota'
for low,high,n in [(0,5,1),(6,11,2),(12,17,3),(18,23,4),(24,29,5),(30,35,6),(36,41,7),(42,47,8),(48,53,9),(54,60,10)]:
 row=t.add_row().cells;row[0].text=f'{low}–{high}';row[1].text=str(n)
for s in sheets:
 doc.add_page_break();doc.add_heading(s['topic'],1);para(f"Varianta {'I' if s['variant']==1 else 'II'} • Rezolvări • Total 60 p",True)
 for i,e in enumerate(s['exercises']):
  if i==3 and s['topic'].startswith('Funcția'):
   doc.add_page_break();doc.add_heading(s['topic']+' • continuare',1);para(f"Varianta {s['variant']} • Rezolvări",True)
  p=doc.add_heading(f'Exercițiul {i+1} • {sum(p["points"] for p in e["parts"])} p',2);p.paragraph_format.keep_with_next=True
  for part in e['parts']:
   p=para(f'{part["label"]}: {part["answer"]}. {part["solution"]} [{part["points"]} p]',size=12);keep(p)
   if part['solution']==part['answer'] and part['points']>2:
    para(f'Metodă sau substituție corectă: {part["points"]//2} p; calcul și rezultat: {part["points"]-part["points"]//2} p.',size=10)
  if e['graph']:doc.add_picture(str(assets/(s['id']+'.png')),width=Cm(10.4))
(ROOT/'downloads'/'Fise_Matematica_IX.docx').parent.mkdir(exist_ok=True)
# Remove inherited title rules for monochrome printing.
for st in doc.styles:
 for el in list(st.element.iter(qn('w:pBdr'))):
  el.getparent().remove(el)
doc.save(ROOT/'downloads'/'Fise_Matematica_IX.docx')
print('DOCX creat')
