import { useNavigate } from 'react-router-dom';
import { Button } from '../components/index.js';
import './MenuPage.css'; // si querés darle estilo

const MenuPage = ({ usuario, setUserLogueado }) => {
    const navigate = useNavigate();

    const changeToSinpePage = () => {
        //navigate('/sinpe');
    };

    const changeToHistorialPage = () => {
        //navigate('/historial');
    };

    const handleLogout = () => {
        //navigate('/'); // podrías también hacer setUsuarioLogueado(null) si lo pasás por props
    
    };

    return (
        <div className="menu-container">
            <h2>Bienvenido, {usuario?.nombre} {usuario?.apellido}</h2>
            <p><strong>Número:</strong> {usuario?.numero}</p>
            <p><strong>Saldo disponible:</strong> ₡{usuario?.monto.toLocaleString()}</p>

            <div className="buttons-display">
                <Button
                buttonText="Realizar SINPE"
                onClick={changeToSinpePage}
                styles="btn-menu"
                />
                <Button
                buttonText="Historial"
                onClick={changeToHistorialPage}
                styles="btn-menu"
                />
                <Button
                buttonText="Cerrar sesión"
                onClick={handleLogout}
                styles="btn-logout"
                />
            </div>
        </div>
    );
};

export default MenuPage;
