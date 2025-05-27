import { useState } from 'react';
import './PageLogin.css'; 
import { Button, TextField } from '../components/index.js';

const PageLogin = ({setUsuarioLogueado }) =>{
    const [cedula, setCedula] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = () =>{
        console.log("Maricon");
        setUsuarioLogueado(cedula);
    };

    return(
        <div className="login-container">
            <h2>Iniciar Sesión</h2>
            <TextField
                label="Código"
                name="codigo"
                value={cedula}
                onChange={(e) => setCedula(e.target.value)}
                placeholder="Ingrese su cédula"
            />
            <TextField
                label="Contraseña"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Ingrese su contraseña"
            />
            <Button
                buttonText="Login"
                onClick={handleLogin}
                styles="btn btn-primary"
            />
        </div>
    );
}
export default PageLogin;