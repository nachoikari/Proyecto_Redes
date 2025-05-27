import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import RoutesApp from './routes'; // o Main.jsx, como lo tengas

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter> {/* 👈 Aquí es donde debe ir */}
      <RoutesApp />
    </BrowserRouter>
  </React.StrictMode>
);