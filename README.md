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

### 5. Create a superuser (optional, for Django admin access)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
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
