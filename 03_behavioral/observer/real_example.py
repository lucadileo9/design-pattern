# ==========================================
# OBSERVER — Real Example: Event-driven UI
# ==========================================
# In a graphical interface, a component (e.g., a button) is the
# Subject. When the user interacts with it, different Observers
# react independently: update the UI, write a log, track
# analytics, etc.
#
# The button doesn't know WHO is observing it nor WHAT the observers do.
# It only knows it must call their on_event() method.
# This is exactly how modern UI frameworks work
# (React, Vue, Qt, Tkinter, WPF…).

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# ==========================================
# EVENT — data associated with an interaction
# ==========================================

@dataclass
class Event:
    """Describes a user interaction with a UI component."""
    type: str                   # "click", "input", "submit"
    source: str                 # name of the component that generated the event
    data: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


# ==========================================
# OBSERVER — common interface
# ==========================================

class EventListener(ABC):
    """Anyone who wants to react to UI events implements this interface."""

    @abstractmethod
    def on_event(self, event: Event) -> None:
        ...


# ==========================================
# SUBJECT — generic UI component
# Note that we could have directly created a specific Subject (like a button),
# but this way we can reuse the listener management logic for
# any UI component.
# ==========================================

class UIComponent:
    """Subject: a UI component that emits events."""

    def __init__(self, name: str):
        self.name = name
        self._listeners: dict[str, list[EventListener]] = {}

    def register(self, event_type: str, listener: EventListener) -> None:
        """Registers a listener for a specific event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def remove(self, event_type: str, listener: EventListener) -> None:
        """Removes a listener from an event type."""
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def _emit(self, event_type: str, data: dict | None = None) -> None:
        """Notifies all listeners registered for this event type."""
        event = Event(type=event_type, source=self.name, data=data or {})
        for listener in self._listeners.get(event_type, []):
            listener.on_event(event)


# ==========================================
# CONCRETE UI COMPONENTS
# ==========================================

class Button(UIComponent):
    """A clickable button."""

    # Note that the Button class in its "main method" or in the method
    # related to the observer pattern simply:
        # 1. performs the button-specific operation (e.g., click), in this case a simple print
        # 2. calls _emit() to notify all listeners registered for this event
    # The button does NOT worry about who the listeners are, what they do, how they react, etc.
    def click(self) -> None:
        print(f"\n[{self.name}] 🖱️ Click!")
        self._emit("click")


class TextField(UIComponent):
    """A text input field."""

    def __init__(self, name: str):
        super().__init__(name)
        self.value = ""

    def write(self, text: str) -> None:
        self.value = text
        print(f"\n[{self.name}] ⌨️ Text entered: '{text}'")
        self._emit("input", {"value": text})


class Form(UIComponent):
    """A form that can be submitted."""

    def __init__(self, name: str):
        super().__init__(name)
        self.fields: dict[str, str] = {}

    def set_field(self, key: str, value: str) -> None:
        self.fields[key] = value

    def submit(self) -> None:
        print(f"\n[{self.name}] 📨 Form submitted with data: {self.fields}")
        self._emit("submit", dict(self.fields))


# ==========================================
# CONCRETE OBSERVERS
# ==========================================
# Each observer reacts in its own way. The UI component knows
# nothing about them — it calls on_event() and that's it.

class Logger(EventListener):
    """Writes every event to a log (simulates writing to a file)."""

    def __init__(self):
        self.log: list[str] = []

    def on_event(self, event: Event) -> None:
        line = f"[{event.timestamp}] {event.type.upper()} on '{event.source}'"
        self.log.append(line)
        print(f"  📝 Logger: {line}")


class Analytics(EventListener):
    """Counts interactions by type (simulates a tracking system)."""

    def __init__(self):
        self.counters: dict[str, int] = {}

    def on_event(self, event: Event) -> None:
        key = f"{event.source}:{event.type}"
        self.counters[key] = self.counters.get(key, 0) + 1
        print(f"  📊 Analytics: {key} → {self.counters[key]} time(s)")


class Validator(EventListener):
    """Checks that a field is not empty (real-time validation)."""

    def on_event(self, event: Event) -> None:
        value = event.data.get("value", "")
        if value.strip():
            print(f"  ✅ Validator: '{event.source}' → OK")
        else:
            print(f"  ❌ Validator: '{event.source}' → empty field!")


class UIUpdate(EventListener):
    """Simulates updating a UI element."""

    def __init__(self, element: str):
        self.element = element

    def on_event(self, event: Event) -> None:
        if event.type == "submit":
            print(f"  🔄 UI: '{self.element}' updated with the form data")
        elif event.type == "click":
            print(f"  🔄 UI: '{self.element}' reacts to the click")


# ==========================================
# USAGE
# ==========================================

if __name__ == "__main__":

    # --- Shared observers ---
    logger = Logger()
    analytics = Analytics()
    validator = Validator()
    update_table = UIUpdate("Users table")

    # --- UI Components ---
    btn_save = Button("Save Button")
    field_name = TextField("Name Field")
    registration_form = Form("Registration Form")

    # --- Listener registration (who listens to what) ---
    btn_save.register("click", logger)
    btn_save.register("click", analytics)
    btn_save.register("click", update_table)

    field_name.register("input", logger)
    field_name.register("input", analytics)
    field_name.register("input", validator)

    registration_form.register("submit", logger)
    registration_form.register("submit", analytics)
    registration_form.register("submit", update_table)

    print("=" * 50)
    print("  EVENT-DRIVEN UI — Observer Pattern")
    print("=" * 50)

    # ---- 1. Click on the button → 3 observers react ----
    btn_save.click()

    # ---- 2. Input in the text field → real-time validation ----
    field_name.write("Mario Rossi")
    field_name.write("")           # validation fails

    # ---- 3. Form submission ----
    registration_form.set_field("name", "Mario Rossi")
    registration_form.set_field("email", "mario@example.com")
    registration_form.submit()

    # ---- 4. Second click (analytics counts) ----
    btn_save.click()

    # ---- 5. Removing a listener ----
    print("\n--- Removing the Logger from the button ---")
    btn_save.remove("click", logger)
    btn_save.click()               # the logger NO LONGER reacts

