# Opis
Jest to projekt będący systemem do obsługi paczek i paczkomatów. 
Projekt był robiony w ramach zajęć na studiach i jest on tylko symulacją jak mógłby taki serwis się prezentować.
System udostępnia trzy różne aplikacje przeznaczone osobno dla strony głównej, aplikacja wyświetlana na ekranie paczkomatu i aplikacja na tablecie kurieria.
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

Możliwie do wykorzystania paczkomaty mają odpowiednie Id:
Id paczkomatu:  paczkomat1
Id paczkomatu:  paczkomat2
Id paczkomatu:  paczkomat3


Możliwie konta kurierów do wykorzystania mają odpowiednie loginy i hasła:

Login: Admin1
Hasło: slomianykapelusz25!
Login: Admin2
Hasło: NieodpowiedzialneHaslo123
Login: Admin3
Hasło: MojPiesJestSuper


Do uruchomienia aplikacji kuriera proponuję użyć polecenia:

`google-chrome --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:8083 --allow-insecure-localhost https://localhost:8083`

lub 

`start chrome --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:8083 --allow-insecure-localhost https://localhost:8083`

w celu wyświtlenia poprawnie progresywnej aplikacji.

Na sam koniec proszę zwrócić uwagę, że podczas kopiowania id paczki z głównej 
aplikacji dla użytkownika, nie kopiować spacji stojącej na samym końcu 
