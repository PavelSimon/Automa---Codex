Zadanie pre vývoj webovej aplikácie na manažment Python aplikácií a agentov pre automatizáciu rutinných úloh podľa zadaného textu:

Webová aplikácia bude slúžiť na riadenie, monitoring, plánovanie a audit nových Python skriptov a agentov, spravovaných v modernom, bezpečnom a rozšíriteľnom prostredí. Prvým krokom je upresnenie požiadaviek, následne návrh architektúry, výber technológií, implementácia a nasadenie riešenia s dôrazom na bezpečnosť (autentifikácia, sandboxovanie, audit) a rozšíriteľnosť pomocou modulov, pluginov či MCP rozhrania.

### Hlavné požiadavky

- Automatizácia všetkých typov rutinných úloh: spracovanie dát, emailing, scraping, plánovanie, monitoring .
- Manažment výhradne nových Python skriptov a agentov .
- Rozšíriteľný backend aj MCP rozhranie cez moduly/pluginy .
- Úplná správa agentov: spúšťanie/stop, monitoring, logovanie, plánovanie .
- Webová aplikácia s lokálnym a LAN prístupom, multi-user autentifikáciou (email/heslo) .
- Implementácia API rozhrania na integráciu a vzdialené riadenie agentov.
- Bezpečnosť: štandardná autentifikácia, sandboxovanie skriptov, audit všetkých akcií (poradenstvo v zadanej oblasti) .
- Moderný webový framework na backend podľa odporúčaných best practice.

### Navrhovaný postup vývoja

#### 1. Upresnenie požiadaviek
- Zistenie konkrétnych typov úloh a agentov.
- Detailné požiadavky na plánovanie, monitoring, logging a audit.

#### 2. Výber technológií
- **Backend:** FastAPI (asynchrónny framework, škálovateľný, API-first, vhodný pre MCP rozhranie) .
- **Databáza:** SQLite (jednoduché lokálne nasadenie) .
- **Task scheduling:** Celery alebo APScheduler (spúšťanie/plánovanie úloh) .
- **Sandboxovanie:** lightweight VM/chroot jail, WASM sandboxing (NEODPORÚČA SA čistý python sandbox kvôli bezpečnosti) .
- **Audit:** Štruktúrované logovanie do súborov alebo databázy (napr. python-audit-log, logging modul) .
- **Frontend:** Jednoduchý HTML/CSS/JS dashboard.

#### 3. Návrh architektúry
- **Modely:** agent, skript, úloha, používateľ .
- **API:** detailné REST endpointy na správu agentov, úloh, monitoring, logovanie, auditovanie .
- **Task scheduling modul:** Celery/APS, pre plánované aj ad-hoc úlohy .

#### 4. Implementácia prototypu
- Základný backend + web frontend .
- Správa agentov a skriptov: spúšťanie, stop, plánovanie, logovanie výstupov, monitoring.
- Základná autentifikácia email/heslo, práva podľa rolí (admin, user) .
- Logovanie a audit všetkých akcií .
- Sandboxovanie cez Docker alebo VM/chroot jail.

#### 5. Rozšírenie a zabezpečenie
- Pridanie auditovania a logovania .
- Pokročilé sandboxovanie podľa best practice.
- Monitorovací dashboard, rozšírené filtrovacie možnosti .

#### 6. Nasadenie a údržba
- Lokálne alebo LAN deployment.
- Dokumentácia, pravidelná údržba, rozširovanie podľa potrieb.

### Bezpečnostné odporúčania

- Email/heslo autentifikácia, možnosť rozšírenia na 2FA .
- Práva podľa rolí admin/používateľ.
- Sandboxované prostredie pre všetky skripty – žiadny čistý Python sandbox kvôli historickým bezpečnostným incidentom .
- Všetky akcie auditované – logovanie do DB/súboru, štruktúrovaný log (JSON/SQL).
- API a UI pravidelne auditované, dôraz na prevenciu útokov a bezpečnú integráciu .

### Inšpirácie a ďalšie zdroje

- FastAPI je odporúčaný pre rýchly, bezpečný, rozšíriteľný REST/MCP backend .
- Sandboxovanie: best practice je Podman/VM/WASM, nikdy čistý python sandbox .
- Auditovanie: python-audit-log, logging, event logging do DB podľa typu akcie, používateľa, statusu .

Ak bude požiadavka na konkrétne ukážky auditovania, sandboxovania alebo plánovania v prostredí FastAPI/sandbox, je možné ich dodať podľa potrieb projektu.
