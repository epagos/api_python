import os

from dotenv import load_dotenv

from src import EpagosClient
from src.types import FiltroObtenerPagos

load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))

datos_pago: FiltroObtenerPagos = {
    "CodigoUnicoTransaccion": 6173896,
}

request, response = client.obtener_pagos_post(
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
