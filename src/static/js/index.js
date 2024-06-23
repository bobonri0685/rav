import React from 'react';
import ReactDOM from 'react-dom/client';
import './static/styles.css'; 
import Dashboard from '../../components/Dashboard'; // Sem a extensão .tsx

const rootElement = document.getElementById('root');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <Dashboard />
    </React.StrictMode>
  );
} else {
  console.error("Elemento 'root' não encontrado.");
}
