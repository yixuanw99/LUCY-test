# LUCY-test Project

This project consists of a Vue.js frontend and a FastAPI backend for epigenetic age report generation and analysis.

## Project Structure

```
LUCY-test/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   └── r_support/
│   │   ├── resources/
│   │   │   ├── adjust_models/
│   │   │   └── model_probes/
│   │   └── main.py
│   ├── data/
│   │   ├── biolearn_output/
│   │   ├── processed_beta_table/
│   │   └── raw/
│   ├── logs/
│   ├── scripts_manual/
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── mockdata/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── router/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   ├── tests/
│   │   └── unit/
│   └── package.json
├── docs/
│   ├── css/
│   ├── img/
│   ├── js/
│   └── mockdata/
├── workflows/
└── docker-compose.yml
```

## Features

### Backend
- Epigenetic age report generation
- IDAT file processing using ChAMP R package
- Cell proportion analysis using EpiDISH
- Saliva-to-blood conversion for methylation data
- BioLearn model integration for age prediction
- Google Cloud Storage integration for data storage
- Database operations using SQLAlchemy and Alembic
- R script integration for specialized bioinformatics processing

### Frontend
- Aging speed visualization
- Disease risks assessment charts

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