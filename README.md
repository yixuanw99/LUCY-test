# LUCY-test Project

This project consists of a Vue.js frontend and a FastAPI backend for epigenetic age report generation.

## Project Structure

```
LUCY-test/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── data/
│   │   ├── biolearn_output/
│   │   ├── biomarker_resource/
│   │   ├── cell_proportions/
│   │   ├── processed_beta_table/
│   │   └── raw/
│   ├── logs/
│   ├── scripts/
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env files
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── router/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   ├── tests/
│   └── package.json
└── docker-compose.yml
```

## Setup and Running

### Using Docker

1. Make sure you have Docker and Docker Compose installed.
2. Create appropriate `.env` files for your environment (development, production) in the backend directory.
3. Run the following command in the root directory:

   ```
   docker-compose up --build
   ```

4. The frontend will be available at `http://localhost:8080` and the backend at `http://localhost:8000`.

### Manual Setup

#### Backend

1. Navigate to the `backend` directory.
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\Activate.ps1`
   ```
3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
4. Set up the appropriate `.env` file for your environment.
5. Run the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

#### Frontend

1. Navigate to the `frontend` directory.
2. Install the dependencies:
   ```
   npm install
   ```
3. Run the development server:
   ```
   npm run serve
   ```

## Features

- Epigenetic age report generation
- IDAT file processing
- Cell proportion analysis using EpiDISH
- Saliva-to-blood conversion for methylation data
- BioLearn model integration for age prediction

## Database

The project uses SQLAlchemy with Alembic for database migrations. To initialize the database or apply migrations:

1. Navigate to the `backend` directory.
2. Run:
   ```
   alembic upgrade head
   ```

## Testing

- Backend tests can be run using pytest in the `backend` directory.
- Frontend tests can be run using `npm test` in the `frontend` directory.

## Documentation

API documentation is automatically generated and can be accessed at `http://localhost:8000/docs` when the backend is running.

For more detailed information about specific components or services, please refer to the comments in the respective files.