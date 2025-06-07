import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { LoginPage } from './indexPages'
import Main from "./routes";
function App() {
  const [usuarioLogueado, setUsuarioLogueado] = useState(null);

  return (
    <>
      <Main></Main>
    </>
  )
}

export default App
