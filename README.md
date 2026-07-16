# ePagos Python SDK

SDK en Python para consumir la API SOAP de ePagos usando `suds-community`.

## Requisitos

- Python 3.10 o superior

## Configuración

El repo incluye un archivo [.env.example](.env.example) con las variables necesarias:

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

- WSDL: `https://api.epagos.com/wsdl/2.5/index.php?wsdl`
- Endpoint: `https://api.epagos.com/wsdl/2.5/index.php`

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
- `obtener_contracargos_post`
- `solicitud_pago_recurrente_post`
- `solicitud_pago_recurrente_suscripcion_post`
- `obtener_tarjetas_cliente_post`
- `obtener_cuentas_cliente_post`
- `generar_qr_vinculado_post`
- `pago_lote_post`
- `registrar_cuentas_cliente_post`
- `obtener_resultado_debito_post`
- `obtener_cajas_qr_post`
- `generar_orden_qr_post`
- `obtener_terminales_pos_post`
- `solicitud_pago_pinpad_post`

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
python .\examples\obtener_pagos_por_id.py
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
python .\examples\obtener_contracargos.py
python .\examples\solicitud_pago_recurrente.py
python .\examples\solicitud_pago_recurrente_suscripcion.py
python .\examples\obtener_tarjetas_cliente.py
python .\examples\obtener_cuentas_cliente.py
python .\examples\generar_qr_vinculado.py
python .\examples\pago_lote.py
python .\examples\registrar_cuentas_cliente.py
python .\examples\obtener_resultado_debito.py
python .\examples\obtener_cajas_qr.py
python .\examples\generar_orden_qr.py
python .\examples\obtener_terminales_pos.py
python .\examples\solicitud_pago_pinpad.py
```

Cada example imprime:

- `REQUEST`: el payload normalizado enviado por el cliente.
- `RESPONSE`: la respuesta normalizada del servicio.

## Tests

Los tests unitarios cubren la construcción de credenciales, el orden de argumentos SOAP y los payloads normalizados de los métodos agregados:

```powershell
python -m unittest discover -s tests -v
```

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

En la carpeta [examples](examples) hay un script para cada método:

- [examples/obtener_token.py](examples/obtener_token.py)
- [examples/obtener_pagos_por_id.py](examples/obtener_pagos_por_id.py)
- [examples/obtener_pagos_por_identificadores_externos.py](examples/obtener_pagos_por_identificadores_externos.py)
- [examples/obtener_pagos_por_fecha.py](examples/obtener_pagos_por_fecha.py)
- [examples/obtener_pagos_por_estado.py](examples/obtener_pagos_por_estado.py)
- [examples/obtener_devoluciones.py](examples/obtener_devoluciones.py)
- [examples/solicitud_pago.py](examples/solicitud_pago.py)
- [examples/solicitud_pago_error_parametro_faltante.py](examples/solicitud_pago_error_parametro_faltante.py)
- [examples/solicitud_pago_lote.py](examples/solicitud_pago_lote.py)
- [examples/obtener_rendiciones.py](examples/obtener_rendiciones.py)
- [examples/obtener_entidades_pago.py](examples/obtener_entidades_pago.py)
- [examples/obtener_pagos_adicionales.py](examples/obtener_pagos_adicionales.py)
- [examples/obtener_contracargos.py](examples/obtener_contracargos.py)
- [examples/solicitud_pago_recurrente.py](examples/solicitud_pago_recurrente.py)
- [examples/solicitud_pago_recurrente_suscripcion.py](examples/solicitud_pago_recurrente_suscripcion.py)
- [examples/obtener_tarjetas_cliente.py](examples/obtener_tarjetas_cliente.py)
- [examples/obtener_cuentas_cliente.py](examples/obtener_cuentas_cliente.py)
- [examples/generar_qr_vinculado.py](examples/generar_qr_vinculado.py)
- [examples/pago_lote.py](examples/pago_lote.py)
- [examples/registrar_cuentas_cliente.py](examples/registrar_cuentas_cliente.py)
- [examples/obtener_resultado_debito.py](examples/obtener_resultado_debito.py)
- [examples/obtener_cajas_qr.py](examples/obtener_cajas_qr.py)
- [examples/generar_orden_qr.py](examples/generar_orden_qr.py)
- [examples/obtener_terminales_pos.py](examples/obtener_terminales_pos.py)
- [examples/solicitud_pago_pinpad.py](examples/solicitud_pago_pinpad.py)

## Estructura general

- [src/client.py](src/client.py): implementación del cliente.
- [src/types.py](src/types.py): tipos `TypedDict` usados para los payloads.
- [tests/test_client.py](tests/test_client.py): tests unitarios del cliente.
- [examples](examples): ejemplos de uso.
- [.env.example](.env.example): variables de entorno base.
