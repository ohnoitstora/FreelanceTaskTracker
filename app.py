import json
import time
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Label, Static
from textual.containers import Container

task_list = []

def load_tasks():
    global task_list
    try:
        with open("tasks.json", "r") as f:
            task_list = json.load(f)
    except Exception:
        task_list = []

def save_tasks():
    global task_list
    with open("tasks.json", "w") as f:
        json.dump(task_list, f)

class FreelanceTaskTracker(App):
    CSS = """
    Screen {
        background: #222;
    }
    #main {
        width: 60%;
        margin: auto;
        padding: 2;
        border: solid #444;
        background: #333;
    }
    Input {
        width: 80%;
        margin-bottom: 1;
        background: #111;
        color: #fff;
        border: solid #666;
    }
    Button {
        width: 18%;
        margin-left: 1;
        background: #c00;
        color: #fff;
        border: solid #fff;
    }
    #tasks {
        margin-top: 2;
        background: #222;
        border: solid #555;
        padding: 1;
    }
    Label {
        margin-bottom: 1;
        color: #0f0;
        background: #222;
    }
    #sync-btn {
        background: #08f;
        color: #fff;
        border: solid #fff;
        margin-top: 1;
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        load_tasks()
        yield Header()
        yield Footer()
        with Container(id="main"):
            self.input = Input(placeholder="Type your task here...", id="task-input")
            yield self.input
            self.add_btn = Button("Add Task", id="add-btn")
            yield self.add_btn
            self.sync_btn = Button("Sync", id="sync-btn")
            yield self.sync_btn
            self.tasks_container = Container(id="tasks")
            yield self.tasks_container
            self.status_label = Label("", id="status")
            yield self.status_label
        self.refresh_tasks()

    def refresh_tasks(self):
        self.tasks_container.remove_children()
        for t in task_list:
            lbl = Label(t)
            self.tasks_container.mount(lbl)

    def on_button_pressed(self, event):
        global task_list
        if event.button.id == "add-btn":
            val = self.input.value
            if val.strip():
                task_list.append(val)
                save_tasks()
                self.input.value = ""
                self.status_label.update("Task added!")
                self.refresh_tasks()
            else:
                self.status_label.update("Type something!")
        elif event.button.id == "sync-btn":
            self.status_label.update("Syncing...")
            time.sleep(2)
            self.status_label.update("Synced! (not really)")

if __name__ == "__main__":
    FreelanceTaskTracker().run()
