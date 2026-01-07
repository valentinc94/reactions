# Foundever: 

---

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.9 or higher**
- **Virtualenv** (recommended)
- **PostgreSQL**

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Install Dependencies

Install the necessary dependencies:


```bash
cd foundever
docker-compose build
```

- **Local Development**:
  ```bash
    docker-compose build
  ```

### 3. Configure Environment Variables

Create a `.env` file in the root directory and set the required environment variables. Example:

```env
POSTGRES_PASSWORD=verysecret
POSTGRES_USER=foundever
POSTGRES_DB=foundever_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg2://foundever:verysecret@postgres:5432/foundever_db
```

### Running the Project

To start the FastAPI server locally, use the following command: 

```bash
docker-compose up
```

# Note: On the first run (or after migration changes), the app may fail to connect if PostgreSQL is still initializing. Just restart the containers:

```bash
docker-compose down && docker-compose up
```

This will launch the development server, and you can access the API documentation at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### Running Unit Tests

To ensure that the application is working as expected, you can run the unit tests using the following command:

```bash
docker-compose run web python
```

### Open shell

```bash
python3
```

To ensure that you can interact with the database, import the database session:

```bash
# Import the database session from the core module
from foundever.core import database

# Create a new database session
db = database.SessionLocal() 
```