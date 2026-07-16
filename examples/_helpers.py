import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src import EpagosClient
from src.types import IdentificacionPagador, Operacion, Pagador


load_dotenv()


def create_client() -> EpagosClient:
    return EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))


def get_credentials() -> dict:
    return {
        "password": os.getenv("EPAGOS_PASSWORD"),
        "hash": os.getenv("EPAGOS_HASH"),
        "id_organismo": int(os.getenv("EPAGOS_ID_ORGANISMO")),
        "id_usuario": os.getenv("EPAGOS_ID_USUARIO"),
    }


def build_demo_operation(amount: float = 250.0) -> Operacion:
    identificacion_pagador: IdentificacionPagador = {
        "tipo_doc_pagador": 1,
        "numero_doc_pagador": 12345678,
        "cuit_doc_pagador": 20123456781,
    }
    pagador: Pagador = {
        "email_pagador": "test@example.com",
        "identificacion_pagador": identificacion_pagador,
    }

    return {
        "numero_operacion": "OP-DEMO-001",
        "identificador_externo_2": "LEG-998877",
        "identificador_externo_3": "SUC-01",
        "id_moneda_operacion": 1,
        "monto_operacion": amount,
        "detalle_operacion": [
            {
                "id_item": 1,
                "desc_item": "Operacion demo",
                "monto_item": amount,
                "cantidad_item": 1,
            }
        ],
        "pagador": pagador,
    }


def print_result(request: dict, response: dict) -> None:
    print("REQUEST:")
    print(request)
    print("RESPONSE:")
    print(response)
