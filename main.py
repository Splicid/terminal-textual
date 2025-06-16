import platform
import psutil, time
import cpuinfo

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Static, Digits, Button, ListView, ListItem
from textual.reactive import reactive
from textual.containers import Container, HorizontalGroup, Horizontal, Vertical


class TimeDisplay(Vertical):
    time = reactive(0.0)

    def compose(self) -> ComposeResult:
        yield Static("Current Time Spent", id="timer-label")
        yield Digits(f"{self.time:.1f}", id="timer")
        
        with Horizontal(classes="button-bar"):
            yield Button("Add Time",    id="add")
            yield Button("Stop",        id="stop_watch")
            yield Button("Resume",      id="resume_watch")
            yield Button("Reset",       id="reset_watch")


    def on_mount(self) -> None:
        self.update_time = self.set_interval(1.0, self.update_time)

    def update_time(self) -> None:
        self.time += 0.1
        self.query_one("#timer", Digits).update(f"{self.time:.1f}")

    def add_time(self) -> None:
        self.time += 100
        self.query_one("#timer", Digits).update(f"{self.time:.1f}")

    def stop_time(self) -> None:
        self.update_time.pause()
        self.total = self.time
        self.time = self.total

    def resume_time(self) -> None:
        self.update_time.resume()

    def reset_time(self) -> None:
        self.time = 0.0
        self.query_one("#timer", Digits).update(f"{self.time:.1f}")
        self.update_time.resume()

class SystemData(Container):
    cpu_usage = reactive(0.0)
    active_programs = reactive(list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.approved_apps = {"Google Chrome", "Godot", "1Password", "Discord"}
        self.platform_name = platform.system()
        self.cpu_brand = cpuinfo.get_cpu_info().get("brand_raw", "Unknown CPU")
        self.app_times: dict[str, float] = {app: 0.0 for app in self.approved_apps}
        self._last_check = time.time()

        # Define the widget here so it exists before Textual calls any watchers
        self.cpu_usage_display = Static(f"CPU Usage: 0%", id="cpu-usage-box")
        self.process_list_widget = ListView(id="proc-list")

    def on_mount(self):
        # Update CPU usage every second
        self.set_interval(1.0, self.update_cpu_usage)
        self.set_interval(1.0, self.update_active_programs)

    def update_cpu_usage(self):
        self.cpu_usage = psutil.cpu_percent()

    def _refresh_process_list(self) -> None:
        """Rebuild the ListView so timers are updated every tick."""
        self.process_list_widget.clear()
        for name in self.active_programs:
            elapsed = self.app_times.get(name, 0.0)
            self.process_list_widget.append(
                ListItem(Static(f"{name} — {elapsed:6.1f}s"))
            )

    def compose(self) -> ComposeResult:
        yield Static(f"Platform: {self.platform_name}", id="platform-box")
        yield Static(f"CPU: {self.cpu_brand}", id="cpu-brand-box")
        yield Static(f"Current Programs: {self.active_programs}")
        yield self.process_list_widget
        yield self.cpu_usage_display  

    def watch_cpu_usage(self, usage: float):
        self.cpu_usage_display.update(f"CPU Usage: {usage}%")

    def update_active_programs(self) -> None:
        now  = time.time()
        dt   = now - self._last_check
        self._last_check = now
        
        # “active” == psutil.STATUS_RUNNING
        running = {p.info["name"]
                   for p in psutil.process_iter(["name", "status"])
                   if p.info["status"] == psutil.STATUS_RUNNING
                   and p.info["name"] in self.approved_apps}
        
        for app in running:
            self.app_times[app] += dt

        self.active_programs = sorted(running)

        # Force a redraw so elapsed times stay current
        self._refresh_process_list()

class HorizontalLayoutExample(App):
    CSS_PATH = "css/vertical_layout.tcss"
    
    def compose(self) -> ComposeResult:
        yield TimeDisplay(classes="box")
        yield SystemData(classes="box")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            self.query_one(TimeDisplay).add_time()
        elif event.button.id == "stop_watch":
            self.query_one(TimeDisplay).stop_time()
        elif event.button.id == "resume_watch":
            self.query_one(TimeDisplay).resume_time()
        elif event.button.id == "reset_watch":
            self.query_one(TimeDisplay).reset_time()


if __name__ == "__main__":
    HorizontalLayoutExample().run()