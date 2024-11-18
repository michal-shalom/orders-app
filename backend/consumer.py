from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import redis
import json

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Connect to Cassandra
cassandra_cluster = Cluster(['localhost'])
cassandra_session = cassandra_cluster.connect()
cassandra_session.set_keyspace('orders')

# Kafka Consumer
consumer = KafkaConsumer('orders', bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for message in consumer:
    order_data = message.value
    order_id = order_data['order_id']
    
    # Update Redis
    redis_client.set(f'order_{order_id}', 'processed')
    
    # Store in Cassandra
    cassandra_session.execute("""
        INSERT INTO order_status (order_id, status)
        VALUES (%s, %s)
    """, (order_id, 'processed'))
    
    print(f'Order {order_id} processed and status updated to "processed"')
