# Backend

This is the backend for the LUCY-test project.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   alembic upgrade head
   ```

## Running the server

To run the server, use the following command:

```
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Running tests

To run the tests, use the following command:

```
pytest
```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`