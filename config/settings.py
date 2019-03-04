from pathlib import Path
import yaml

default_file = Path(__file__).parent / "config.yaml"

with open(default_file, "r") as file:
    config = yaml.safe_load(file)

telegram_bot = config.get("telegram_bot")
restaurant = config.get("restaurant")
database = config.get("database")
