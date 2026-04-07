FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize the database
RUN python -c "from db.database import init_db; init_db()"

EXPOSE 8080

CMD ["adk", "web", "--port", "8080", "--host", "0.0.0.0"]
