# Planer produktywności w stylu Notion

Aplikacja webowa Django implementująca wzorzec **MVC** (Model-Widok-Kontroler). Umożliwia użytkownikom organizowaie zadań w przestrzeniach roboczych z pełną obsługą CRUD uwierzytelnianiem wyszukiwaniem filtrowaniem, walidacją oraz wsparciem dla dockera.

## Spis treści
1. [Funkcje](#features)
2. [Architektura](#architecture)
3. [Wymagania](#requirements)
4. [Konfiguracja i uruchomienie lokalne](#setup--run-local)
5. [Konfigurecja i uruchomienie dockera](#setup--run-docker)
6. [Uruchomienie testów](#running-tests)
7. [Struktura projektu](#project-structure)

## Funkcje
- **Uwierzytelnianie użytkownika** rejestracja logowanie wylogowanie oparte na sesji wbudowany system Django
- **Przestrzenie robocze** (Model 1) nazwa opis właściciel interfejs CRUD
- **Zadania** (Model 2) tytuł treść termin status do zrobienia w trakcie zakończone interfejs CRUD
- **Relacja jeden do wielu** każda przestrzeń robocza ma wiele zadań (Workspace 1
N Task)
- **Izolacja danych użytkownika** użytkownicy widzą i edytują tylko swoje przestrzenie robocze i zadania
- **Wyszukiwanie i filtrowanie wyszukiwanie** po tytule i treści filtrowanie po statusie i przestrzeni roboczej
- **﻿﻿Walidacja po stronie serwera formularze Django minimalna długość brak przeszłych terminów oraz po stronie klienta HTML5 (`required`, `type="date"`, `maxlength`)
- **Responsywny interfejs** użytkownika styl Bootstrap 5 tabela listy i karty szczegółów
- **Paginacja** na liście zadań
- **Docker** zawiera Dockerfile oraz docker compose yml
- **Testy jednostkowe** modele walidacja formularzy oraz widoki

## Architektura
Django implementuje wzorzec **MVC** jako **MTV**:
- **Model** — `tasks/models.py`, `workspaces/models.py` (data layer, ORM)
- **Widok (Controller)** — `tasks/views.py`, `workspaces/views.py` (obsługa zadań HTTP, logika biznesowa, widoki oparte na klasach)
- **Szablon (View)** — `templates/`, `*/templates/` (renderowanie interfejsu użytkownika)
- **URL** — `planner/urls.py` oraz per-app `urls.py` (routing)

## Wymagania
- Python 3.10+
- pip
- (opcjonalnie) Docker + Docker Compose

## Konfiguracja i uruchomienie lokalnie

```bash
# 1. Clone
git clone <your-repo-url>
cd planner

# 2. Tworzenie śródowiska wirtualnego
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Instalowanie zależności
pip install -r requirements.txt

# 4. Migracja (tworzenie bazy danych SQLite)
python manage.py makemigrations
python manage.py migrate

# 5. (Opcjonalnie) tworzenie konta administratora
python manage.py createsuperuser

# 6. Uruchomienie serwera 
python manage.py runserver
```

Otwórz http://127.0.0.1:8080/ — przekierowanie do strony logowania. Rejestracja nowego konta, utworzenie workspace, dodawanie zadań

## Konfiguracja i uruchomienie dockera

```bash
docker compose up --build
```

Aplikacja będzie dostępna pod adresem http://localhost:8080/ 
Migracje są wykonywane automatychnie przy starcie kontenera

## Uruchamianie testów

```bash
python manage.py test
```

## Struktura projektu
```
planner/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── planner/              # project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/            # global templates (base, auth)
│   ├── base.html
│   └── registration/
├── workspaces/           # Workspace app (Model 1)
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/workspaces/
└── tasks/                # Task app (Model 2)
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    └── templates/tasks/
```

## Realizowane kryterie na wyższą ocenę
- **Zaawansowane modele danych**: 2 modele (`Workspace`, `Task`) z relacją One-to-Many (jeden do wielu), oba powiazane z `auth.User`.
- **UI/UX**: respontywna tabela w stulu Bootstrap, karty, statusy oraz widok szczegółowy
- **Docker**: `Dockerfile` + `docker-compose.yml`.
- **Testy jednostkowe**: `tasks/tests.py` obejmuje modele, walidację formularzy oraz autoryzacja/wyszukiwanie w widokach
- **Walidacja**: po stronie serwera i po stronie klijenta
- **Filtrowanie i wyszukiwanie**: wedlug słów kluczowych, statusu i obrzaru roboczego
- **Uwierzytelnianie**: logowanie, rejestracja, wylogowywanie w oparciu o sesję
