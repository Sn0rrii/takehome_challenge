# Restaurant Opening Time Takehome Challenge

This repo completes the challenge outlined in the [challenge/ directory](challenge/README.md).

# Setup:

The database migrations are setup to be used by dbmate, to install dbmate on linux:
```
sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
sudo chmod +x /usr/local/bin/dbmate
```

Or on Osx using homebrew:

```
brew install dbmate
```


# Running the service:
Create a python3 venv, and install requirements:
```
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```


Spin up the database:
```
docker-compose up postgres
```

Run migrations:
```
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/restaurants?sslmode=disable dbmate up
```

Seed the database:
```
python parse_csv.py   
```

Run the service:
```
uvicorn app.main:app --reload
```

Make a request:
```
curl -X GET 'http://localhost:8000/2023-04-01T09:30:43'
```


```
Run tests:
```
pytest test/test.py
```
