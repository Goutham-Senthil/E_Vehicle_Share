# E-Vehicle Share Platform

A full-stack electric vehicle sharing and fleet management web application built with Django. Developed as a collaborative team project.

## Overview

E-Vehicle Share simulates a real-world EV rental and fleet management platform with distinct workflows for three user roles: Customers, Operators, and Managers.

Built collaboratively by:
- [Prajwal Pawan Save](https://github.com/prajwalsave)
- [Goutham Senthil](https://github.com/Goutham-Senthil)


## Features

### Multi-Role Access Control
- **Customers** — browse and book vehicles, manage reservations, make payments, report issues
- **Operators** — update vehicle status, charge and repair vehicles, track availability
- **Managers** — fleet analytics dashboard, utilisation metrics, revenue overview, battery distribution reports

### Vehicle Sharing System
- Real-time vehicle availability and booking flow
- Location tracking (lat/long) per vehicle
- Hourly rate billing and payment settlement
- Reservation lifecycle management (In Use → Completed)

### Modular Django Architecture
Five Django apps with clean separation of concerns:
- `customers` — custom user model, vehicles, reservations, payments
- `operators` — charging and maintenance records
- `managers` — fleet analytics and reporting
- `landing_start` — authentication, registration, public pages
- `e_vehicle_share` — core settings and URL routing

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 4.2 |
| Frontend | HTML, Django Templates, Bootstrap |
| Database | SQLite (development) |
| Auth | Custom AbstractBaseUser with role-based flags |


## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/prajwalsave/E_Vehicle_Share.git
cd E_Vehicle_Share
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Seed the database (Recommended)
To quickly populate the app with test users and a fleet of vehicles:
```bash
python seed_db.py
```
Refer to the [Test Credentials](#test-credentials) section below for login details.

### 6. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

App runs at: `http://127.0.0.1:8000/`

## Demo Login Credentials (Default Test Accounts)

### Customer Login
Username: goutham1  
Password: password1  

### Operator Login
Username: goutham2  
Password: password1  

### Manager Login
Username: goutham3  
Password: password1 


## Testing

The project uses `pytest-django` for automated testing.

### Run full test suite:
```bash
pytest tests/test_suite.py -v
```

### CI/CD
GitHub Actions is configured to run the test suite automatically on every push to `main`. See `.github/workflows/ci.yml`.

---

## Test Credentials

If you ran `seed_db.py`, the following accounts are available (Password for all: `password123`):

| Role | Username |
| :--- | :--- |
| **Manager** | `manager1` |
| **Operator** | `operator1` |
| **Customer** | `customer1` |
| **Customer** | `customer2` |

### Demo Login Credentials (Default Test Accounts)

#### Customer Login
- **Username**: `goutham1`
- **Password**: `password1`

#### Operator Login
- **Username**: `goutham2`
- **Password**: `password1`

#### Manager Login
- **Username**: `goutham3`
- **Password**: `password1`

---

## Project Structure
```bash
e_vehicle_share/
│
├── customers/          # Custom user model, vehicles, reservations, payments
├── managers/           # Fleet analytics and management dashboard
├── operators/          # Vehicle charging and maintenance workflows
├── landing_start/      # Auth, registration, landing pages
├── e_vehicle_share/    # Core settings, URL routing
│
├── manage.py
├── requirements.txt
└── README.md
```

## License

MIT License — see [LICENSE.txt](LICENSE.txt)
