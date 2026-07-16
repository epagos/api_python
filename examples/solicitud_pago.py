import os

from dotenv import load_dotenv

from src import EpagosClient
from src.types import (
    DetalleOperacion,
    FormaPago,
    IdentificacionPagador,
    Operacion,
    Pagador,
)


load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))

identificacion_pagador: IdentificacionPagador = {
    "tipo_doc_pagador": 1,
    "numero_doc_pagador": 31252804,
    "cuit_doc_pagador": 20312528046,
}

pagador: Pagador = {
    "email_pagador": "test@example.com",
    "identificacion_pagador": identificacion_pagador,
}

detalle_operacion_1: DetalleOperacion = {
    "id_item": 1,
    "desc_item": "Abono mensual",
    "monto_item": 30.0,
    "cantidad_item": 2,
}

detalle_operacion_2: DetalleOperacion = {
    "id_item": 2,
    "desc_item": "Cargo administrativo",
    "monto_item": 40.5,
    "cantidad_item": 1,
}

datos_operacion_pago: Operacion = {
    "numero_operacion": "OP-00012345",
    "identificador_externo_2": "LEG-998877",
    "identificador_externo_3": "SUC-01",
    "identificador_externo_4": "CANAL-WEB",
    "id_moneda_operacion": 1,
    "monto_operacion": 100.5,
    "opc_fecha_vencimiento": "2027-05-20",
    "fecha_2do_venc": "2027-05-27",
    "monto_operacion_2do_venc": 110.5,
    "detalle_operacion": [detalle_operacion_1, detalle_operacion_2],
    "pagador": pagador,
}

formas_pago: list[FormaPago] = [
    {
        "id_fp": 34,
        "monto_fp": 100.5,
    }
]

convenio = 31047

request, response = client.solicitud_pagos_post(
    password=os.getenv("EPAGOS_PASSWORD"),
    hash=os.getenv("EPAGOS_HASH"),
    id_organismo=os.getenv("EPAGOS_ID_ORGANISMO"),
    id_usuario=os.getenv("EPAGOS_ID_USUARIO"),
    datos_operacion_pago=datos_operacion_pago,
    formas_pago_array=formas_pago,
    convenio=convenio,
)

print("REQUEST:")
print(request)
print("RESPONSE:")
print(response)
