import os

from dotenv import load_dotenv

from src import EpagosClient
from src.types import (
    Operacion,
    FiltroSolicitudLote,
    IdentificacionPagador,
    DetalleOperacion,
    Pagador,
    FormaPago,
)

load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))

forma_pago: FormaPago = {
    "id_fp": 34,
    "monto_fp": 100.5,
}

detalle_operacion: DetalleOperacion = {
    "id_item": 1,
    "desc_item": "Pago lote de prueba",
    "monto_item": 100.5,
    "cantidad_item": 1,
}

identificacion_pagador: IdentificacionPagador = {
    "tipo_doc_pagador": 1,
    "numero_doc_pagador": 12345678,
    "cuit_doc_pagador": 20123456789,
}

pagador: Pagador = {
    "email_pagador": "test@example.com",
    "identificacion_pagador": identificacion_pagador,
}

operacion: Operacion = {
    "id_moneda_operacion": 1,
    "monto_operacion": 100.5,
    "detalle_operacion": [detalle_operacion],
    "pagador": pagador,
}

lote_item: FiltroSolicitudLote = {
    "fp": [forma_pago],
    "operacion": operacion,
    "convenio": 31047,
}

lote: list[FiltroSolicitudLote] = [lote_item]

request, response = client.solicitud_pagos_lote_post(
    password=os.getenv("EPAGOS_PASSWORD"),
    hash=os.getenv("EPAGOS_HASH"),
    id_organismo=os.getenv("EPAGOS_ID_ORGANISMO"),
    id_usuario=os.getenv("EPAGOS_ID_USUARIO"),
    array_tipo_lote=lote,
)

print("REQUEST:")
print(request)
print("RESPONSE:")
print(response)
