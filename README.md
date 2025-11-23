# E-Vehicle Share Platform  
A Django-based multi-role electric vehicle sharing system

## Overview
E-Vehicle Share is a full-stack web application built using Django that simulates a real-world electric vehicle rental and fleet management platform. It supports multiple user roles, operational workflows, and modular backend logic. This project demonstrates full-stack development, structured design, and practical experience with Python and Django.

## Features

### Multi-Role Access
- Customers: browse vehicles, book rides, manage profiles  
- Managers: oversee operations, supervisory control, fleet management  
- Operators: update vehicle status, track availability, manage routine tasks  

### Vehicle Sharing System
- View and manage available electric vehicles  
- Reservation and booking flow  
- Vehicle status and maintenance tracking  

### Modular Architecture
The platform is divided into multiple Django apps:
- customers  
- managers  
- operators  
- e_vehicle_share (core settings and URLs)  
- landing_start  

### Frontend and Backend Integration
- Django Template System  
- Clean URL routing  
- SQLite database for development  
- Admin interface for internal management  

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

## Tech Stack

### Backend
- Python  
- Django  
- SQLite

### Frontend
- HTML  
- Django Templates

### Development Tools
- GitHub Desktop  
- Visual Studio Code  
- Python virtual environments  

## Folder Structure

```
e_vehicle_share/
│
├── customers/             
├── managers/              
├── operators/             
├── e_vehicle_share/       
├── landing_start/         
│
├── manage.py              
├── .gitignore             
└── db.sqlite3
```

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/Goutham-Senthil/e_vehicle_share
cd e_vehicle_share

### 2. Create a virtual environment
python -m venv venv

### 3. Activate the environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

### 4. Install dependencies

```bash
pip install -r requirements.txt
```
### 5. Apply migrations
python manage.py migrate

### 6. Start the development server
python manage.py runserver

App will run on:
http://127.0.0.1:8000/

