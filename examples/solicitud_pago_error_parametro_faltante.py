import os
from pprint import pprint

from dotenv import load_dotenv

from src import EpagosClient


load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))

datos_operacion_pago = {
    "numero_operacion": "OP-ERROR-REQ-0001",
    "identificador_externo_2": "LEG-ERROR-02",
    "identificador_externo_3": "SUC-01",
    "identificador_externo_4": "CANAL-WEB",
    "id_moneda_operacion": 1,
    "opc_fecha_vencimiento": "2026-05-20",
    "detalle_operacion": [
        {
            "id_item": 1,
            "desc_item": "Abono mensual",
            "monto_item": 30.0,
            "cantidad_item": 2,
        }
    ],
    "pagador": {
        "email_pagador": "test@example.com",
        "identificacion_pagador": {
            "tipo_doc_pagador": 1,
            "numero_doc_pagador": 31252804,
            "cuit_doc_pagador": 20312528046,
        },
    },
}

formas_pago = [
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
pprint(request, sort_dicts=False)
print("RESPONSE:")
pprint(response, sort_dicts=False)
