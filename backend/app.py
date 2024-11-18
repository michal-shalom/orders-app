from gevent import monkey
monkey.patch_all()
from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
import redis
from flask_cors import CORS
from kafka import KafkaProducer
import json
import uuid





app = Flask(__name__)
CORS(app)

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Connect to Cassandra
cassandra_cluster = Cluster(['localhost'])
cassandra_session = cassandra_cluster.connect()
cassandra_session.execute("""
    CREATE KEYSPACE IF NOT EXISTS orders
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
""")
cassandra_session.set_keyspace('orders')
cassandra_session.execute("""
    CREATE TABLE IF NOT EXISTS order_status (
        order_id UUID PRIMARY KEY,
        status text
    );
""")

# Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/api/orders', methods=['POST'])
def create_order():
    order_id = str(uuid.uuid4())
    order_data = {'order_id': order_id, 'status': 'created'}
    producer.send('orders', order_data)  # Send order to Kafka
    redis_client.set(f'order_{order_id}', 'created')  # Cache in Redis
    return jsonify({'order_id': order_id, 'message': 'Order created successfully'}), 201

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order_status(order_id):
    status = redis_client.get(f'order_{order_id}')
    if not status:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify({'order_id': order_id, 'status': status})

if __name__ == '__main__':
    app.run(debug=True)
