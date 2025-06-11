@echo off
cd /d "%~dp0"
setlocal

REM Ruta al certificado
set CERT_PATH=cert.crt

REM Verificar si el archivo existe
if not exist "%CERT_PATH%" (
    echo ❌ No se encontró el archivo %CERT_PATH%
    pause
    exit /b 1
)

echo 🔐 Importando %CERT_PATH% como entidad de certificación raíz...

REM Ejecutar certutil (requiere permisos de administrador)
certutil -addstore -f "Root" "%CERT_PATH%"

if %errorlevel%==0 (
    echo ✅ Certificado importado exitosamente en el almacén "Root"
) else (
    echo ❌ Ocurrió un error al importar el certificado
)

pause
