## GDP Forecasting Tool
This project is a GDP Forecasting Tool that leverages a React and Vite-based frontend and a Django-powered backend. It enables users to forecast GDP values using advanced data processing and visualization tools.

## Getting Started
To get started, clone the repository from GitHub:

``` bash
git clone https://github.com/JustusWamswa/gdp_forecast.git
cd gdp-forecasting-tool
```

The project has two directories:

backend: Contains the Django backend code.

frontend: Contains the React frontend code.

## Prerequisites
Ensure the following are installed on your system:

Python (3.8 or later)
Node.js (14.x or later) and npm

## Setup
#### Backend Setup
Navigate to the backend directory:

``` bash
cd backend
```
Create a Python virtual environment:

``` bash
python -m venv venv
```
Activate the virtual environment:

On macOS/Linux:
``` bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

Install dependencies from requirements.txt:
``` bash
pip install -r requirements.txt
```
Run the backend server locally:
``` bash
python manage.py runserver
```
Alternatively, you can use the hosted backend link provided: https://gdp-forecast-backend.vercel.app/api/get_inference/

#### Frontend Setup
Navigate to the frontend directory:
``` bash
cd frontend
```
Install the necessary dependencies:
``` bash
npm install
```
Create a .env file in the frontend directory with the following content:
``` bash
VITE_API=<BACKEND_LINK>
```
Replace <BACKEND_LINK> with either the local backend URL (e.g., http://127.0.0.1:8000/api/get_inference/) or the hosted backend link.

Run the frontend development server:
``` bash
npm run dev
```
## Running the Application
Start the backend server (locally or use the hosted backend).

Run the frontend server.

Access the application via the local frontend server URL displayed in the terminal (e.g., http://localhost:5173).

Access hosted frontend at https://gdp-forecast.vercel.app/

