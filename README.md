# RetroBoard

<!-- markdownlint-disable MD033 -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img alt="Logo" src="assets/banner-light.svg">
</picture>
<!-- markdownlint-enable MD033 -->

A lightweight, full-stack application for running productive sprint retrospective ceremonies. Built with Python 3, Flask, SQLAlchemy, and a Vue 3 frontend, this app enables team members to anonymously write and later share feedback and ideas about the last sprint.

## What RetroBoard is?

RetroBoard is a collaborative tool for retrospective ceremonies or for other team events where brainstorming is key for success. It helps the team form ideas and share them with others. It is anonymous so everyone can share their thoughts leaving the stepping up part completely optional. With multiple **boards**, every team in an organization can have their separate space and by using **categories** every piece of idea can be sorted to its right place.

## Features

* **Note Management**: Create boards where all the teams can have their own space to add notes to.
* **Categorization**: Sort your notes in different categories which can be either custom or one of the pre-created ones.
* **Privacy Mode**: Show or hide existing notes on the board so it won't influence others.
* **Autosave**: Automatically saves your note if your browser crashes.
* **Brandable**: You can add your logo to the navbar to make it blend in with all your other tools in the organization.

## Data Storage

From the nature of the tool, some data needs to be stored in order for it to work as intended. There are two data storages:

* **SQLite DB**: The boards, categories and notes are stored in an SQLite DB which is persisted on the host computer for resilience across updates.
* **Local storage**: Some settings (e.g. visibility, draft note) are stored on the user's local storage in browser. This is needed for some functions to work properly like persisting the state of the note's visibility or the currently drafted note in case of a sudden crash.

## Under the hood

* **Backend**: Built with Python 3 using Flask & SQLAlchemy.
* **Frontend**: Vue 3 to make the tool fast and simple.
* **Database**: Using SQLite to store the data locally — where it belongs.

## Using the tool

From the start, RetroBoard was made to be user friendly. Here is an example workflow which can be used on the next retrospective ceremony. In the example, the `Retrospective` board template was used.

1. **Create a new board for your team beforehand:** Ask every member invited to the meeting to add their ideas to this before the meeting. This leaves time for everyone to collect their thoughts. Use the Privacy Mode and hide the notes to avoid influencing eachother.
2. **Check the board and discuss:** When the meeting starts, open the board on a central screen where everyone can see the notes and discuss each one in an orderly fashion. You can use *Action items* to create actions from the ideas.
3. **Export to Save**: After all ideas were tackled, export the board and save it for future reference. Choose either JSON or MD format.

### How to run it

The tool lives in a docker container to simple things even futher. It needs to be hosted on your server and expose it to the network, the application will take care of the rest. Make sure you either expose port `8000` or re-route it as you like. Ensure that you assign a persistent directory for storing the database so that its data remains intact across updates.

Here is an example:
```docker run --rm -ti -v path/to/database:/app/backend/database/ -p 8000:8000 ghcr.io/gulyasgergely902/retroboard```

You can also specify a version using tags e.g.: `retroboard:1.1.0`. The complete list of docker versions can be seen under packages.

### How to build it from source

Building from source can provide you with the latest features which are not yet available in the latest release. Please be aware that if you build a newer than released version, it might contain bugs. To open a bug ticket, see **Contribution** section.

1. Build the frontend using `scripts/build_frontend.sh`.
2. Create a virtual environment: `python3 -m venv rb_venv` then `source rb_venv/bin/activate`.
3. Install the required modules in the environment which are needed to run the app: `python3 -m pip install .`.
4. Run the app from the backend using `flask run`.

## Contribution

You can contribute to RetroBoard in two ways:

* **Contribute via an issue:** Open an issue for a feature request or bug report. Use the provided templates which will guide you giving the essential information. Based on current priorities, I’ll add it to one of the milestones and address it in a future release. You can check the milestones with the assigned release date - if any - at **Issues** / **Milestones**.
* **Contribute via code:** Fork the repository and implement the change yourself. Once done, open a pull request. I’ll review your submission and either provide feedback for refinement or merge it. Be sure to check the guidelines in the `CONTRIBUTING.md` file before submitting a pull request. Also if you choose an existing issue from **Issues**, make sure to assign it to yourself.
