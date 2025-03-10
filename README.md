# Charter Company Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.1.3-green.svg)](https://flask.palletsprojects.com/)

A full-stack web application for managing charters and crew assignments in a charter company. This project was developed as a capstone for the Udacity Full Stack Web Developer Nanodegree.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Authentication & Authorization](#authentication--authorization)
- [Installation & Setup](#installation--setup)
- [Running Tests](#running-tests)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)

## 🚢 Overview

The Charter Company Management System provides a streamlined interface for managing charter bookings and skipper assignments. As the Head of the Charter Department, you can use this application to manage charters, assign crew members, track departures, and maintain your fleet operations in one centralized platform.

## ✨ Features

- **Charter Management**: Create, view, update, and delete charter bookings
- **Skipper Assignments**: Manage skipper assignments to specific charters
- **Role-Based Access Control**: Different permission levels for various roles in the organization
- **RESTful API**: Full API access with proper authentication and authorization
- **Secure Authentication**: JWT-based authentication with Auth0 integration

## 📊 Data Models

The application is built around two core models:

### Charter Model

```
Charter {
  id: Integer (Primary Key)
  charters_name: String
  departure_date: Date
  skippers: Relationship to Skipper model
}
```

### Skipper Model

```
Skipper {
  id: Integer (Primary Key)
  name: String
  age: Integer
  gender: String
  charter_id: Integer (Foreign Key to Charter)
}
```

## 🔌 API Endpoints

### Charter Endpoints

| Method | Endpoint | Description | Required Permission |
|--------|----------|-------------|---------------------|
| GET | `/charters` | Retrieve all charters | `view:charters` |
| POST | `/charters/create` | Create a new charter | `create:charter` |
| PATCH | `/charters/patch/<id>` | Update a charter | `edit:charter` |
| DELETE | `/charters/delete/<id>` | Delete a charter | `delete:charter` |

### Skipper Endpoints

| Method | Endpoint | Description | Required Permission |
|--------|----------|-------------|---------------------|
| GET | `/skippers` | Retrieve all skippers | `view:skippers` |
| POST | `/skippers/create` | Create a new skipper | `create:skipper` |
| PATCH | `/skippers/patch/<id>` | Update a skipper | `edit:skipper` |
| DELETE | `/skippers/delete/<id>` | Delete a skipper | `delete:skipper` |

### API Usage Examples

Retrieve all charters:
```bash
curl -X GET \
  https://charterscompany.herokuapp.com/charters \
  -H 'Authorization: Bearer <YOUR_JWT_TOKEN>'
```

Create a new skipper:
```bash
curl -X POST \
  https://charterscompany.herokuapp.com/skippers/create \
  -H 'Authorization: Bearer <YOUR_JWT_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John Smith",
    "age": 35,
    "gender": "male",
    "charter_id": 1
  }'
```

## 🔐 Authentication & Authorization

The application uses Auth0 for authentication and implements role-based access control. Three roles are available:

### Charter Assistant
- Can view skippers and charters
- Permissions: `view:charters`, `view:skippers`

### Charter Director
- All Charter Assistant permissions
- Can add, delete, and modify skippers
- Can modify charters
- Permissions: `view:charters`, `view:skippers`, `create:skipper`, `delete:skipper`, `edit:skipper`, `edit:charter`

### Head of the Charter Department
- All Charter Director permissions
- Can add and delete charters
- Permissions: `view:charters`, `view:skippers`, `create:skipper`, `delete:skipper`, `edit:skipper`, `edit:charter`, `create:charter`, `delete:charter`

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip3
- virtualenv (recommended)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/charter-company.git
   cd charter-company
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Set up your database:
   ```bash
   # Create a PostgreSQL database
   sudo -u postgres createdb charters
   
   # Apply migrations
   python3 manage.py db upgrade
   ```

5. Start the application:
   ```bash
   gunicorn app:app
   ```

## 🧪 Running Tests

The application includes a comprehensive test suite that verifies endpoint functionality and permission controls:

```bash
# Create a test database
sudo -u postgres createdb test_db

# Run tests
python3 test_app.py
```

## 💻 Technology Stack

- **Backend**: Flask, Python
- **Database**: PostgreSQL, SQLAlchemy
- **Authentication**: Auth0, JWT
- **Deployment**: Heroku
- **Other Tools**: Flask-Migrate, Flask-CORS, Gunicorn

## 🤝 Contributing

Contributions to this project are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
