import json
from abc import ABC
from dataclasses import dataclass, field, asdict
from datetime import datetime

@dataclass(kw_only=True)
class GameEvent(ABC):
    game_id: str
    score: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    row: int
    column: int


@dataclass(kw_only=True)
class GameStartedEvent(GameEvent):
    message: str = "Game started with specified height and width."
    height: int
    width: int

@dataclass(kw_only=True)
class ExitFoundEvent(GameEvent):
    message: str = "You found the exit at specified height and width!"


@dataclass(kw_only=True)
class PlayerMovedEvent(GameEvent):
    message: str = "You moved in the specified direction."
    direction: str

@dataclass(kw_only=True)
class MoveFailedEvent(GameEvent):
    direction: str
    message: str


@dataclass(kw_only=True)
class CharacterFoundEvent(GameEvent):
    character_message: str
    points: int


@dataclass(kw_only=True)
class GameEndedEvent(GameEvent):
    message: str


class EventHandler:
    events: list[GameEvent] = []

    def handle_event(self, event: GameEvent):
        self.events.append(event)
        if isinstance(event, GameEndedEvent) or isinstance(event, ExitFoundEvent):
            self.save_events()

    def save_events(self):
        with open("game_events.jsonl", "a") as f:
            for event in self.events:
                dict_event = asdict(event)
                dict_event["type"] = event.__class__.__name__
                f.write(json.dumps(dict_event) + "\n")

        # Clear the event list after saving to avoid double-writing in current session
        self.events = []
