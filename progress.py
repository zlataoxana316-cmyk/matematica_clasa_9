"""Calcule independente pentru rapoarte individuale și catalog."""
import json
TOPICS=['Operații cu numere reale','Radicali','Puteri','Funcția de gradul I','Funcția de gradul al II-lea']
def report(c,student,content,lessons,grade):
 uid=student['id'];events=[dict(r) for r in c.execute('SELECT lesson,item,correct,created FROM lesson_events WHERE user_id=? ORDER BY id',(uid,))]
 mastered={(e['lesson'],e['item']) for e in events if e['correct']}
 attempts=[dict(r) for r in c.execute('SELECT id,sheet,started,submitted,scores,reviewed,feedback FROM attempts WHERE user_id=? AND submitted IS NOT NULL ORDER BY submitted,id',(uid,))]
 for r in attempts:
  r['scores']=json.loads(r['scores']);r['total']=sum(p['points'] for p in r['scores']);r['grade']=grade(r['total']) if r['reviewed'] else None
 done=[r for r in attempts if r['reviewed']];sheetmap={s['id']:s for s in content};topic_reports=[]
 for i,topic in enumerate(TOPICS):
  ls=[l for l in lessons if l['topic']==i];ids={l['id'] for l in ls};ev=[e for e in events if e['lesson'] in ids];ex=[r for r in done if sheetmap[r['sheet']]['topic']==topic]
  lessonrows=[]
  for l in ls:
   n=sum((l['id'],j) in mastered for j in range(len(l['checks'])))
   lessonrows.append({'id':l['id'],'title':l['title'],'mastered':n,'total':len(l['checks']),'completed':n==len(l['checks'])})
  passed=sum(l['mastered'] for l in lessonrows);total=sum(l['total'] for l in lessonrows)
  avg=round(sum(r['total'] for r in ex)/len(ex),1) if ex else None
  recommendation=('Începe cu explicațiile și exemplele acestei teme.' if not ev and not ex else 'Reia exemplele și verificările încă nerezolvate corect.' if passed<total else 'Ai rezolvat corect toate verificările. Încearcă o evaluare completă.')
  if avg is not None and avg<36:recommendation='Reia lecțiile de bază și exersează din nou; media evaluărilor corectate este sub 36/60.'
  topic_reports.append(dict(topic=i,title=topic,lessons=lessonrows,mastered=passed,total=total,completed_lessons=sum(l['completed'] for l in lessonrows),learning_attempts=len(ev),learning_correct=sum(e['correct'] for e in ev),evaluations=len(ex),average=avg,first=ex[0]['total'] if ex else None,latest=ex[-1]['total'] if ex else None,best=max((r['total'] for r in ex),default=None),change=ex[-1]['total']-ex[0]['total'] if len(ex)>1 else None,recommendation=recommendation))
 difficulty=[]
 for label,indices in [('Ușor',(0,1)),('Mediu',(2,3)),('Avansat',(4,5))]:
  got=maximum=0
  for r in done:
   for p in r['scores']:
    if int(p['key'].split('-')[0]) in indices:got+=p['points'];maximum+=p['max']
  difficulty.append(dict(label=label,points=got,max=maximum,percent=round(100*got/maximum) if maximum else None))
 return dict(student={k:student[k] for k in ['id','name','username','class_name']},topics=topic_reports,difficulty=difficulty,evaluations=attempts,submitted=len(attempts),reviewed=len(done),pending=len(attempts)-len(done),average=round(sum(r['total'] for r in done)/len(done),1) if done else None,mastered=len(mastered),total_checks=sum(len(l['checks']) for l in lessons),completed_lessons=sum(t['completed_lessons'] for t in topic_reports),learning_attempts=len(events),learning_accuracy=round(100*sum(e['correct'] for e in events)/len(events)) if events else None,last_active=max([e['created'] for e in events]+[r['submitted'] for r in attempts],default=None))
