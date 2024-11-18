Flask Kafka Cassandra Redis Project
===================================

A distributed system for processing and tracking orders, built to demonstrate practical use of Flask, Kafka, Cassandra, and Redis. This project provides a REST API for creating and managing orders and demonstrates how to integrate modern distributed technologies.

Features
--------
- Flask API:
  - Create orders via POST /api/orders
  - Fetch order statuses via GET /api/orders/<order_id>
- Kafka:
  - Decouples order creation from processing using a Kafka topic.
- Cassandra:
  - Stores persistent order statuses.
- Redis:
  - Caches order statuses for fast, real-time access.
- Docker:
  - Simplifies setup and deployment using Docker and docker-compose.

Project Architecture
--------------------
1. Flask:
   - Acts as the API backend.
   - Sends orders to Kafka for further processing.
   - Retrieves order statuses from Redis or Cassandra.
2. Kafka:
   - A message broker to handle real-time streaming of orders.
   - Producers (Flask) send messages; Consumers process them.
3. Cassandra:
   - Stores processed orders for persistence.
4. Redis:
   - Caches order statuses for quick lookups.
5. Docker:
   - Manages all services (Kafka, Zookeeper, Cassandra, Redis) via docker-compose.

Prerequisites
-------------
Before running this project, ensure you have the following installed:
- Docker Desktop
- Python 3.8+ (Python 3.11 recommended for compatibility)
- pip (Python package installer)
- Postman or curl for testing the API

Setup Instructions
------------------
1. Clone the Repository:
   git clone https://github.com/your-username/flask-kafka-app.git
   cd flask-kafka-app

2. Start Services with Docker:
   docker-compose up -d

3. Set Up the Virtual Environment:
   - Create and activate a Python virtual environment:
     python -m venv venv
     venv\Scripts\activate  (For Windows)
   - Install dependencies:
     pip install -r requirements.txt

4. Initialize Cassandra Database:
   - Access the Cassandra shell:
     docker exec -it <cassandra-container-name> cqlsh
   - Create the keyspace and table:
     CREATE KEYSPACE IF NOT EXISTS orders
     WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

     USE orders;

     CREATE TABLE IF NOT EXISTS order_status (
         order_id UUID PRIMARY KEY,
         status text
     );

5. Start Flask Application:
   python app.py

6. Start Kafka Consumer:
   In another terminal, start the Kafka consumer:
   python consumer.py

Usage
-----
1. Create an Order:
   Send a POST request to create a new order:
     curl -X POST http://127.0.0.1:5000/api/orders

   Response:
     {
         "order_id": "some-unique-id",
         "message": "Order created successfully"
     }

2. Fetch Order Status:
   Send a GET request to retrieve the status of an order:
     curl http://127.0.0.1:5000/api/orders/<order_id>

   Response:
     {
         "order_id": "some-unique-id",
         "status": "created"
     }

Testing with Postman
--------------------
1. Use Postman to send requests to:
   - POST /api/orders to create orders.
   - GET /api/orders/<order_id> to check their status.
2. Set up a Postman Collection Runner to simulate multiple requests.

Project Structure
-----------------
flask-kafka-app/
├── backend/
│   ├── app.py           (Flask API)
│   ├── consumer.py      (Kafka consumer)
│   ├── requirements.txt (Python dependencies)
│   ├── venv/            (Virtual environment - not included in Git)
│   └── __pycache__/     (Compiled Python files - ignored)
├── docker-compose.yml    (Docker configuration)
├── README.txt            (Project documentation)

Future Enhancements
-------------------
- Add more Kafka topics for different data types (e.g., invoices).
- Introduce user authentication for API endpoints.
- Add a React or Vue.js frontend for real-time order tracking.
- Deploy the system to the cloud using Kubernetes or AWS.
