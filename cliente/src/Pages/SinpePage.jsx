import { useState } from 'react';
import { TextField, Button } from '../components';
import "./SinpePage.css";
import { BASE_URL } from "../constants";
const SinpePage = ({ usuario, volverAlMenu,setUsuarioLogueado }) => {
  const [destinatario, setDestinatario] = useState('');
  const [monto, setMonto] = useState('');
  const [detalle, setDetalle] = useState('');
  const [mensaje, setMensaje] = useState('');


  const handleEnviar = async () => {
    if (!destinatario || !monto || parseFloat(monto) <= 0 || destinatario.length !== 8) {
      setMensaje("⚠️ Verifique que todos los campos estén correctos");
      return;
    }
    try {
      const response = await fetch(`${BASE_URL}/enviar-sinpe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          num_emisor: usuario.numero,
          num_destino: destinatario,
          monto,
          detalle
        })
      });
      const data = await response.json();
      console.log("Respuesta del backend:", data);

      if (response.status === 200) {
        // Obtener datos actualizados del usuario desde el backend
        try {
          const userRes = await fetch(`${BASE_URL}/usuario/${usuario.numero}`);
          const userData = await userRes.json();
          if (userRes.status === 200) {
            setMensaje("✅ Transacción exitosa");
            setUsuarioLogueado(userData.usuario);
          } else {
            console.warn("No se pudo actualizar el saldo del usuario.");
          }
        } catch (fetchError) {
          console.error("Error al actualizar datos del usuario:", fetchError);
        }
      } else {
        setMensaje("❌ " + (data.message || "Ocurrió un error"));
      }
    } catch (error) {
      console.error(error);
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
