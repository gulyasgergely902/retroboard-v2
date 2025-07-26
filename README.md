# RetroBoard

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/gulyasgergely902/retroboard-v2)](https://github.com/gulyasgergely902/retroboard-v2/issues)
[![GitHub stars](https://img.shields.io/github/stars/gulyasgergely902/retroboard-v2)](https://github.com/gulyasgergely902/retroboard-v2/stargazers)
[![Docker Image](https://img.shields.io/badge/Docker-Available-blue)](https://ghcr.io/gulyasgergely902/retroboard)

![Logo](.github/logo.svg)

A lightweight, full-stack application for running productive sprint retrospective ceremonies. Built with Python 3, Flask, SQLAlchemy, and a Vue 3 frontend, this app enables team members to anonymously write and later share feedback and ideas about the last sprint.

## What it Does

Built with collaborative teams in mind for an efficient retrospective ceremony:

* 🧠 **Write your thoughts in private**: Everyone can write down their feedback about the last sprint — but you won’t see what others wrote until everyone is ready to discuss. This keeps the input unbiased and personal.
* 👀 **Reveal mode when it's time to discuss**: Once everyone’s done writing, we switch to a reveal page that shows all the ideas for group discussion.
* 🚀 **Fast, clean, no clutter**: Just the essentials — no logins, no bloat, no distractions. Open the link, write your thoughts, done.
* 🔐 **Fully self-hosted**: You can run it on your own servers or environment, so you stay in control of your data — perfect if your company has privacy or security policies.

## The tech behind

* **Backend**: Built with Python 3 using Flask & SQLAlchemy.
* **Frontend**: Vue 3 to make the tool fast and simple.
* **Database**: Using SQLite to store the data locally — where it belongs.

## Using to tool

This is cool, but how should I use it? Here is a simple breakdown:

1. Before starting the retrospective meeting, create a new board for your thoughts. Everyone at the meeting will add their ideas to this.
2. When the meeting starts, everyone opens the app and writes their feedback to different categories from the last sprint. Don't worry, no-one can see these at this stage, yet.
3. After the team finished adding new ideas, the faciliator of the meeting reveals the notes and the team checks them together.

## How to run it

The tool lives in a docker compose to simple things even futher. It needs to be hosted on your server and expose it to the network, the application will take care of the rest. Make sure you either expose port `5000` or re-route it as you like. Ensure that you assign a persistent directory for the database so data remains persistent across updates.

## Build from source

In rare cases when you want to build it from the source, it is not any harder.

### Frontend

1. Navigate to the `frontend` directory: `cd frontend`.
2. `pnpm install --force`
3. `pnpm format`
4. `pnpm build`

### Backend

1. Create a virtual environment: `python3 -m venv venv`.
2. Activate the virtual environment:
   * On Linux/macOS: `source venv/bin/activate`
   * On Windows: `venv\Scripts\activate`
3. Install the required modules in the environment which are needed to run the app:
   `python3 -m pip install .`
4. Set the `FLASK_APP` environment variable to the entry point of the application (e.g., `export FLASK_APP=app.py` on Linux/macOS or `set FLASK_APP=app.py` on Windows).
5. Run the app from the root using `flask run`.

## Contribution

You can contribute to RetroBoard in two ways:

* Open an issue for a feature request or bug report. Based on current priorities, I’ll add it to the roadmap and address it in a future release.
* Fork the repository and implement the change yourself. Once done, open a pull request. I’ll review your submission and either provide feedback for refinement or merge it. Be sure to check the guidelines in the `CONTRIBUTING.md` file before submitting a pull request.
