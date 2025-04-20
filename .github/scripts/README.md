# Python Scripts Documentation

This document describes the purpose, functionality, and usage of two Python scripts: `check_commit_message.py` and `start.py`. These scripts are part of a larger project and serve distinct roles in development and deployment workflows.

## 1. check_commit_message.py

### Overview
The `check_commit_message.py` script enforces a standardized format for Git commit messages. It is designed to be used as a pre-commit hook to validate commit messages before they are accepted, ensuring consistency across the repository.

### Purpose
- Validates that commit messages adhere to a specific format: `<type>: <description>`, where `<type>` is one of `feat`, `chore`, or `fix`.
- Prevents developers from pushing commits with incorrectly formatted messages, improving traceability and changelog generation.

### Code
```python
import sys
import re

# Obtener el archivo temporal que contiene el mensaje de commit desde los argumentos
commit_msg_filepath = sys.argv[1]

# Leer el mensaje de commit
with open(commit_msg_filepath, "r", encoding="utf-8") as file:
    commit_msg = file.read().strip()

# Definir el patrón regex
pattern = r"^(feat|chore|fix): .+"

# Validar el mensaje
if not re.match(r"^(feat|chore|fix): .+", commit_msg):
    print("Error: El mensaje debe seguir el formato 'tipo: descripción'")
    print("Ejemplos válidos:")
    print("feat: agregar login")
    print("chore: actualizar dependencias")
    print("fix: corregir error en API")
    sys.exit(1)

sys.exit(0)
```

### Functionality
1. **Input Handling**:
   - Reads the path to a temporary file containing the commit message from the command-line argument (`sys.argv[1]`).
   - Opens and reads the file with UTF-8 encoding, stripping any trailing whitespace.
2. **Validation**:
   - Defines a regular expression pattern (`^(feat|chore|fix): .+`) that requires:
     - The message to start with one of `feat`, `chore`, or `fix`, followed by a colon and a space.
     - A non-empty description following the colon.
   - Uses `re.match` to check if the commit message conforms to the pattern.
3. **Error Handling**:
   - If the message does not match the pattern, prints an error message with the expected format and valid examples.
   - Exits with a status code of `1`, causing the commit to fail.
   - If the message is valid, exits with a status code of `0`, allowing the commit to proceed.

### Usage
- The script is executed as part of a pre-commit hook, typically configured via a tool like `pre-commit`.
- It is invoked automatically during `git commit`, receiving the path to a temporary file containing the commit message.
- Example valid commit messages:
  - `feat: agregar login`
  - `chore: actualizar dependencias`
  - `fix: corregir error en API`
- Example invalid commit message:
  - `add new feature` (fails because it lacks a valid type prefix).

### Dependencies
- Python standard libraries: `sys`, `re`.

### Notes
- The script enforces a minimal set of commit types (`feat`, `chore`, `fix`). Additional types (e.g., `docs`, `test`) can be added by modifying the regex pattern.
- Ensure the script is executable and located in a directory accessible to the pre-commit hook (e.g., `.github/scripts/`).

## 2. start.py

### Overview
The `start.py` script serves as an entry point for running a Django application using Gunicorn in a production environment. It is designed to be used within a containerized setup, specifically with a Dockerfile that configures a minimal production image.

### Purpose
- Initializes the Gunicorn WSGI server to run the Django application defined in `yana.site_app.wsgi:application`.
- Simplifies the command-line interface for starting the application in a container.

### Code
```python
import sys
import gunicorn.app.wsgiapp as app

if __name__ == "__main__":
    sys.argv[1:] | ["yana.site_app.wsgi:application"]
    app.run()
```

### Functionality
1. **Command-Line Argument Setup**:
   - Replaces the command-line arguments (`sys.argv[1:]`) with a single argument: `yana.site_app.wsgi:application`.
   - This specifies the WSGI application entry point for Gunicorn, pointing to the Django application's WSGI module.
2. **Gunicorn Execution**:
   - Calls `gunicorn.app.wsgiapp.run()` to start the Gunicorn server with the provided WSGI application.
   - Gunicorn handles the server configuration (e.g., port, workers) based on environment variables or default settings.

### Usage
- The script is executed as the `CMD` in a Docker container, as defined in the associated Dockerfile.
- It is typically run with the command:
  ```bash
  python start.py
  ```
- The script assumes the `yana.site_app.wsgi:application` module is available in the Python path, which is configured in the Docker environment.

### Dependencies
- Python standard library: `sys`.
- External package: `gunicorn` (must be installed in the Docker image, typically via `requirements.txt`).

### Environment Variables
- The script relies on environment variables set in the Docker container, such as:
  - `PYTHONPATH`: Ensures the `yana` module and Gunicorn are accessible.
  - `PORT`: Specifies the port for Gunicorn (defaults to `8000` in the Dockerfile).
  - `PYTHONUNBUFFERED`: Ensures logs are output in real-time.

### Notes
- The script is intentionally minimal, delegating most configuration to Gunicorn and the Docker environment.
- Additional Gunicorn options (e.g., number of workers, timeout) can be passed via environment variables or by modifying the script to include them in `sys.argv`.
- The script assumes a Django project structure with a `yana` directory containing the `site_app.wsgi` module.

## Troubleshooting
- **check_commit_message.py**:
  - **Error: "No such file or directory"**: Ensure the temporary commit message file path is correctly passed by the pre-commit hook.
  - **Invalid regex failures**: Verify the commit message matches the expected pattern. Update the regex if additional commit types are needed.
- **start.py**:
  - **ModuleNotFoundError**: Confirm that `gunicorn` is installed and `yana.site_app.wsgi` is in the `PYTHONPATH`.
  - **Port conflicts**: Ensure the `PORT` environment variable is set to an available port.
  - **No output**: Check that `PYTHONUNBUFFERED=1` is set for real-time logging.