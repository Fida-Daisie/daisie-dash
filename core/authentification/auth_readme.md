Mit Daisie kann auch die simple Authetifizierungsfunktionalität von Dash verwendet werden. 
**DashBasicAuth** legt über die App einen Dialog in dem ein gültiger Nutzername und das dazugehörige Passwort eingegeben werden müssen, ansonsten sind die App und ihre Unterseiten nicht erreichbar. 

Es ist wichtig zu erwähnen, dass die Funktionen dieser Authentifikation sehr eingeschränkt sind:

- Benutzer können sich nicht ausloggen. Sie sind eingeloggt bis die Sitzung endet.
- Sie sind für ein sicheres Verwahren und Versenden der Nutzernamen bzw. Passwörter verantwortlich.
- Nutzer können sich nicht selbst registrieren oder ihr Passwort ändern.
- Es gibt keine verschiedenen Kategorien von Nutzern.

Für die Verwendung der *Dash-Authentifizierung* muss lediglich nach der Initialisierung von Daisie-Main ebenso eine `Server`-Instanz erstellt werden. 
Dazu muss ein Dictionary mit Nutzernamen und den jeweiligen Passwörtern hinterlegt sein. Dieses kann entweder aus einer `.txt`-Datei oder über eine Datenbankverbindung gelesen werden. Entweder übergibt man dem Konstruktor 
    - `file_path`: den Pfad der `.txt`-Datei oder 
    - `database_kwargs`: ein Dictionary mit den Zugangsdaten für die Datenbankverbindung.

Das sieht folgendermaßen aus:
```
# authentification setup
authClient = None
from .core.authentification import DashBasicAuth
db = {
    'database': 'fidadwh',
    'host':'dev-02.fida.local',
    'uid': 'fidadwhadmin',
    'pwd': 'tbd' 
}

daisie_main.authentification = DashBasicAuth.Server(database_kwargs=db)
```
Beziehungsweise:
```
daisie_main.authentification = DashBasicAuth.Server(file_path="daisie-framework/users.txt")
```