# Google Tasks CLI

Small Python script to list your Google Task lists and mark pending tasks as completed from the terminal.

## Features

- OAuth login with token reuse (`token.json`)
- Lists task lists and tasks
- Shows pending tasks in a numbered menu
- Lets you mark one selected task as completed
- Handles missing/invalid credential files with clear messages

## Requirements

- Python 3.10+
- A Google Cloud OAuth client for desktop apps
- `credentials.json` in the project root

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Place your OAuth client file as `credentials.json` in the project root.

## Run

```bash
python main.py
```

On first run, the script opens a Google OAuth flow. After granting access, it stores credentials in `token.json`.

## Notes

- The script uses scope `https://www.googleapis.com/auth/tasks` so it can mark tasks as completed.
- If you change scopes or OAuth client settings, delete `token.json` and re-run.
- Sensitive local files are ignored by Git via `.gitignore`.
