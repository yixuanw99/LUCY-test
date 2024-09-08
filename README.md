# LUCY-test Project

This project consists of a Vue.js frontend and a FastAPI backend.

## Project Structure

```
LUCY-test/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   ├── tests/
│   └── package.json
├── docs/
└── docker-compose.yml
```

## Setup and Running

### Using Docker

1. Make sure you have Docker and Docker Compose installed.
2. Run the following command in the root directory:

   ```
   docker-compose up --build
   ```

3. The frontend will be available at `http://localhost:8080` and the backend at `http://localhost:8000`.

### Manual Setup

Please refer to the README files in the `frontend` and `backend` directories for manual setup instructions.

## Documentation

Project documentation can be found in the `docs` directory.