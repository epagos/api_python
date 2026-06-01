import os

from dotenv import load_dotenv

from src import EpagosClient
from src.types import FiltroObtenerRendiciones


load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))

datos_rendicion: FiltroObtenerRendiciones = {
    "Fecha_desde": "2026-01-01",
    "Fecha_hasta": "2026-01-31",
}

request, response = client.obtener_rendiciones_post(
    password=os.getenv("EPAGOS_PASSWORD"),
    hash=os.getenv("EPAGOS_HASH"),
    id_organismo=int(os.getenv("EPAGOS_ID_ORGANISMO")),
    id_usuario=os.getenv("EPAGOS_ID_USUARIO"),
    datos_rendicion=datos_rendicion,
)

print("REQUEST:")
print(request)
print("RESPONSE:")
print(response)
