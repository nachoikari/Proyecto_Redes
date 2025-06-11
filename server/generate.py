from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
import ipaddress
from lib.config.constants import SERVER_IP
from OpenSSL import crypto
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
    x509.NameAttribute(NameOID.COMMON_NAME, u"%s" % SERVER_IP),
])

# Crear certificado
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
    .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([
            x509.IPAddress(ipaddress.IPv4Address(SERVER_IP))
        ]),
        critical=False
    )
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

print("✅ Archivos 'key.pem' y 'cert.pem' generados exitosamente.")

# Convertir PEM a DER (.crt)
x509_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert.public_bytes(serialization.Encoding.PEM))
with open("cert.crt", "wb") as f_out:
    f_out.write(crypto.dump_certificate(crypto.FILETYPE_ASN1, x509_cert))

print("✅ Archivo 'cert.crt' generado exitosamente.")