# ePagos Python SDK

SDK en Python para consumir la API SOAP de ePagos usando `suds-community`.

## Requisitos

- Python 3.10 o superior

## Configuración

El repo incluye un archivo [.env.example](https://github.com/epagos/api_python/blob/main/.env.example) con las variables necesarias:

```env
EPAGOS_PASSWORD=
EPAGOS_HASH=
EPAGOS_ID_ORGANISMO=
EPAGOS_ID_USUARIO=
DEFAULT_VERSION=2.0
```

Copiá ese archivo a `.env` y completá tus credenciales.

## URLs de sandbox y producción

El SDK ya incluye las URLs de sandbox y producción. No hace falta configurarlas por `.env`.

Sandbox:

- WSDL: `https://sandbox.epagos.net/wsdl/2.5/index.php?wsdl`
- Endpoint: `https://sandbox.epagos.net/wsdl/2.5/index.php`

Producción:

- WSDL: `https://api.epagos.com/wsdl/2.1/index.php?wsdl`
- Endpoint: `https://api.epagos.com/wsdl/2.1/index.php`

## Crear el cliente

El cliente principal es `EpagosClient` y se exporta desde `src`.

Cliente sandbox:

```python
import os

from dotenv import load_dotenv

from src import EpagosClient

load_dotenv()

client = EpagosClient.sandbox(version=os.getenv("DEFAULT_VERSION"))
```

Cliente producción:

```python
import os

from dotenv import load_dotenv

from src import EpagosClient

load_dotenv()

client = EpagosClient.production(version=os.getenv("DEFAULT_VERSION"))
```

## Métodos disponibles

Actualmente el cliente incluye estos métodos:

- `obtener_token_post`
- `obtener_pagos_post`
- `obtener_devoluciones_post`
- `solicitud_pagos_post`
- `solicitud_pagos_lote_post`
- `obtener_rendiciones_post`
- `obtener_entidades_pago_post`
- `obtener_pagos_adicionales_post`

## Ejecutar los ejemplos

Crear un entorno virtual:

```powershell
python -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias del proyecto:

```powershell
pip install -e .
```

Una vez creado el `venv`, activado el entorno e instalado el proyecto:

```powershell
python .\examples\obtener_token.py
python .\examples\obtener_pagos.py
python .\examples\obtener_pagos_codigo_operacion.py
python .\examples\obtener_pagos_numero_operacion.py
python .\examples\obtener_pagos_por_identificadores_externos.py
python .\examples\obtener_pagos_por_fecha.py
python .\examples\obtener_pagos_por_estado.py
python .\examples\obtener_devoluciones.py
python .\examples\solicitud_pago.py
python .\examples\solicitud_pago_error_parametro_faltante.py
python .\examples\solicitud_pago_lote.py
python .\examples\obtener_rendiciones.py
python .\examples\obtener_entidades_pago.py
python .\examples\obtener_pagos_adicionales.py
```

Cada example imprime:

- `REQUEST`: el payload normalizado enviado por el cliente.
- `RESPONSE`: la respuesta normalizada del servicio.

## Filtros de `obtener_pagos`

El tipo `DatosPago` del WSDL de ePagos para `obtener_pagos` expone estos filtros:

- `CodigoUnicoTransaccion`
- `ExternoId`
- `ExternoId_2`
- `ExternoId_3`
- `FechaPagoDesde`
- `FechaPagoHasta`
- `FechaAcreditacionDesde`
- `FechaAcreditacionHasta`
- `FechaNovedadAcreditacionDesde`
- `FechaNovedadAcreditacionHasta`
- `Estado`
- `CodBarras`
- `Implementador`
- `DevolverID4`
- `Pagina`

## Ejemplos por método

En la carpeta [examples](https://github.com/epagos/api_python/tree/main/examples) hay un script para cada método:

- [examples/obtener_token.py](https://github.com/epagos/api_python/tree/main/examples/obtener_token.py)
- [examples/obtener_pagos_por_estado.py](https://github.com/epagos/api_python/tree/main/examples/obtener_pagos_por_estado.py)
- [examples/obtener_pagos_por_fecha.py](https://github.com/epagos/api_python/tree/main/examples/obtener_pagos_por_fecha.py)
- [examples/obtener_pagos_por_id.py](https://github.com/epagos/api_python/tree/main/examples/obtener_pagos_por_id.py)
- [examples/obtener_pagos_por_identificadores_externos.py](https://github.com/epagos/api_python/tree/main/examples/obtener_pagos_por_identificadores_externos.py)
- [examples/obtener_devoluciones.py](https://github.com/epagos/api_python/tree/main/examples/obtener_devoluciones.py)
- [examples/solicitud_pago.py](https://github.com/epagos/api_python/tree/main/examples/solicitud_pago.py)
- [examples/solicitud_pago_error_parametro_faltante.py](https://github.com/epagos/api_python/tree/main/examples/solicitud_pago_error_parametro_faltante.py)
- [examples/solicitud_pago_lote.py](https://github.com/epagos/api_python/tree/main/examples/solicitud_pago_lote.py)
- [examples/obtener_rendiciones.py](https://github.com/epagos/api_python/tree/main/examples/obtener_rendiciones.py)
- [examples/obtener_entidades_pago.py](https://github.com/epagos/api_python/tree/main/examples/obtener_entidades_pago.py)
- [examples/obtener_pagos_adicionales.py](https://github.com/epagos/api_python/tree/main/examples/obtener_pagos_adicionales.py)

## Estructura general

- [src/client.py](https://github.com/epagos/api_python/tree/main/src/client.py): implementación del cliente.
- [src/types.py](https://github.com/epagos/api_python/tree/main/src/types.py): tipos `TypedDict` usados para los payloads.
- [examples](https://github.com/epagos/api_python/tree/main/examples): ejemplos de uso.
- [.env.example](https://github.com/epagos/api_python/tree/main/.env.example): variables de entorno base.
