import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [orders, setOrders] = useState([]);

  // Fetch orders from Flask API
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/orders')
      .then(response => {
        setOrders(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div className="App">
      <h1>Order List</h1>
      <ul>
        {orders.map(order => (
          <li key={order.id}>
            {order.item} - Quantity: {order.quantity}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
