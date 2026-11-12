import unittest,tempfile,threading,json,http.client,secrets
from pathlib import Path
import server
class Integration(unittest.TestCase):
 def setUp(self):
  cls=self
  cls.tmp=tempfile.TemporaryDirectory();server.DB=Path(cls.tmp.name)/'test.sqlite3';server.init()
  with server.conn() as c:
   salt=secrets.token_hex(16);c.execute('INSERT INTO users(username,name,class_name,salt,hash,role) VALUES(?,?,?,?,?,?)',('profesor','Profesor','',salt,server.pw('parola-test-123',salt),'teacher'))
   cls.code=c.execute("SELECT value FROM settings WHERE key='class_code'").fetchone()[0]
  cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.port=cls.http.server_port;threading.Thread(target=cls.http.serve_forever,daemon=True).start()
 def tearDown(self):self.http.shutdown();self.http.server_close();self.tmp.cleanup()
 def req(self,path,data=None,cookie=''):
  c=http.client.HTTPConnection('127.0.0.1',self.port);headers={'Cookie':cookie}
  if data is not None:headers['Content-Type']='application/json'
  c.request('POST' if data is not None else 'GET','/api/'+path,json.dumps(data) if data is not None else None,headers);r=c.getresponse();status=r.status;ck=r.getheader('Set-Cookie','').split(';')[0];out=json.loads(r.read());c.close();return status,out,ck
 def test_lifecycle_and_isolation(self):
  self.assertEqual(self.req('results')[0],401)
  def register(username):
   st,d,ck=self.req('register',dict(username=username,password='parola-test-123',name=username,class_name='IX A',code=self.code));self.assertEqual(st,200);return ck
  c1=register('elev1');c2=register('elev2');teacher=self.req('login',dict(username='profesor',password='parola-test-123'))[2]
  self.assertEqual(self.req('solutions',cookie=c1)[0],403)
  public=self.req('content',cookie=c1)[1];self.assertNotIn('answer',public[0]['exercises'][0]['parts'][0]);self.assertEqual(len(public),10)
  a=self.req('start',{'sheet':'t1v1'},c1)[1];aid=a['id']
  self.assertEqual(self.req('draft',dict(id=aid,answers={}),c2)[0],404)
  answers={'0-0':'−7/4 < −1,5 < 0 < 2/3','1-0':'5','1-1':'3','2-0':'5/4','2-1':'-1/2','work2':'1/2 + 3/4 = 5/4'}
  self.assertEqual(self.req('draft',dict(id=aid,answers=answers),c1)[0],200)
  self.assertEqual(json.loads(self.req('start',{'sheet':'t1v1'},c1)[1]['answers']),answers)
  self.assertEqual(self.req('submit',dict(id=aid,answers=answers),c1)[0],200)
  self.assertEqual(self.req('submit',dict(id=aid,answers=answers),c1)[0],409)
  self.assertEqual(self.req('results',cookie=c2)[1],[])
  r=self.req('results',cookie=teacher)[1][0];self.assertEqual(r['total'],14);self.assertEqual(r['reviewed'],0)
  points={x['key']:x['max'] for x in r['scores']}
  self.assertEqual(self.req('review',dict(id=aid,points=points),c1)[0],403)
  wrong=points|{'0-0':99};self.assertEqual(self.req('review',dict(id=aid,points=wrong),teacher)[0],400)
  self.assertEqual(self.req('review',dict(id=aid,points=points,feedback='Corect.'),teacher)[0],200)
  r=self.req('results',cookie=c1)[1][0];self.assertEqual((r['total'],r['grade'],r['reviewed']),(60,10,1));self.assertEqual(r['feedback'],'Corect.')
  with server.conn() as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM attempts').fetchone()[0],1)
 def test_content_and_grades(self):
  self.assertEqual(len(server.CONTENT),10)
  for s in server.CONTENT:
   self.assertEqual([sum(p['points'] for p in e['parts']) for e in s['exercises']],[4,6,8,10,14,18])
   self.assertEqual(len(s['exercises']),6)
  self.assertEqual([server.grade(x) for x in [0,5,6,53,54,60]],[1,1,2,9,10,10])
  self.assertTrue(server.auto('−2/3','-2/3'));self.assertTrue(server.auto('0,75','3/4'));self.assertFalse(server.auto('nan','3/4'));self.assertFalse(server.auto('1/0','0'))
 def test_learning_and_individual_reports(self):
  st,lessons,_=self.req('lessons');self.assertEqual(st,200);self.assertEqual(len(lessons),15)
  self.assertNotIn('answer',lessons[0]['checks'][0]);self.assertNotIn('explain',lessons[0]['checks'][0])
  guest=self.req('practice',dict(lesson='reale-ordine',item=0,answer='-1.6',request_id='guest-request-000001'))
  self.assertTrue(guest[1]['correct']);self.assertFalse(guest[1]['saved'])
  def register(name):return self.req('register',dict(username=name,password='parola-test-123',name=name,class_name='IX B',code=self.code))[2]
  one=register('ana');two=register('ion');prof=self.req('login',dict(username='profesor',password='parola-test-123'))[2]
  values=['-1.6','-7/4','5']
  for i,value in enumerate(values):
   data=dict(lesson='reale-ordine',item=i,answer=value,request_id='unique-request-00000'+str(i))
   self.assertTrue(self.req('practice',data,one)[1]['correct'])
   self.assertTrue(self.req('practice',data,one)[1]['saved'])
  self.req('practice',dict(lesson='reale-ordine',item=0,answer='100',request_id='unique-wrong-00001'),one)
  r=self.req('progress',cookie=one)[1];self.assertEqual(len(r),1);r=r[0]
  self.assertEqual((r['mastered'],r['completed_lessons'],r['learning_attempts'],r['learning_accuracy']),(3,1,4,75))
  self.assertEqual(r['average'],None);self.assertEqual(r['topics'][0]['mastered'],3)
  self.assertEqual(self.req('report?student='+str(r['student']['id']),cookie=two)[0],403)
  self.assertEqual(self.req('report?student='+str(r['student']['id']),cookie=prof)[0],200)
  self.assertEqual(self.req('progress',cookie=two)[1][0]['mastered'],0)
  allrows=self.req('progress',cookie=prof)[1];self.assertEqual(len(allrows),2)
  self.assertEqual(self.req('report?student=99999',cookie=prof)[0],404)
  self.assertEqual(self.req('report')[0],401)
  bad=dict(lesson='reale-ordine',item=999,answer='5',request_id='invalid-request-000001');self.assertEqual(self.req('practice',bad,one)[0],400)
  with server.conn() as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM lesson_events').fetchone()[0],4)
 def test_report_excludes_pending_and_compares_same_topic(self):
  student=self.req('register',dict(username='maria',password='parola-test-123',name='Maria',class_name='IX C',code=self.code))[2]
  teacher=self.req('login',dict(username='profesor',password='parola-test-123'))[2]
  for sheet,factor in [('t1v1',0),('t1v2',1),('t2v1',None)]:
   a=self.req('start',dict(sheet=sheet),student)[1]
   self.req('submit',dict(id=a['id'],answers={}),student)
   if factor is not None:
    row=next(r for r in self.req('results',cookie=teacher)[1] if r['id']==a['id']);points={x['key']:x['max']*factor for x in row['scores']}
    self.assertEqual(self.req('review',dict(id=a['id'],points=points,feedback='Feedback test'),teacher)[0],200)
  r=self.req('progress',cookie=student)[1][0]
  self.assertEqual((r['submitted'],r['reviewed'],r['pending'],r['average']),(3,2,1,30))
  self.assertEqual((r['topics'][0]['first'],r['topics'][0]['latest'],r['topics'][0]['change']),(0,60,60))
  self.assertEqual(r['topics'][1]['average'],None)
  self.assertEqual([d['percent'] for d in r['difficulty']],[50,50,50])
if __name__=='__main__':unittest.main()
