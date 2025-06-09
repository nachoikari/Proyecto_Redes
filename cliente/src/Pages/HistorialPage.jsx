import { useEffect, useState } from 'react';
import { BASE_URL } from "../constants";
import { Button } from "../components"; // Asegúrate de tener este componente
import "./HistorialPage.css";

const HistorialPage = ({ usuario, volverAlMenu }) => {
  const [historial, setHistorial] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!usuario) return;

    const fetchHistorial = async () => {
      try {
        const response = await fetch(`${BASE_URL}/historial/${usuario.numero}`);
        const data = await response.json();
        console.log("Historial recibido:", data.historial);
        if (response.status === 200) {
          setHistorial(data.historial);
        } else {
          setError("No se pudo obtener el historial.");
        }
      } catch (err) {
        setError("Error de conexión con el servidor.");
      }
    };

    fetchHistorial();
  }, [usuario]);

  return (
    <div className="historial-container">
      <h2>Historial de Transacciones</h2>
      {error && <p className="error">{error}</p>}

      <table className="historial-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Detalle</th>
            <th>Monto (₡)</th>
            <th>Receptor</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {historial.map((item, index) => (
            <tr key={index} className={item.estado_transaccion.includes("RECEPCIÓN") ? "recepcion" : "envio"}>
              <td>{item.fecha_transaccion ? new Date(item.fecha_transaccion).toLocaleDateString() : "Fecha inválida"}</td>
              <td>{item.detalle}</td>
              <td>{item.monto != null ? Number(item.monto).toLocaleString() : "₡0"}</td>
              <td>{item.numero_receptor}</td>
              <td>{item.estado_transaccion}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="buttons-display">
        <Button buttonText="Volver al menú" onClick={volverAlMenu} styles="btn-logout" />
      </div>
    </div>
  );
};

export default HistorialPage;
