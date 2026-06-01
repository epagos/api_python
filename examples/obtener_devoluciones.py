import os

from dotenv import load_dotenv

from src import EpagosClient
from src.types import FiltroObtenerPagos

load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))
datos_pago: FiltroObtenerPagos = {'FechaPagoDesde': '2026-01-01', 'FechaPagoHasta': '2026-01-31'}

request, response = client.obtener_devoluciones_post(
    password=os.getenv("EPAGOS_PASSWORD"),
    hash=os.getenv("EPAGOS_HASH"),
    id_organismo=os.getenv("EPAGOS_ID_ORGANISMO"),
    id_usuario=os.getenv("EPAGOS_ID_USUARIO"),
    datos_pago=datos_pago,
)

print("REQUEST:")
print(request)
print("RESPONSE:")
print(response)
