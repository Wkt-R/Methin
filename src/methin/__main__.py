import logging

from methin.bot import MethinBot
from methin.config import get_settings


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    if not settings.discord_token:
        raise SystemExit("Brak DISCORD_TOKEN w .env")
    MethinBot(settings).run(settings.discord_token, log_handler=None)


if __name__ == "__main__":
    main()
