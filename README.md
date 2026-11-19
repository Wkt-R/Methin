# Methin

Tekstowe MMORPG na Discordzie: jeden wspólny świat dla wielu serwerów.

## Wymagania (Windows)

Wszystkie polecenia uruchamiaj w **PowerShellu**. Instalację przez Chocolatey wykonaj w PowerShellu **uruchomionym jako administrator**.

1. **Chocolatey** (menedżer pakietów)
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   choco --version
   ```
2. **Git, Python 3.12 i make:**
   ```powershell
   choco install git python312 make -y # pomiń git i python312 jak już masz
   ```
   Po instalacji **zamknij i otwórz ponownie terminal**, żeby odświeżyć PATH. Sprawdź:
   ```powershell
   git --version
   python --version    # powinno pokazać 3.12.x
   make --version
   ```
   Jeśli `python` nie działa, spróbuj `py -3.12 --version`. Wtedy zamień `python` na `py` w `Makefile` (cel `setup` i `bot`).
3. **Docker Desktop** (z backendem WSL 2): https://www.docker.com/products/docker-desktop/
   Po instalacji uruchom Docker Desktop i poczekaj, aż będzie "running". Sprawdź: `docker compose version`.
4. **Własny bot testowy Discorda:** utwórz aplikację w https://discord.com/developers/applications, w zakładce Bot wygeneruj token i dodaj bota na swój serwer testowy (OAuth2 → URL Generator, zakresy `bot` i `applications.commands`). Każdy deweloper ma własnego bota i własny token.

## Szybki start

```powershell
git clone <adres-repozytorium> methin
cd methin
make setup     # tworzy .env i buduje obrazy
```

Otwórz `.env` i wpisz `DISCORD_TOKEN` (oraz opcjonalnie `DEV_GUILD_ID`, czyli ID Twojego serwera testowego). Potem:

```powershell
make up        # baza + bot w tle
make logs      # logi bota (Ctrl+C wychodzi z podglądu)
```

Jeśli na Discordzie widzisz komendę `/ping`, wszystko działa.

### Alternatywa bez `make`

Każdy cel z `Makefile` to zwykła komenda `docker compose`, np.:

```powershell
copy .env.example .env
docker compose up -d --build
docker compose logs -f bot
```

## Edytor (VS Code)

Biblioteki aplikacji są zainstalowane w kontenerze, więc VS Code ich nie widzi. Żeby edytor podpowiadał kod i nie podkreślał importów, utwórz lokalny venv:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Potem `Ctrl+Shift+P` → **Python: Select Interpreter** → wybierz `.venv`.
Jeśli PowerShell blokuje aktywację skryptu, użyj raz: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Tryby pracy

| Tryb | Komenda | Kiedy |
|---|---|---|
| Wszystko w Dockerze | `make up` | najprostsze, identyczne u wszystkich |
| Baza w Dockerze, bot w venv | `make bot` | debugowanie z breakpointami (w `.env` `DATABASE_URL` wskazuje na `localhost`) |
| Testy | `make test` | wymagają prawdziwego Postgresa (baza `methin_test`) |
| Lint / format | `make lint` / `make fmt` | przed commitem |
| Konsola SQL | `make psql` | podgląd danych |
| Podgląd bazy w przeglądarce | `docker compose --profile tools up -d` → http://localhost:8080 | Adminer (system: PostgreSQL, serwer: `db`) |
| Reset bazy | `make reset-db` | **kasuje** dane deweloperskie |

## Rozwiązywanie problemów

- **`make` nie jest rozpoznawane:** zainstaluj przez Chocolatey (krok 1 - choco i 2 - make) i otwórz nowy terminal.
- **`error getting credentials ... docker-credential-desktop` przy budowaniu:** sprawdź `where docker-credential-desktop`. Jeśli brak, dodaj `C:\Program Files\Docker\Docker\resources\bin` do PATH i zrestartuj terminal. Ostateczność: usuń wpis `"credsStore"` z `C:\Users\<ty>\.docker\config.json` (zrób kopię).
- **Bot restartuje się w kółko:** zwykle pusty `DISCORD_TOKEN` w `.env`. Sprawdź `make logs`, po poprawce `docker compose restart bot`.
- **Port 5432 zajęty:** zmień `POSTGRES_PORT` w `.env` (np. na 5433) i zaktualizuj port w `DATABASE_URL`.
- **Brak bazy `methin_test`:** skrypt tworzący ją działa tylko na pustym wolumenie. Użyj `make reset-db`.

## Zasady

- Wersja Pythona (3.12) i Postgresa (16) jest przypięta w `Dockerfile` / `docker-compose.yml`. Zmiana wersji = osobny PR.
- Schemat bazy tylko przez migracje Alembic, nigdy ręcznie.
- Pliku `.env` nigdy nie commitujemy.
