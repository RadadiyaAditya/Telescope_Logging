# Telescope Log Web Application

## Overview

A **web-based Telescope Logging System** built with **Django (Framework)** and **PostrgreSQL (Database)** to facilitate **astronomical observation logging**. It includes features such as user authentication, real-time updates using Django Channels, and PDF report generation.

## Features

- User authentication and management
- Real-time updates with Django Channels
- PDF report generation using `pdfkit`
- Responsive design with Bootstrap 5

## Tech Stack

- **Backend:** Django
- **Frontend:** HTML, Django Templates
- **Database:** PostgreSQL / SQLite
- **Real-time Communication:** Django Channels (WebSockets)
- **Version Control:** Git & GitHub

## Diagram
```mermaid
%% A custom initialization block for a pastel-lavender background
%% (May not always display on GitHub, but works in Mermaid Live Editor or custom setups)
%%{init: {'theme': 'default', 'themeVariables': { 'background': '#F3E5F5'}}}%%

flowchart TD
    %% Client
    Client("Client Browser"):::client

    %% Frontend
    Frontend("Frontend UI (Django Templates)"):::frontend

    %% Real-time Communication
    Realtime("Real-Time Communication Manager"):::realtime

    %% API Endpoints
    APIGateway("API Gateway (FastAPI)"):::api

    %% Backend Application Server
    Backend("Backend Application Server"):::backend

    %% Database
    DB("Database (SQLite/PostgreSQL)"):::database

    %% Django Project Setup subgraph
    subgraph "Django Project Setup"
        managePy("manage.py"):::config
        settings("Settings"):::config
        urls("URLs"):::config
        asgi("ASGI"):::config
        wsgi("WSGI"):::config
    end

    %% Logging System Application subgraph
    subgraph "Logging System App"
        forms("Forms"):::backend
        views("Views"):::backend
        consumers("Consumers"):::backend
        models("Models"):::backend
        templates("Templates"):::frontend
        lst("LST Calculations"):::backend
        admin("Admin"):::backend
        tests("Tests"):::backend
        migrations("Migrations"):::backend
    end

    %% Relationships between high-level components
    Client -->|"HTTP Request"| Frontend
    Client -->|"REST API Calls"| APIGateway
    Client -->|"WebSocket Connection"| Realtime

    Frontend -->|"Renders Data"| Backend
    Backend -->|"Stores Data"| DB

    %% Integration of configuration into backend and real-time
    managePy --> Backend
    settings --> Backend
    urls --> Backend
    asgi -- "Configures WebSocket" --> Realtime
    wsgi --> Backend

    %% Internal relationships within Logging System App
    views -->|"Uses"| models
    forms --> views
    views -->|"Renders"| templates
    consumers -->|"Performs Calculations"| lst

    %% Connect API layer to configuration (defining endpoints)
    urls --> APIGateway

    %% Pastel Styles for a Light Theme
    classDef client fill:#FFE4E1,stroke:#333,stroke-width:2px,font-size:14px,color:#000;
    classDef frontend fill:#CFE2F3,stroke:#333,stroke-width:2px,font-size:14px,color:#000;
    classDef realtime fill:#D9EAD3,stroke:#333,stroke-width:2px,font-size:14px,color:#000;
    classDef backend fill:#F4CCCC,stroke:#333,stroke-width:2px,font-size:14px,color:#000;
    classDef database fill:#FFF2CC,stroke:#333,stroke-width:2px,font-size:14px,color:#000;
    classDef config fill:#EEEEEE,stroke:#333,stroke-width:2px,font-size:14px,color:#000;
    classDef api fill:#F9C0C0,stroke:#333,stroke-width:2px,font-size:14px,color:#000;

    %% Clickable GitHub Links (with tooltips)
    click managePy "https://github.com/radadiyaaditya/telescope_logging/blob/main/manage.py" "Django Management Script"
    click settings "https://github.com/radadiyaaditya/telescope_logging/blob/main/telescope_log/settings.py" "Django Settings"
    click urls "https://github.com/radadiyaaditya/telescope_logging/blob/main/telescope_log/urls.py" "Django URL Configurations"
    click asgi "https://github.com/radadiyaaditya/telescope_logging/blob/main/telescope_log/asgi.py" "Django ASGI Config"
    click wsgi "https://github.com/radadiyaaditya/telescope_logging/blob/main/telescope_log/wsgi.py" "Django WSGI Config"

    click models "https://github.com/radadiyaaditya/telescope_logging/blob/main/logging_system/models.py" "Django Models"
    click views "https://github.com/radadiyaaditya/telescope_logging/blob/main/logging_system/views.py" "Django Views"
    click forms "https://github.com/radadiyaaditya/telescope_logging/blob/main/logging_system/forms.py" "Django Forms"
    click admin "https://github.com/radadiyaaditya/telescope_logging/blob/main/logging_system/admin.py" "Django Admin Panel"
    click tests "https://github.com/radadiyaaditya/telescope_logging/blob/main/logging_system/tests.py" "Django Test Cases"
    click migrations "https://github.com/radadiyaaditya/telescope_logging/tree/main/logging_system/migrations/" "Django Migrations"
    click consumers "https://github.com/radadiyaaditya/telescope_logging/blob/main/logging_system/consumers.py" "Django WebSockets Consumers"
    click templates "https://github.com/radadiyaaditya/telescope_logging/tree/main/logging_system/templates/logging_system/" "Django Templates"
    click lst "https://github.com/radadiyaaditya/telescope_logging/blob/main/logging_system/lst.py" "Local Sidereal Time Calculations"

    click APIGateway "https://github.com/radadiyaaditya/telescope_logging/blob/main/README.md" "FastAPI Gateway"
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- wkhtmltopdf

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/telescope_log_webapp.git
    cd telescope_log_webapp
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database and update the `.env` file with your database credentials:
    ```
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=your_db_host
    DATABASE_PORT=your_db_port
    ```

5. Apply the database migrations:
    ```sh
    python manage.py migrate
    ```

6. Collect static files:
    ```sh
    python manage.py collectstatic
    ```

7. Run the development server:
    ```sh
    daphne -b 0.0.0.0 -p 8000 telescope_log.asgi:application
    ```

## Configuration

### Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=your_db_host
DATABASE_PORT=your_db_port
```

### PDFKit Configuration

Ensure `wkhtmltopdf` is installed and update the `WKHTMLTOPDF_PATH` in `settings.py`:

```python
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
```

## Usage

### Running the Server

To start the server, run:

```sh
daphne -b 0.0.0.0 -p 8000 telescope_log.asgi:application
```

### Accessing the Application

Open your web browser and navigate to `http://127.0.0.1:8000/`.

### Admin Interface

Access the Django admin interface at `http://127.0.0.1:8000/admin/`. Use the superuser credentials created during the setup.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [wkhtmltopdf](https://wkhtmltopdf.org/)
