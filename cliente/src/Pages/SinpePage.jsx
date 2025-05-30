import { useState } from 'react';
import { TextField, Button } from '../components';
import "./SinpePage.css";
const SinpePage = ({ usuario, volverAlMenu }) => {
  const [destinatario, setDestinatario] = useState('');
  const [monto, setMonto] = useState('');
  const [detalle, setDetalle] = useState('');
  const [mensaje, setMensaje] = useState('');

  const handleEnviar = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/sinpe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origen: usuario.numero,
          destino: destinatario,
          monto,
          detalle
        })
      });
      const data = await response.json();
      setMensaje(data.status === "OK" ? "✅ Transacción exitosa" : "❌ Transacción fallida");
    } catch (error) {
      setMensaje("❌ Error de conexión con el servidor");
    }
  };

  return (
    <div className="sinpe-container">
      <TextField
        label="Destinatario"
        name="destino"
        value={destinatario}
        onChange={(e) => setDestinatario(e.target.value)}
        placeholder="Ingrese número de destino"
      />
      <TextField
        label="Monto"
        name="monto"
        type="number"
        value={monto}
        onChange={(e) => setMonto(e.target.value)}
        placeholder="Ingrese monto ₡"
      />
      <TextField
        label="Detalle"
        name="detalle"
        value={detalle}
        onChange={(e) => setDetalle(e.target.value)}
        placeholder="Motivo o comentario"
      />
      <div className="buttons-display">
        <Button buttonText="Enviar" onClick={handleEnviar} styles="btn-menu" />
        <Button buttonText="Volver al menú" onClick={volverAlMenu} styles="btn-logout" />
      </div>
      {mensaje && <p className="mensaje-sinpe">{mensaje}</p>}
    </div>
  );
};

export default SinpePage;
