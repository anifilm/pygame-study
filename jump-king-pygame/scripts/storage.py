"""Small JSON save file helper."""

import json
from pathlib import Path

from settings import SAVE_FILE


class SaveData:
    """Stores best climb height and clear time between runs."""

    def __init__(self, filename: str = SAVE_FILE):
        self.path = Path(__file__).resolve().parent.parent / filename
        self.best_height = 0
        self.best_time = None
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        self.best_height = int(data.get("best_height", 0))
        self.best_time = data.get("best_time")

    def save(self) -> None:
        data = {
            "best_height": self.best_height,
            "best_time": self.best_time,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def update_height(self, height: int) -> None:
        if height > self.best_height:
            self.best_height = height
            self.save()

    def update_clear_time(self, seconds: float) -> None:
        if self.best_time is None or seconds < self.best_time:
            self.best_time = round(seconds, 2)
            self.save()
