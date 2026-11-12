"""Pornire interactivă pentru calculatorul profesorului."""
import server,subprocess,sys,webbrowser
server.init()
with server.conn() as c:ready=bool(c.execute("SELECT 1 FROM users WHERE role='teacher'").fetchone())
if not ready:
 result=subprocess.run([sys.executable,str(server.ROOT/'server.py'),'--init-teacher'])
 if result.returncode:raise SystemExit(result.returncode)
webbrowser.open('http://localhost:8000')
subprocess.run([sys.executable,str(server.ROOT/'server.py')],check=True)
