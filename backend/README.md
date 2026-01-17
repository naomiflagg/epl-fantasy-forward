# EPL Fantasy Forward - Backend API

FastAPI backend for the EPL Fantasy Transfer tool.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:

```bash
cp .env.example .env
```

4. Update the `.env` file with your database credentials and secret keys.

5. Create the database:

```bash
createdb epl_fantasy
```

6. Run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info (protected)

### Squads

- `GET /api/v1/squads/` - Get current user's squad (protected)
- `POST /api/v1/squads/` - Create/update squad (protected)
- `PUT /api/v1/squads/{squad_id}` - Update specific squad (protected)

## Database Models

- **User**: User authentication and profile
- **UserSquad**: User's fantasy squad with players and budget
- **TransferSuggestion**: AI-generated transfer suggestions
