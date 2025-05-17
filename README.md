# Simple Python Web Server with Message Form

This is a basic Python web server built with the `http.server` module. It serves HTML pages, processes form submissions, saves messages to a JSON file, and displays them dynamically using Jinja2 templates.

## Features

- **Routing** for multiple pages (`/`, `/message`, `/read`)
- **Form submission** handling (username and message)
- **Data storage** in JSON format (`storage/data.json`)
- **Dynamic rendering** of saved messages using Jinja2
- **Static file serving** (e.g. CSS, images)
- **Custom 404 page** for unknown routes

## Routes

- `/` - Home page (`index.html`)
- `/message` - Page with a message submission form (`message.html`)
- `/read` - Page displaying all saved messages
- `/style.css`, `/logo.png`, etc. - Static assets

## JSON Format

Submitted messages are saved with a timestamp as the key:

```json
{
  "2025-05-17 19:17:16.025156": {
    "username": "John",
    "message": "Hello, world!"
  }
}
```

Getting Started
Prerequisites
Python 3.10+
Jinja2

Install dependencies:
pip install Jinja2

Run the Server
python main.py
The server will start on http://localhost:3000.

Folder Structure

```
├── main.py
├── index.html
├── message.html
├── persons.html
├── style.css
├── logo.png
└── storage/
    └── data.json
```
