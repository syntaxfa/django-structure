# Syntax Django Structure

A robust and scalable Django project structure designed for building modern web applications. This structure emphasizes clean code, separation of concerns, and best practices for development and deployment.

-----

## Features

  * **Modular Architecture**: The project is organized into `apps` and `pkg` for better separation of concerns. Django apps handle specific business logic, while the `pkg` directory contains reusable packages.
  * **JWT Authentication**: Secure user authentication using JSON Web Tokens (JWT) with refresh and access tokens. It includes token verification, refresh, and logout (banning) functionalities.
  * **Rich Error Handling**: A custom `RichError` pattern for detailed and layered error reporting, which simplifies debugging and improves user feedback.
  * **Environment-based Settings**: Separate settings files for `development`, `production`, and `test` environments to manage configurations effectively.
  * **Dockerized Environment**: Comes with `docker-compose.yml` for both development and production, making it easy to set up and run the project with all its services (Postgres, Redis, Celery).
  * **Asynchronous Tasks**: Integrated with **Celery** and **Celery Beat** for handling background tasks and scheduled jobs.
  * **API Documentation**: Automatic API documentation generation with `drf-spectacular`, providing **Swagger** and **Redoc** UIs.
  * **Code Quality and Linting**: Pre-configured with `pre-commit` hooks for `pylint` and `gitlint` to ensure code quality and consistent commit messages.
  * **CI/CD Pipeline**: A basic CI pipeline is set up using GitHub Actions to run tests and linters on pull requests.
  * **Structured Logging**: A standardized logger is implemented to produce structured logs with relevant metadata for better monitoring and debugging.

-----

## Project Structure

```
├── apps                    # Contains Django applications
│   ├── api                 # Handles API routing, responses, and documentation
│   ├── authentication      # Manages user authentication and token handling
│   └── common              # Shared models, utilities, and validations
├── config                  # Project configuration files
│   ├── settings            # Environment-specific settings
│   ├── celery_conf.py      # Celery configuration
│   └── urls.py             # Root URL configuration
├── docs                    # Project documentation
├── pkg                     # Reusable Python packages
│   ├── client              # Utilities for client information (IP, device)
│   ├── email               # Email sending abstractions
│   ├── logger              # Structured logging implementation
│   └── rich_error          # Custom error handling package
├── requirements            # Python dependencies
├── .github/workflows       # GitHub Actions CI/CD workflows
├── compose.yml             # Docker Compose for production
├── compose-development.yml # Docker Compose for development
├── Dockerfile              # Dockerfile for the application
├── entrypoint.py           # Entrypoint script for the Docker container
└── manage.py               # Django's command-line utility
```

-----

## Getting Started

### Prerequisites

  * Docker
  * Docker Compose

### Installation

1.  **Clone the repository:**

    ```shell
    git clone <repository-url>
    cd django-structure
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root directory by copying the example. You will need to fill this out with your own credentials.

3.  **Build and run the application using Docker Compose:**
    For a development environment, run:

    ```shell
    docker compose --file compose-development.yml up -d
    ```

    This command, build the images and start the services.

-----

## Usage

### API Endpoints

The API is versioned and accessible under `/api/v1/`.

#### Authentication Endpoints

  * `POST /api/v1/auth/token/verify/`: Verify the validity of an access or refresh token.
  * `POST /api/v1/auth/token/refresh/`: Obtain a new access token using a refresh token.
  * `GET /api/v1/auth/token/logout/`: Ban the user's tokens, effectively logging them out from all devices.

#### API Documentation

  * **Swagger UI**: `  /api/v1/schema/swagger/ `
  * **Redoc**: `/api/v1/schema/redoc/`

### Running Tests

To run the test suite, you can use the following command:

```shell
make test
```

This will execute the tests inside the Docker container. Tests are located in the `tests.py` file within each package/app.

### Pre-commit Hooks

This project uses `pre-commit` for code quality. To install the hooks:

```shell
pre-commit install
```

The hooks will run automatically on every commit, ensuring that your code adheres to the project's standards. You can also run them manually on all files:

```shell
pre-commit run --all-files
```

-----

## Rich Error Handling

This project uses a custom `RichError` pattern to provide detailed, multi-layered error information. This helps in debugging by preserving the context of an error as it propagates up the call stack.

An error can be wrapped with additional context at each layer:

```python
# Repository Layer
raise RichError(operation="db.get_user").set_msg("User not found")

# Service Layer
try:
    # ... call repository
except Exception as err:
    raise RichError(operation="service.process_user").set_error(err)
```

The `get_error_info` function can then be used to retrieve a list of all error layers for logging or structured responses. For more details, refer to the documentation in `docs/rich_error.md`.

-----

## Deployment

The project is configured for deployment using **Docker**, **Nginx**, and **Gunicorn**. The `compose.yml` file defines the services for a production environment, including the application container, a Celery worker, a Celery beat scheduler, a Postgres database, and Redis.

The `nginx.conf` file is a sample Nginx configuration that can be used as a reverse proxy to serve the Django application.

The `entrypoint.py` script handles database migrations and starts the Gunicorn server with an appropriate number of workers based on the CPU cores available.

-----

## Dependencies

Key dependencies are managed in the `requirements` directory.

  * **`base.txt`**: Core dependencies for the project, such as Django, Django REST Framework, and Simple JWT.
  * **`development.txt`**: Dependencies for the development environment, including `django-debug-toolbar` and `pylint`.
  * **`production.txt`**: Dependencies for the production environment, such as `gunicorn` and `gevent`.
  * **`test.txt`**: Dependencies for running tests, like `model-bakery`.