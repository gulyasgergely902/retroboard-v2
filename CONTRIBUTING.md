# Contributing Guidelines

Here are a few simple rules to follow when contributing to RetroBoard:

## Directory layout

* `assets/`: Contains all assets for readme files (images mainly).
* `backend/`: Backend (Python) code.
* `docker/`: Docker file for running RetroBoard.
* `frontend/`: Frontend (Vue) code.
* `scripts/`: All the scripts which also runs on CI.

## Development

To enable linting during development for the backend, make sure to install the optional development dependencies as well:

```python3 -m pip install -e .[dev]```

If you want to run RetroBoard in a live environment, follow these steps:

* Run the backend with flask from the backend directory: `flask run`
* Run frontend with pnpm: `pnpm run dev`

After this, the application will be available on `localhost:5173`.

> [!NOTE]
> pip install `-e` is used to install the package in editable mode, which is useful during development. It allows you to make changes to the code without needing to reinstall the package.

## Code

* Always use the provided scripts `lint_backend.sh` and `lint_frontend.sh` to check your code for issues.
* Keep your code clean, modular, and readable.
* Variable names should clearly reflect their purpose and usage.

## Documentation

* All comments should be complete sentences, start with a capital letter, and end with a period.
* Public functions, classes, and modules should include docstrings or relevant documentation.
* Update the README or relevant docs if your change affects usage or features.

## Git

All git commit messages should follow the general rules:

* Separate your commits into logically grouped changes. For example, frontend and backend modifications should be in separate commits. This principle can be applied at even finer levels — keep each commit focused and coherent to make code review and debugging easier.
* Use the imperative mood in the subject line. E.g. "Implement x/y changes." instead of "Implemented x/y changes."
* All fixup commits must be squashed before opening a pull request.
* All commit messages should follow the accepted structure where the commit message starts with a tag which represents the scope of the change then the change's short description starting with a capital letter followed by an optional longer description separated by an empty line:

```text
tag: Short description of changes

Optional longer description to provide additional context.
```

In most cases, a short descriptive tag is sufficient for a commit message. However, contributors are free to include a longer description if they feel it adds clarity or context to the changes.

* The accepted tags are:
  * `assets`: Asset changes for readme related modifications.
  * `backend`: Any backend related change.
  * `ci`: Changes in the ci/cd pipelines. E.g. adding a new worflow to GitHub Actions.
  * `docker`: Changes in docker file.
  * `docs`: Changes in markdown files (README, CONTRIBUTING, etc.).
  * `frontend`: Any frontend related change. No need more granularity.
  * `misc`: This category is for any changes that do not affect backend or frontend code — for example, configuration files, or scripts.
  * `style`: Style-only changes (e.g. formatting, indentation, whitespace) should be used sparingly and ideally included within relevant commits. Avoid making standalone styling commits unless absolutely necessary.
  * `tests`: Any test related changes either for backend or frontend. All modified tests should be grouped together and comitted separately from other changes with this tag.

## Before submitting a Pull Request

* Check if your code builds and runs correctly.
* There should be no linting or formatting errors.
* Pull request description should be clear and helpful.

## After opening a Pull Request

* Wait for all the checks to run and fix the issues if any came up.
* Make sure to check back on the PR regularly to see if any comment or change request was issued.

> [!NOTE]
> Stale Pull Requests will be closed in 1 week if there is no activity to comments and the checks are failed / changes were requested!

## Issue Reporting

* Search existing issues before opening a new one.
* Always use the issue templates.
