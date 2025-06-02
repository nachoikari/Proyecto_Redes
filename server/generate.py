from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime

# Generar clave privada
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Datos para el certificado
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"CR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"San José"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Cartago"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Universidad Nacional"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])

# Crear certificado
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False)
    .sign(key, hashes.SHA256(), default_backend())
)

# Guardar clave privada
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# Guardar certificado
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ Archivos 'cert.pem' y 'key.pem' generados exitosamente.")
