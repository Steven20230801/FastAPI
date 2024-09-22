# FastAPI
Learn Python API from Python API Development - Comprehensive Course for Beginners


```bash
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

## start fastapi

```bash
uvicorn main:app --reload --port 3000

```

## create postgres db
```
docker build -t my-postgres .
docker run -d -p 5432:5432 --name my-postgres-container my-postgres
```