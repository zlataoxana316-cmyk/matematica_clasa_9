# Matematica clasa a IX-a

## Versiunea publică

Folderul `docs/` conține versiunea publică fără server: 15 lecții, 45 de verificări și 10 variante de autoevaluare. Funcționează pe GitHub Pages. Progresul se salvează numai în browserul elevului; conturile și catalogul centralizat sunt omise. Punctajul etapelor scrise și al graficelor se acordă prin autoevaluare după barem, nu de profesor. Workflow-ul `pages.yml` publică această versiune.

Restul proiectului păstrează separat versiunea completă cu server, descrisă mai jos.

Platformă în limba română pentru pregătirea la matematică, cu trei spații separate: **Învață**, **Evaluări**, **Catalog și rapoarte**. Material original pentru antrenament; nu se afirmă conformitatea cu un curriculum oficial verificat.

## Învață

- Cinci teme: operații cu numere reale, radicali, puteri, funcția de gradul I, funcția de gradul al II-lea.
- 15 lecții, cu idei esențiale, exemple dezvăluite pas cu pas, indicii și greșeli frecvente.
- 45 de verificări formative cu feedback imediat și explicații.
- Laboratoare cu glisoare pentru dreaptă și parabolă. Cazul a=0 este identificat explicit drept funcție constantă, în afara gradului cerut.
- Lecțiile pot fi explorate fără cont. Progresul este salvat pe server doar pentru elevii autentificați.

O lecție este finalizată după ce elevul a rezolvat corect toate cele trei verificări distincte, chiar dacă a avut nevoie de reluări. Se păstrează și numărul total de încercări. Verificările formative nu primesc note.

## Evaluări

- 10 variante, câte două pentru fiecare temă, cu 6 exerciții și 60 de puncte per variantă.
- 60 de minute pentru lucru, câmpuri pentru calcule și explicații, caroiaj desenabil cu mouse-ul sau degetul.
- Autosalvare pe server și posibilitatea de a relua o fișă netrimisă.
- Răspunsurile numerice sunt verificate automat la trimitere. Se acceptă fracții ca `-2/3` și zecimale ca `0,75`.
- Justificările și graficele sunt corectate de profesor. Profesorul poate modifica fiecare subpunct pentru punctaj parțial și metode alternative corecte.
- Punctajul automat este **provizoriu**. Media și nota finală se bazează pe evaluările corectate.

## Catalog și rapoarte

Accesul profesorului este separat de cel al elevilor. Elevii își văd numai propriile date.

- Lista elevilor, inclusiv cei fără activitate; căutare, filtru pe clasă și pe stare.
- Lecții finalizate, verificări distincte rezolvate corect și număr de încercări formative.
- Evaluări corectate, evaluări în așteptare, medii și ultima activitate.
- Raport individual cu progres pe fiecare temă, prima și ultima evaluare corectată, diferența de punctaj, cel mai bun rezultat și istoric.
- Grafic al evaluărilor, rezultate pe nivel de dificultate și recomandări de recapitulare.
- Export CSV general, exportul încercărilor, raport CSV individual și imprimarea raportului / salvarea ca PDF din browser.

Diferența de punctaj compară numai evaluări din **aceeași temă**, în ordinea trimiterii, și numai după corectare. Pentru zero sau o singură evaluare nu se inventează o tendință. Rapoartele se referă la întreaga perioadă înregistrată.

## Pornire pe calculator

Este necesar **Python 3.11 sau mai nou**. Pentru rulare nu sunt necesare biblioteci suplimentare.

1. Descărcați depozitul prin **Code → Download ZIP** și dezarhivați-l.
2. Pe Windows deschideți `Start_Windows.bat`, sau rulați `python start.py` din folderul proiectului.
3. La prima pornire creați contul profesorului: utilizator, nume, parolă proprie de minimum 10 caractere. Parola nu se afișează în timpul tastării.
4. Deschideți `http://localhost:8000`. În **Catalog și rapoarte**, secțiunea **Înscrierea elevilor în platformă** arată codul de înscriere.
5. Elevii aleg **Intră în cont → Sunt elev și vreau un cont** și folosesc codul, numele și clasa lor.

Păstrați fereastra serverului deschisă. Alte dispozitive din aceeași rețea folosesc adresa IP a calculatorului profesorului și portul 8000. `localhost` pe telefon indică telefonul, nu calculatorul profesorului. Accesul depinde de firewall și de rețeaua școlii.

## GitHub și accesul printr-un link comun

Depozitul conține codul complet și fișele imprimabile. **Codul de pe GitHub nu reprezintă încă o instanță online a platformei.** GitHub Pages nu rulează serverul Python și SQLite. Pentru acces din afara rețelei școlii este necesară găzduirea aplicației pe un server Python / Docker, cu HTTPS și disc persistent.

Catalogul, parolele și rezultatele elevilor sunt salvate pe serverul aplicației, **nu în depozitul public GitHub**. Nu încărcați datele elevilor sau copiile bazei de date în depozit.

## Rulare cu Docker

```sh
docker compose build
docker compose run --rm matematica python server.py --init-teacher
docker compose up -d
```

Aplicația ascultă pe `127.0.0.1:8000`; se configurează un proxy HTTPS pentru adresa publică. După activarea HTTPS setați `COOKIE_SECURE=1` în mediul de rulare și reporniți aplicația. Volumul `matematica_data` păstrează datele la repornire. Fără Docker, `DATA_DIR` trebuie să indice un folder persistent, iar `PORT` poate fi ales de găzduire. Folosiți un singur proces al aplicației.

## Date, acces și limite

- Baza de date este `data/school.sqlite3` în rularea obișnuită. Copiile de siguranță se fac cu mecanismul SQLite backup sau după oprirea aplicației.
- Parole PBKDF2 cu sare aleatorie, sesiuni de 12 ore, cookie-uri HttpOnly și SameSite, acces separat elev/profesor. Pentru HTTPS activați și Secure prin `COOKIE_SECURE=1`.
- Contul profesorului se creează local, prin CLI. Nu există o parolă comună inclusă în cod.
- Codul de înscriere se distribuie elevilor; nu se publică pe GitHub. Un profesor poate urmări mai multe clase.
- Nu sunt implementate recuperarea automată a parolelor, administrarea mai multor profesori și sincronizarea offline.
- În cazul unei întreruperi de rețea, păstrați pagina deschisă până la confirmarea salvării. La expirare, pagina încearcă trimiterea; dacă este închisă sau fără rețea, trimiterea are loc după revenire. Durata și trimiterile întârziate sunt vizibile profesorului. Cronometrul este pentru antrenament, nu pentru examen supravegheat.
- Sursa și baremul sunt publice în acest proiect. Platforma este pentru pregătire, nu o bancă secretă de examen sau un sistem de verificare a identității.
- Exporturile CSV tratează câmpurile care pot fi interpretate ca formule. Conținutul introdus de elev este escapat în interfață.

## Fișe imprimabile

`downloads/Fise_Matematica_IX.docx` și `downloads/Fise_Matematica_IX.pdf` conțin 35 de pagini: **1–20 pentru elevi**, **21–35 pentru profesor**, cu rezolvări, grafice și barem. Formulele sunt text Unicode editabil în Word; graficele și caroiajele sunt imagini.

Grilă orientativă propusă, fără puncte din oficiu: 0–5 → 1; 6–11 → 2; 12–17 → 3; 18–23 → 4; 24–29 → 5; 30–35 → 6; 36–41 → 7; 42–47 → 8; 48–53 → 9; 54–60 → 10. Nu este prezentată drept grilă oficială a Republicii Moldova.

## Verificare

```sh
python -m unittest -v test_server.py
node --check public/app.js
node --check public/learn.js
node --check public/reports.js
```

Testele HTTP verifică izolarea conturilor, înscrierea, punctajele, salvarea și trimiterea fișelor, corectarea, progresul formativ, evitarea numărării duble a aceleiași cereri și rapoartele. Testele rapoartelor verifică faptul că punctajele provizorii sunt excluse din medii și că diferențele compară aceeași temă. Lecțiile publice, feedbackul rapid, pagina evaluărilor și glisoarele graficelor au fost verificate în browser. Fluxurile autentificate au fost verificate prin teste HTTP; toate ecranele lor nu au fost inspectate vizual.

Fișierul `.github/workflows/check.yml` rulează testele automat după push și permite descărcarea fișelor ca artefact.

## Editarea materialelor

`lessons.json`: lecțiile. `content.json`: evaluările. `make_lessons.py` și `make_content.py` regenerează datele. `build_document.py` regenerează fișele și graficele, cu `python-docx`, `matplotlib` și `numpy` instalate doar pentru autorare. Nu schimbați ID-urile sau structura exercițiilor peste încercări existente fără migrarea istoricului.
