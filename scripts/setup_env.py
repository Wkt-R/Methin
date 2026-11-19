import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
env, example = root / ".env", root / ".env.example"

if env.exists():
    print(".env już istnieje, pomijam")
else:
    shutil.copy(example, env)
    print("Utworzono .env, uzupełnij w nim DISCORD_TOKEN")
