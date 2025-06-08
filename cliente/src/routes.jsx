import { Routes, Route } from 'react-router-dom';
import PageLogin from './Pages/PageLogin';
import MenuPage from './Pages/MenuPage';
import SinpePage from "./Pages/SinpePage";
import HistorialPage from "./Pages/HistorialPage";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
function Main() {
  const [usuarioLogueado, setUsuarioLogueado] = useState(null);
  const navigate = useNavigate();
  const volverAlMenu = () => {
    navigate('/menu');
  };
  
  return (
    <Routes>
      <Route path="/" element={<PageLogin setUsuarioLogueado={setUsuarioLogueado} />} />
      <Route path="/menu" element={<MenuPage usuario={usuarioLogueado} setUserLogueado={setUsuarioLogueado} />} />
      <Route path="/sinpe" element={<SinpePage usuario={usuarioLogueado} volverAlMenu={volverAlMenu} setUsuarioLogueado={setUsuarioLogueado}></SinpePage>}/>
      <Route path="/historial" element={<HistorialPage />}/>
    </Routes>
  );
}

export default Main;
