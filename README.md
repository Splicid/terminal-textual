# Rich Terminal

This project is a Textual-based terminal application that displays current time spent and system data such as CPU usage and active approved processes.

## Features

- **Time Display:**  
  Displays the elapsed time with controls to add time, stop, resume, or reset the timer. See [`TimeDisplay`](main.py#L6) in [main.py](main.py).

- **System Data Monitoring:**  
  Shows platform, CPU brand, CPU usage, and a list of active approved applications with their runtime. See [`SystemData`](main.py#L38) in [main.py](main.py).

- **Horizontal Layout:**  
  Uses a custom CSS file for a vertical layout styling. See [css/vertical_layout.tcss](css/vertical_layout.tcss).

## Requirements

- Python 3.11  
- Pipenv

## Setup & Run

1. **Install dependencies:**

   ```sh
   pipenv install


   rich-terminal/
├── [main.py](http://_vscodecontentref_/0)
├── Pipfile
├── [Pipfile.lock](http://_vscodecontentref_/1)
├── [README.md](http://_vscodecontentref_/2)
└── css/
    └── [vertical_layout.tcss](http://_vscodecontentref_/3)