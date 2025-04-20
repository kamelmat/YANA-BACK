[![GCP Production CI/CD Pipeline](https://github.com/IgrowkerTraining/i005-yana-back/actions/workflows/backend.yaml/badge.svg)](https://github.com/IgrowkerTraining/i005-yana-back/actions/workflows/backend.yaml)

# Yana Backend

This guide explains how to set up the development environment for the `yana-back` Django application, configure a pre-commit hook to enforce standardized commit messages, run the server locally, and use Docker to containerize the application.

## Prerequisites
Before starting, ensure the following are installed and configured:
- **Python 3.7 or higher**: Required for the application, validation script, and pre-commit.
- **Git**: Needed for version control and commit operations.
- **pip**: Python package manager, typically included with Python.
- **Docker**: Required for building and running the containerized application.
- **Virtual environment (recommended)**: To isolate dependencies and avoid conflicts.

## 1. Set Up the Development Environment

### 1.1 Create and Activate a Virtual Environment
A virtual environment keeps dependencies isolated and is highly recommended.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On Linux/macOS
source venv/bin/activate
```

**Note**: After activation, your terminal prompt should show `(venv)`.

### 1.2 Install Pre-Commit
Install the `pre-commit` package to manage commit validation hooks.

```bash
pip install pre-commit
```

**Verification**: Check the installed version to confirm:
```bash
pre-commit --version
```

## 2. Configure the Commit Message Validation Hook

The pre-commit hook ensures all commit messages follow the Conventional Commits format (`<type>: <description>`, where `<type>` is `feat`, `chore`, or `fix`).

### 2.1 Create the Validation Script
The script checks commit message format and blocks invalid commits.

- **File Path**: `.github/scripts/check_commit_message.py`
- **Permissions** (Linux/macOS): Ensure the script is executable:
  ```bash
  chmod +x .github/scripts/check_commit_message.py
  ```

### 2.2 Configure the Pre-Commit Hook
Define the hook in a configuration file to integrate with `pre-commit`.

- **File Path**: `.pre-commit-config.yaml` (place in the project root)

## 3. Install and Test the Hook

### 3.1 Install the Hook
Install the pre-commit hook to validate commit messages automatically.

```bash
pre-commit install --hook-type commit-msg
```

**Verification**: Confirm the hook is installed:
```bash
ls -l .git/hooks/ | grep commit-msg
```
You should see a `commit-msg` file created by `pre-commit`.

### 3.2 Test the Hook
Test the hook to ensure it enforces the correct format.

- **Manual Test**:
  ```bash
  pre-commit run --hook-stage commit-msg --commit-msg "feat: test commit"
  ```
  This should pass. Test an invalid message:
  ```bash
  pre-commit run --hook-stage commit-msg --commit-msg "invalid commit"
  ```

- **Real Commit Test**:
  ```bash
  git commit -m "feat: add test file"
  ```
  Try an invalid message:
  ```bash
  git commit -m "bad message"
  ```
  The hook will block invalid commits and show valid examples.

## 4. Run the Server Locally

To run the Django application locally for development:

- **Install dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

- **Start the server**:
  ```bash
  python3 site_app/manage.py runserver
  ```
  Access the app at `http://localhost:8000`.

### 4.1 Dockerfile Overview
The `Dockerfile` is a script that builds a Docker image for the Django app.

- **What It Does**:
  - Starts with a Python base image to install dependencies.
  - Copies the app code and a startup script (`start.py`).
  - Creates a minimal, secure image for running the app with Gunicorn.
  - Runs the server on port `8000` by default.

- **Environment Variables**:
  The application requires specific configuration settings to connect to a database and secure the app. These settings are provided as environment variables. The repository includes a `.env.example` file with the required variables:
  ```plaintext
  DB_NAME=
  DB_USER=
  DB_PASSWORD=
  DB_HOST=
  DB_PORT=
  SECRET_KEY=
  ```
  To configure the app:
  1. Copy `.env.example` to a new file named `.env`:
     ```bash
     cp .env.example .env
     ```
  2. Open `.env` in a text editor and fill in the values for each variable (e.g., database name, user, password, host, port, and a secure secret key).
  3. Save the `.env` file and keep it secure (do not commit it to Git).

- **Usage**:
  Build and run the Docker container, passing the environment variables from the `.env` file:
  ```bash
  # Build the Docker image
  docker build -t yana-back .

  # Run the container with the .env file
  docker run --env-file .env -p 8000:8000 yana-back
  ```
  Access the app at `http://localhost:8000`.

### 4.2 .dockerignore Overview
The `.dockerignore` file lists files and folders to exclude from the Docker image, keeping it small and secure.

- **What It Excludes**:
  - Documentation (e.g., `README.md`).
  - Git files (e.g., `.git`, `.gitignore`).
  - Virtual environments (e.g., `venv/`, `.venv/`).
  - Python caches (e.g., `__pycache__/`, `*.pyc`).
  - Development files (e.g., `.pytest_cache/`, `*.log`).
  - Configuration files (e.g., `.pre-commit-config.yaml`, `.github/workflows/`).

- **Why It’s Important**:
  - Reduces image size.
  - Improves build speed.
  - Prevents sensitive files from being included.
