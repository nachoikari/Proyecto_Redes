import { Routes, Route } from 'react-router-dom';
import PageLogin from './Pages/PageLogin';
import MenuPage from './Pages/MenuPage';
import { useState } from 'react';

function Main() {
  const [usuarioLogueado, setUsuarioLogueado] = useState(null);

  return (
    <Routes>
      <Route path="/" element={<PageLogin setUsuarioLogueado={setUsuarioLogueado} />} />
      <Route path="/menu" element={<MenuPage usuario={usuarioLogueado} />} />
    </Routes>
  );
}

export default Main;
