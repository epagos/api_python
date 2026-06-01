from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping, Optional

from dotenv import load_dotenv
from suds.cache import NoCache
from suds.client import Client
from suds.sudsobject import Object as SudsObject

from .types import (
    Operacion,
    FiltroObtenerPagos,
    FiltroPagosAdicionales,
    FiltroObtenerRendiciones,
    FormaPago, FiltroSolicitudLote,
)

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()

DEFAULT_VERSION = "2.0"
SANDBOX_WSDL_URL = "https://sandbox.epagos.net/wsdl/2.5/index.php?wsdl"
SANDBOX_ENDPOINT_URL = "https://sandbox.epagos.net/wsdl/2.5/index.php"
PRODUCTION_WSDL_URL = "https://api.epagos.com/wsdl/2.1/index.php?wsdl"
PRODUCTION_ENDPOINT_URL = "https://api.epagos.com/wsdl/2.1/index.php"

Environment = Literal["sandbox", "production"]


@dataclass(frozen=True)
class EnvironmentConfig:
    wsdl_url: str
    endpoint_url: str


ENVIRONMENTS: dict[Environment, EnvironmentConfig] = {
    "sandbox": EnvironmentConfig(
        wsdl_url=SANDBOX_WSDL_URL,
        endpoint_url=SANDBOX_ENDPOINT_URL,
    ),
    "production": EnvironmentConfig(
        wsdl_url=PRODUCTION_WSDL_URL,
        endpoint_url=PRODUCTION_ENDPOINT_URL,
    ),
}


__all__ = ["EpagosClient"]

class EpagosClient:
    def __init__(
        self,
        environment: Environment,
        version: str = DEFAULT_VERSION,
        timeout: int = 30,
    ) -> None:
        config = ENVIRONMENTS[environment]
        self.environment = environment
        self.wsdl_url = config.wsdl_url
        self.endpoint_url = config.endpoint_url
        self.version = version
        self.timeout = timeout
        self._client: Client | None = None

    @classmethod
    def sandbox(
        cls,
        version: str = DEFAULT_VERSION,
        timeout: int = 30,
    ) -> "EpagosClient":
        return cls(environment="sandbox", version=version, timeout=timeout)

    @classmethod
    def production(
        cls,
        version: str = DEFAULT_VERSION,
        timeout: int = 30,
    ) -> "EpagosClient":
        return cls(environment="production", version=version, timeout=timeout)

    def _required_argument(self, name: str, value: Any) -> Any:
        if value is None:
            raise RuntimeError(f"Falta pasar el parametro obligatorio {name}.")
        return value

    def _get_client(self) -> Client:
        if self._client is None:
            self._client = Client(self.wsdl_url, cache=NoCache(), timeout=self.timeout)
            self._client.set_options(location=self.endpoint_url)
        return self._client

    def _create_type(self, type_name: str, values: Mapping[str, Any] | None = None) -> Any:
        client = self._get_client()
        obj = client.factory.create(type_name)
        if values:
            self._fill_suds_object(obj, values)
        return obj

    def _fill_suds_object(self, obj: Any, values: Mapping[str, Any]) -> Any:
        for key, value in values.items():
            setattr(obj, key, self._convert_value(value))
        return obj

    def _convert_value(self, value: Any) -> Any:
        if isinstance(value, Mapping):
            return deepcopy(dict(value))
        if isinstance(value, list):
            return [self._convert_value(item) for item in value]
        if isinstance(value, tuple):
            return [self._convert_value(item) for item in value]
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value

    def _build_credentials(self, token: str, id_organismo: int) -> Any:
        return self._create_type(
            "DatosCredencialesPago",
            {
                "id_organismo": id_organismo,
                "token": token,
            },
        )

    def _extract_token(self, response: Any) -> str:
        data = self._normalize(response)
        token = data.get("token") if isinstance(data, dict) else None
        if isinstance(token, str) and token.strip():
            return token.strip()
        raise RuntimeError(f"No se pudo extraer el token de obtener_token. Respuesta: {data}")

    def _normalize(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, list):
            return [self._normalize(item) for item in value]
        if isinstance(value, tuple):
            return [self._normalize(item) for item in value]
        if isinstance(value, Mapping):
            return {k: self._normalize(v) for k, v in value.items()}
        if isinstance(value, SudsObject):
            data: dict[str, Any] = {}
            for key, val in value:
                data[key] = self._normalize(val)
            return self._normalize_date_fields(data)
        if hasattr(value, "__dict__"):
            data = {
                key: self._normalize(val)
                for key, val in vars(value).items()
                if not key.startswith("__")
            }
            return self._normalize_date_fields(data)
        return value

    def _normalize_date_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        for key, value in list(data.items()):
            if isinstance(value, dict):
                data[key] = self._normalize_date_fields(value)
            elif isinstance(value, list):
                data[key] = [
                    self._normalize_date_fields(item) if isinstance(item, dict) else item
                    for item in value
                ]
            elif key == "FechaNovedad" and isinstance(value, str) and " " in value:
                data[key] = value.replace(" ", "T")
        return data

    def _typed_object_or_value(self, type_name: str, payload: Mapping[str, Any] | Any) -> Any:
        if isinstance(payload, Mapping):
            return self._create_type(type_name, payload)
        return payload

    def _typed_list(self, type_name: str, items: Iterable[Mapping[str, Any] | Any]) -> list[Any]:
        return [self._typed_object_or_value(type_name, item) for item in items]

    def obtener_token_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        credenciales = {
            "hash": hash,
            "password": password,
            "id_organismo": id_organismo,
            "id_usuario": id_usuario,
        }
        request = {
            "version": self.version,
            "credenciales": self._normalize(credenciales),
        }
        response = client.service.obtener_token(self.version, credenciales)
        return request, self._normalize(response)

    def _get_token(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
    ) -> str:
        _, token_response = self.obtener_token_post(password, hash, id_organismo, id_usuario)
        return self._extract_token(token_response)

    def obtener_pagos_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
        datos_pago: Optional[FiltroObtenerPagos] = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        datos_pago = self._required_argument("datos_pago", datos_pago)
        token = self._get_token(password, hash, id_organismo, id_usuario)
        credenciales = self._build_credentials(token, id_organismo)
        pago = self._typed_object_or_value("DatosPago", datos_pago)
        request = {
            "version": self.version,
            "credenciales": self._normalize(credenciales),
            "pago": self._normalize(pago),
        }
        response = client.service.obtener_pagos(self.version, credenciales, pago)
        return request, self._normalize(response)

    def obtener_devoluciones_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
        datos_pago: Optional[FiltroObtenerPagos] = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        datos_pago = self._required_argument("datos_pago", datos_pago)
        token = self._get_token(password, hash, id_organismo, id_usuario)
        credenciales = self._build_credentials(token, id_organismo)
        datos_pago["Estado"] = "D"
        pago = self._typed_object_or_value("DatosPago", datos_pago)
        request = {
            "version": self.version,
            "credenciales": self._normalize(credenciales),
            "pago": self._normalize(pago),
        }
        response = client.service.obtener_pagos(self.version, credenciales, pago)
        return request, self._normalize(response)

    def solicitud_pagos_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
        datos_operacion_pago: Operacion,
        formas_pago_array: Iterable[FormaPago],
        convenio: int,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        datos_operacion_pago = self._required_argument(
            "datos_operacion_pago", datos_operacion_pago
        )
        formas_pago_array = self._required_argument("formas_pago_array", formas_pago_array)
        convenio = self._required_argument("convenio", convenio)
        token = self._get_token(password, hash, id_organismo, id_usuario)
        credenciales = self._build_credentials(token, id_organismo)
        operacion = self._typed_object_or_value("DatosOperacionPago", datos_operacion_pago)
        fp = self._typed_list("DatosFormaPago", formas_pago_array)
        request = {
            "version": self.version,
            "tipo_operacion": "op_pago",
            "credenciales": self._normalize(credenciales),
            "operacion": self._normalize(operacion),
            "fp": self._normalize(fp),
            "convenio": convenio,
        }
        response = client.service.solicitud_pago(
            self.version, "op_pago", credenciales, operacion, fp, int(convenio)
        )
        return request, self._normalize(response)

    def solicitud_pagos_lote_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
        array_tipo_lote: Iterable[FiltroSolicitudLote],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        array_tipo_lote = self._required_argument("array_tipo_lote", array_tipo_lote)
        token = self._get_token(password, hash, id_organismo, id_usuario)
        credenciales = self._build_credentials(token, id_organismo)
        pago_lote = self._typed_list("TipoLote", array_tipo_lote)
        request = {
            "version": self.version,
            "tipo_operacion": "op_pago",
            "credenciales": self._normalize(credenciales),
            "pago_lote": self._normalize(pago_lote),
        }
        response = client.service.solicitud_pago_lote(
            self.version, "op_pago", credenciales, pago_lote
        )
        return request, self._normalize(response)

    def obtener_rendiciones_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
        datos_rendicion: Optional[FiltroObtenerRendiciones] = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        datos_rendicion = self._required_argument("datos_rendicion", datos_rendicion)
        token = self._get_token(password, hash, id_organismo, id_usuario)
        credenciales = self._build_credentials(token, id_organismo)
        rendicion = self._typed_object_or_value("DatosRendicion", datos_rendicion)
        request = {
            "version": self.version,
            "credenciales": self._normalize(credenciales),
            "rendicion": self._normalize(rendicion),
        }
        response = client.service.obtener_rendiciones(self.version, credenciales, rendicion)
        return request, self._normalize(response)

    def obtener_entidades_pago_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
        fp: Optional[list[int]] = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        token = self._get_token(password, hash, id_organismo, id_usuario)
        credenciales = self._build_credentials(token, id_organismo)
        fp_value = [] if fp is None else fp
        request = {
            "version": self.version,
            "credenciales": self._normalize(credenciales),
            "fp": fp_value,
        }
        response = client.service.obtener_entidades_pago(self.version, credenciales, fp_value)
        return request, self._normalize(response)

    def obtener_pagos_adicionales_post(
        self,
        password: str,
        hash: str,
        id_organismo: int,
        id_usuario: str,
        datos_pagos_adicionales: FiltroPagosAdicionales,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        client = self._get_client()
        datos_pagos_adicionales = self._required_argument(
            "datos_pagos_adicionales", datos_pagos_adicionales
        )
        token = self._get_token(password, hash, id_organismo, id_usuario)
        credenciales = self._build_credentials(token, id_organismo)
        pago_adicional = self._typed_object_or_value(
            "DatosPagosAdicionales", datos_pagos_adicionales
        )
        request = {
            "version": self.version,
            "credenciales": self._normalize(credenciales),
            "datos_pagos_adicionales": self._normalize(pago_adicional),
        }
        response = client.service.obtener_pagos_adicionales(
            self.version, credenciales, pago_adicional
        )
        return request, self._normalize(response)
