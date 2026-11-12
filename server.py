"""Matematica IX — Python 3.11+, fără dependențe externe."""
import os,json,sqlite3,secrets,hashlib,hmac,time,math,csv,io,re,argparse,getpass
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlsplit,parse_qs
from progress import report
from fractions import Fraction
ROOT=Path(__file__).parent
DB=Path(os.environ.get('DATA_DIR',ROOT/'data'))/'school.sqlite3'
LIMITS={}
CONTENT=json.loads((ROOT/'content.json').read_text())
LESSONS=json.loads((ROOT/'lessons.json').read_text())
def conn():
 c=sqlite3.connect(DB,timeout=15);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');return c
def init():
 DB.parent.mkdir(parents=True,exist_ok=True)
 with conn() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, name TEXT, class_name TEXT, salt TEXT, hash TEXT, role TEXT);
CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id INTEGER REFERENCES users(id),expires REAL);
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,user_id INTEGER REFERENCES users(id),sheet TEXT,started REAL,submitted REAL,answers TEXT,scores TEXT,feedback TEXT DEFAULT '',reviewed INTEGER DEFAULT 0);
CREATE INDEX IF NOT EXISTS attempts_user ON attempts(user_id);
CREATE TABLE IF NOT EXISTS lesson_events(id INTEGER PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, user_id INTEGER NOT NULL REFERENCES users(id),lesson TEXT NOT NULL,item INTEGER NOT NULL,answer TEXT NOT NULL,correct INTEGER NOT NULL,created REAL NOT NULL);
CREATE INDEX IF NOT EXISTS lessons_user ON lesson_events(user_id);''')
  c.execute("INSERT OR IGNORE INTO settings VALUES('class_code',?)",(secrets.token_urlsafe(9),))
def pw(password,salt):return hashlib.pbkdf2_hmac('sha256',password.encode(),salt.encode(),200000).hex()
def safeuser(row):return {k:row[k] for k in ['id','username','name','class_name','role']}
def grade(score):
 for top,n in [(5,1),(11,2),(17,3),(23,4),(29,5),(35,6),(41,7),(47,8),(53,9),(60,10)]:
  if score<=top:return n
 return 10
def numeric(s):
 s=str(s).strip().replace(',','.').replace('−','-').replace(' ','')
 if len(s)>100:raise ValueError()
 return float(Fraction(s))
def auto(answer,expected):
 try:return math.isfinite(numeric(answer)) and abs(numeric(answer)-numeric(expected))<1e-7
 except (ValueError,ZeroDivisionError,OverflowError):return False
class Handler(BaseHTTPRequestHandler):
 server_version='MatematicaIX'
 def log_message(self,*args):pass
 def send(self,data,status=200,kind='application/json; charset=utf-8',cookie=None):
  body=json.dumps(data,ensure_ascii=False).encode() if kind.startswith('application/json') else data
  self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY');self.send_header('Referrer-Policy','same-origin');self.send_header('Cache-Control','no-store' if self.path.startswith('/api/') else 'no-cache')
  self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
  if cookie:self.send_header('Set-Cookie',cookie)
  self.end_headers();self.wfile.write(body)
 def user(self,c):
  cookies=SimpleCookie();cookies.load(self.headers.get('Cookie',''));t=cookies.get('session')
  return c.execute('SELECT u.* FROM users u JOIN sessions s ON s.user_id=u.id WHERE s.token=? AND s.expires>?',(t.value if t else '',time.time())).fetchone()
 def do_GET(self):self.route()
 def do_POST(self):
  # Same-origin JSON writes prevent cross-site form requests.
  if self.headers.get('Sec-Fetch-Site')=='cross-site' or self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send({'error':'Cerere nepermisă.'},403)
  self.route()
 def route(self):
  try:self.handle_route()
  except (ValueError,KeyError,TypeError,json.JSONDecodeError):self.send({'error':'Date invalide.'},400)
  except Exception as e:
   print(type(e).__name__,str(e),flush=True);self.send({'error':'Eroare internă. Reîncercați.'},500)
 def handle_route(self):
  path=urlsplit(self.path).path
  if not path.startswith('/api/'):
   if self.command!='GET':return self.send({},405)
   files={'/':'public/index.html','/app.js':'public/app.js','/style.css':'public/style.css','/learn.js':'public/learn.js','/reports.js':'public/reports.js','/fise.docx':'downloads/Fise_Matematica_IX.docx'}
   if path not in files:return self.send({'error':'Pagina nu există.'},404)
   if path=='/fise.docx':
    with conn() as c:
     u=self.user(c)
     if not u or u['role']!='teacher':return self.send({'error':'Descărcare disponibilă profesorului.'},403)
   p=ROOT/files[path]
   if not p.exists():return self.send({'error':'Fișier indisponibil.'},404)
   kind={'html':'text/html; charset=utf-8','js':'text/javascript; charset=utf-8','css':'text/css; charset=utf-8','docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}[p.suffix[1:]]
   return self.send(p.read_bytes(),kind=kind)
  data={}
  if self.command=='POST':
   n=int(self.headers.get('Content-Length',0))
   if n>1500000:return self.send({'error':'Cerere prea mare.'},413)
   data=json.loads(self.rfile.read(n))
  with conn() as c:
   u=self.user(c)
   if path=='/api/lessons' and self.command=='GET':
    public=json.loads(json.dumps(LESSONS))
    for l in public:
     for q in l['checks']:
      q.pop('answer');q.pop('explain')
    return self.send(public)
   if path=='/api/practice' and self.command=='POST':
    l=next((l for l in LESSONS if l['id']==data.get('lesson')),None);item=data.get('item');value=data.get('answer');rid=data.get('request_id')
    if not l or not isinstance(item,int) or not 0<=item<len(l['checks']) or not isinstance(value,str) or len(value)>100 or not isinstance(rid,str) or not re.fullmatch(r'[a-zA-Z0-9_-]{12,80}',rid):raise ValueError()
    q=l['checks'][item];correct=auto(value,q['answer'])
    if u and u['role']=='student':
     old=c.execute('SELECT * FROM lesson_events WHERE request_id=?',(rid,)).fetchone()
     if old:
      if old['user_id']!=u['id'] or old['lesson']!=l['id'] or old['item']!=item or old['answer']!=value:raise ValueError()
      correct=bool(old['correct'])
     else:c.execute('INSERT INTO lesson_events(request_id,user_id,lesson,item,answer,correct,created) VALUES(?,?,?,?,?,?,?)',(rid,u['id'],l['id'],item,value,int(correct),time.time()))
    return self.send({'correct':correct,'explain':q['explain'],'answer':q['answer'],'saved':bool(u and u['role']=='student')})
   if path in ['/api/login','/api/register']:
    if self.command!='POST':return self.send({},405)
    ip=self.client_address[0];now=time.time();hits=[t for t in LIMITS.get(ip,[]) if t>now-600]
    if len(hits)>=300:return self.send({'error':'Prea multe încercări. Reîncercați peste 10 minute.'},429)
    LIMITS[ip]=hits+[now]
    username=str(data.get('username','')).strip().lower();password=str(data.get('password',''))
    if not re.fullmatch(r'[a-z0-9_.-]{3,40}',username) or not 10<=len(password)<=200:return self.send({'error':'Utilizator: 3–40 litere latine/cifre. Parolă: 10–200 caractere.'},400)
    if path.endswith('register'):
     if not hmac.compare_digest(str(data.get('code','')),c.execute("SELECT value FROM settings WHERE key='class_code'").fetchone()[0]):return self.send({'error':'Codul clasei este incorect.'},403)
     name=str(data.get('name','')).strip();cl=str(data.get('class_name','')).strip()
     if not name or len(name)>100 or not cl or len(cl)>30:return self.send({'error':'Completați numele și clasa.'},400)
     salt=secrets.token_hex(16)
     try:c.execute('INSERT INTO users(username,name,class_name,salt,hash,role) VALUES(?,?,?,?,?,?)',(username,name,cl,salt,pw(password,salt),'student'))
     except sqlite3.IntegrityError:return self.send({'error':'Acest utilizator există deja.'},409)
    row=c.execute('SELECT * FROM users WHERE username=?',(username,)).fetchone()
    if not row or not hmac.compare_digest(row['hash'],pw(password,row['salt'])):return self.send({'error':'Utilizator sau parolă incorectă.'},401)
    t=secrets.token_urlsafe(32);c.execute('DELETE FROM sessions WHERE expires<?',(time.time(),));c.execute('INSERT INTO sessions VALUES(?,?,?)',(t,row['id'],time.time()+12*3600))
    cookie='session='+t+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=43200'+('; Secure' if os.environ.get('COOKIE_SECURE')=='1' else '')
    return self.send(safeuser(row),cookie=cookie)
   if not u:return self.send({'error':'Autentificare necesară.'},401)
   if path=='/api/progress' and self.command=='GET':
    rows=c.execute("SELECT id,name,username,class_name FROM users WHERE role='student'"+('' if u['role']=='teacher' else ' AND id=?')+' ORDER BY name',() if u['role']=='teacher' else (u['id'],)).fetchall()
    return self.send([report(c,row,CONTENT,LESSONS,grade) for row in rows])
   if path=='/api/report' and self.command=='GET':
    params=parse_qs(urlsplit(self.path).query);uid=int(params.get('student',[u['id']])[0])
    if u['role']!='teacher' and uid!=u['id']:return self.send({'error':'Acces interzis.'},403)
    student=c.execute("SELECT id,name,username,class_name FROM users WHERE id=? AND role='student'",(uid,)).fetchone()
    if not student:return self.send({'error':'Elev inexistent.'},404)
    return self.send(report(c,student,CONTENT,LESSONS,grade))
   if path=='/api/me':return self.send(safeuser(u))
   if path=='/api/logout' and self.command=='POST':
    c.execute('DELETE FROM sessions WHERE user_id=?',(u['id'],));return self.send({},cookie='session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
   if path=='/api/content':
    public=json.loads(json.dumps(CONTENT))
    for s in public:
     for e in s['exercises']:
      for p in e['parts']:p.pop('answer');p.pop('solution')
    return self.send(public)
   if path=='/api/start' and self.command=='POST':
    if u['role']!='student':return self.send({'error':'Folosiți un cont de elev pentru rezolvare.'},403)
    sid=data['sheet'];assertion=next((s for s in CONTENT if s['id']==sid),None)
    if not assertion:raise ValueError()
    old=c.execute('SELECT id,started,answers FROM attempts WHERE user_id=? AND sheet=? AND submitted IS NULL ORDER BY id DESC LIMIT 1',(u['id'],sid)).fetchone()
    if old:return self.send(dict(old))
    cur=c.execute('INSERT INTO attempts(user_id,sheet,started,answers,scores) VALUES(?,?,?,?,?)',(u['id'],sid,time.time(),'{}','[]'))
    return self.send({'id':cur.lastrowid,'started':time.time(),'answers':'{}'})
   if path in ['/api/draft','/api/submit'] and self.command=='POST':
    row=c.execute('SELECT * FROM attempts WHERE id=? AND user_id=?',(data['id'],u['id'])).fetchone()
    if not row:return self.send({'error':'Încercare inexistentă.'},404)
    if row['submitted']:return self.send({'error':'Încercarea a fost deja trimisă.'},409)
    s=next(s for s in CONTENT if s['id']==row['sheet']);answers=data['answers']
    if not isinstance(answers,dict) or len(answers)>80:raise ValueError()
    for key,val in answers.items():
     if not re.fullmatch(r'(?:[0-5]-[0-4]|work[0-5]|graph[0-5])',key):raise ValueError()
     if key.startswith('graph'):
      if not isinstance(val,list) or len(val)>101:raise ValueError()
      for line in val:
       if not isinstance(line,list) or len(line)>300:raise ValueError()
       for point in line:
        if not isinstance(point,list) or len(point)!=2 or not all(isinstance(n,(int,float)) and math.isfinite(n) and -100<=n<=620 for n in point):raise ValueError()
     elif not isinstance(val,str) or len(val)>20000:raise ValueError()
    if path.endswith('draft'):
     c.execute('UPDATE attempts SET answers=? WHERE id=?',(json.dumps(answers),row['id']));return self.send({'saved':True})
    scores=[]
    for i,e in enumerate(s['exercises']):
     for j,p in enumerate(e['parts']):
      key=f'{i}-{j}';val=str(answers.get(key,''))
      scores.append({'key':key,'points':0 if p['manual'] else (p['points'] if auto(val,p['answer']) else 0),'max':p['points'],'manual':p['manual']})
    # Every submission awaits teacher review: methods can earn partial credit, including numeric fields.
    c.execute('UPDATE attempts SET answers=?,scores=?,submitted=? WHERE id=?',(json.dumps(answers),json.dumps(scores),time.time(),row['id']))
    return self.send({'saved':True})
   if path=='/api/results':
    rows=c.execute('SELECT a.*,u.name,u.class_name,u.username FROM attempts a JOIN users u ON u.id=a.user_id WHERE a.submitted IS NOT NULL'+('' if u['role']=='teacher' else ' AND a.user_id=?')+' ORDER BY a.submitted DESC',() if u['role']=='teacher' else (u['id'],)).fetchall()
    out=[]
    for row in rows:
     d=dict(row);d['scores']=json.loads(d['scores']);d['answers']=json.loads(d['answers']);d['total']=sum(p['points'] for p in d['scores']);d['grade']=grade(d['total']);out.append(d)
    return self.send(out)
   if path=='/api/solutions':
    if u['role']!='teacher':return self.send({'error':'Acces profesor.'},403)
    return self.send(CONTENT)
   if path=='/api/students':
    if u['role']!='teacher':return self.send({},403)
    return self.send({'students':[dict(x) for x in c.execute("SELECT id,name,username,class_name FROM users WHERE role='student' ORDER BY name")], 'code':c.execute("SELECT value FROM settings WHERE key='class_code'").fetchone()[0]})
   if path=='/api/review' and self.command=='POST':
    if u['role']!='teacher':return self.send({},403)
    row=c.execute('SELECT * FROM attempts WHERE id=? AND submitted IS NOT NULL',(data['id'],)).fetchone()
    if not row:return self.send({},404)
    scores=json.loads(row['scores'])
    for score in scores:
     value=float(data['points'][score['key']])
     if not math.isfinite(value) or value<0 or value>score['max'] or value%1:raise ValueError()
     score['points']=int(value)
    feedback=str(data.get('feedback',''))[:5000]
    c.execute('UPDATE attempts SET scores=?,feedback=?,reviewed=1 WHERE id=?',(json.dumps(scores),feedback,row['id']))
    return self.send({'saved':True})
   return self.send({'error':'Rută inexistentă.'},404)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--init-teacher',action='store_true');parser.add_argument('--port',type=int,default=int(os.environ.get('PORT','8000')));parser.add_argument('--host',default='0.0.0.0');parser.add_argument('--strictPort',action='store_true');args=parser.parse_args();init()
 if args.init_teacher:
  username=input('Utilizator profesor: ').strip().lower();name=input('Nume profesor: ').strip();password=getpass.getpass('Parolă (minimum 10 caractere): ')
  if not re.fullmatch(r'[a-z0-9_.-]{3,40}',username) or len(password)<10:raise SystemExit('Date invalide.')
  salt=secrets.token_hex(16)
  with conn() as c:
   if c.execute("SELECT 1 FROM users WHERE role='teacher'").fetchone():raise SystemExit('Există deja un profesor.')
   c.execute('INSERT INTO users(username,name,class_name,salt,hash,role) VALUES(?,?,?,?,?,?)',(username,name,'',salt,pw(password,salt),'teacher'))
  print('Cont creat. Porniți: python server.py')
 else:
  print(f'Matematica IX: http://localhost:{args.port}',flush=True);ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
