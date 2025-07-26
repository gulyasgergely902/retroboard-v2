# Contributing Guidelines

Here are a few simple rules to follow when contributing to RetroBoard:

## Directory layout

* `assets/`: Contains all assets for readme files (images mainly)
* `docker/`: Docker file for running RetroBoard
* `frontend/`: Frontend (Vue) code
* `src/`: Backend (Python) code

## Code

* Set up `prettier` and use the existing prettier config against your frontend code.
* Organize imports using `isort` on python code.
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
* All commit messages should follow the accepted structure:

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

## Issue Reporting

* Search existing issues before opening a new one.
* Always use the issue templates.
