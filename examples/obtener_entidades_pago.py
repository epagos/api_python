import os

from dotenv import load_dotenv
from src import EpagosClient

load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))
request, response = client.obtener_entidades_pago_post(
    password=os.getenv("EPAGOS_PASSWORD"),
    hash=os.getenv("EPAGOS_HASH"),
    id_organismo=os.getenv("EPAGOS_ID_ORGANISMO"),
    id_usuario=os.getenv("EPAGOS_ID_USUARIO"),
)

print("REQUEST:")
print(request)
print("RESPONSE:")
print(response)
