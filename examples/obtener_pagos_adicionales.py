import os

from dotenv import load_dotenv

from src import EpagosClient
from src.types import FiltroPagosAdicionales

load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))

datos_pagos_adicionales: FiltroPagosAdicionales = {
    "Fecha_desde": "2026-01-01",
    "Fecha_hasta": "2026-01-31"
}

request, response = client.obtener_pagos_adicionales_post(
    password=os.getenv("EPAGOS_PASSWORD"),
    hash=os.getenv("EPAGOS_HASH"),
    id_organismo=os.getenv("EPAGOS_ID_ORGANISMO"),
    id_usuario=os.getenv("EPAGOS_ID_USUARIO"),
    datos_pagos_adicionales=datos_pagos_adicionales,
)

print("REQUEST:")
print(request)
print("RESPONSE:")
print(response)
