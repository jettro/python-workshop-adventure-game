# Add events to the Game and a way to store them
In the next section, you are experimenting with Python Notbooks and data. To have some data, you add events to the game.

The game needs to emit events to listeners. Therefore you need to store EventListeners in the Game. Next, you need to emit events to all listeners.

## Create the events
Events:
- GameStartedEvent: provide height, width, and a message
- PlayerMovedEvent: provide the direction and a message
- MoveFailedEvent: provide the direction and a message
- CharacterFoundEvent: provide the character_message and the points
- ExitFoundEvent: provide the row, column and a message 
- GameEndedEvent: provide the message

Create the GameEvent class in a new file named <b>events.py</b>.

Make all events extend the GameEvent class. The property kw_only=True is needed to make the timestamp field keyword only. Without this, you cannot add fields without a default value after the field with a default value. Which is a problem for having the subclasses. This does mean you cannot create an instance of the class with positional initialization of parameters. Valid is GameEvent(score=10), not valid is GameEvent(10).  

The ABC super class does nothing by itself, it is more a design intent that other classes should inherit from it.

```python
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

```

### Assignments
- Add GameEvent class and create the events as specified above in the events.py file.

## Connect event listeners and emit events

Next, you are connecting the event listeners to the <b>game</b> class and start emitting events. You need to initialise an array of event listeners, create a method to emit events. 

```python
from typing import Callable

event_listeners = []

def add_event_listener(self, listener: Callable[[GameEvent], None]):
    self.event_listeners.append(listener)

def __emit_event(self, event: GameEvent):
    for listener in self.event_listeners:
        listener(event)

```

Next, you can emit the events. Below is an example of emitting a GameStartedEvent. You can add emitting all the other events.

```python
self.__emit_event(GameStartedEvent(
    game_id=self.game_id, 
    score=self.score, 
    height=self.board.height, 
    width=self.board.width,
    row=self.board.player_location[0],
    column=self.board.player_location[1]    
))
```

### Assignments
- Add the event listeners and emit events.

## Create the event listener
The event listener is a class that listens to events and stores them. Save all events to a file on receiving the GameEndedEvent or the ExitFoundEvent.

```python
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
```
Next, register the event listener in the Game before starting the game with run.

### Assignments
- Create the EventHandler class in events.py and register it in the Game.
- Play the game and notice the events are saved to the file.
