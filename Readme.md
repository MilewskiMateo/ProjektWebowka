# Opis
Jest to projekt będący systemem do obsługi paczek i paczkomatów. 
Projekt był robiony w ramach zajęć na studiach i jest on tylko symulacją jak mógłby taki serwis się prezentować.
System udostępnia trzy różne aplikacje przeznaczone osobno dla strony głównej, aplikacji wyświetlanej na ekranie paczkomatu i aplikacji na tablecie kurieria.
Znajdują się one pod innymi portami.

Aplikacja głównej strony znajduje się na porcie 8080
Aplikacja paczkomatu znajduje się na porcie 8082
Aplikacja kuriera znajduje się na porcie 8083

# Uruchomienie
Aby uruchomić aplikację należy stać w folderze "projekt" i wykonać instrukcję:

`docker-compose up`

Po uruchomieniu dockera należy udać się na adres:

`https://localhost:8080/init-db`

Jest to endpoint wypełniający bazę danych przykładowymi paczkomatami i kurierami. 

# Poruszanie się po serwisie
Mając już uruchomienie załatwione można swobodnie testować działanie serwisów pod adresami:
```
https://localhost:8080/
https://localhost:8082/
https://localhost:8083/
```
### W celu zasymulowania instnienia paczkomatów w programie na stałe zostały dodane paczkomaty o id:

Id paczkomatu:  paczkomat1

Id paczkomatu:  paczkomat2

Id paczkomatu:  paczkomat3


### Na tej samej zasadzie zostały na sztywno stworzone konta kurierów z których można korzystać:

Login: Admin1 Hasło: slomianykapelusz25!

Login: Admin2 Hasło: NieodpowiedzialneHaslo123

Login: Admin3 Hasło: MojPiesJestSuper

# Progresywność
Aplikacja kuriera (na tablety) posiada swoją dodatkową możliwość działania w trybie aplikacji progresywnej.

Niestety nie posiada ona jeszcze certyfikatu ale w celu zobaczenia samego efektu można skorzystać z polecenia:

`google-chrome --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:8083 --allow-insecure-localhost https://localhost:8083`

lub 

`start chrome --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:8083 --allow-insecure-localhost https://localhost:8083`

w celu wyświtlenia poprawnie progresywnej aplikacji ignorująć brak certyfikatu strony.
