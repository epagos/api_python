from typing import Literal, TypedDict

try:
    from typing import NotRequired
except ImportError:
    try:
        from typing_extensions import NotRequired
    except ImportError:
        class NotRequired:
            def __class_getitem__(cls, item):
                return item


EstadosOperacion = Literal[
    "A",  # Acreditada
    "O",  # Adeudada
    "V",  # Vencida
    "C",  # Cancelada por el usuario
    "R",  # Rechazada por el medio de pago
    "P",  # Pendiente
    "D",  # Devuelto
    "L",  # Acreditación por Lote
]

MedioRecurrente = Literal[
    "op_pago_recurrente_medio_tarjeta",
    "op_pago_recurrente_medio_debin",
    "op_pago_recurrente_medio_debito_directo",
    "op_pago_recurrente_medio_debito_inmediato",
]


class FiltroObtenerPagos(TypedDict):
    CodigoUnicoTransaccion: NotRequired[int]
    ExternoId: NotRequired[str]  # numero_operacion
    ExternoId_2: NotRequired[str]  # identificador_externo_2
    ExternoId_3: NotRequired[str]  # identificador_externo_3
    Estado: NotRequired[EstadosOperacion]
    CodBarras: NotRequired[str]
    Implementador: NotRequired[int]
    FechaPagoDesde: NotRequired[str]  # YYYY-MM-DD
    FechaPagoHasta: NotRequired[str]  # YYYY-MM-DD
    FechaAcreditacionDesde: NotRequired[str]  # YYYY-MM-DD HH:mm:ss
    FechaAcreditacionHasta: NotRequired[str]  # YYYY-MM-DD HH:mm:ss
    FechaNovedadAcreditacionDesde: NotRequired[str]  # YYYY-MM-DD HH:mm:ss
    FechaNovedadAcreditacionHasta: NotRequired[str]  # YYYY-MM-DD HH:mm:ss
    DevolverID4: NotRequired[bool]
    Pagina: NotRequired[int]


class FiltroPagosAdicionales(TypedDict):
    Fecha_desde: NotRequired[str]  # YYYY-MM-DD
    Fecha_hasta: NotRequired[str]  # YYYY-MM-DD


class FiltroObtenerRendiciones(TypedDict):
    numero: NotRequired[int]
    secuencia: NotRequired[int]
    Fecha_desde: NotRequired[str]  # YYYY-MM-DD
    Fecha_hasta: NotRequired[str]  # YYYY-MM-DD
    fecha_deposito_desde: NotRequired[str]  # YYYY-MM-DD
    fecha_deposito_hasta: NotRequired[str]  # YYYY-MM-DD


class FiltroObtenerContracargos(TypedDict):
    Numero: str
    Estado: str
    Fecha_desde: NotRequired[str]  # YYYY-MM-DD
    Fecha_hasta: NotRequired[str]  # YYYY-MM-DD


class OperacionLote(TypedDict):
    id_operacion: int


class DetalleOperacion(TypedDict):
    id_item: int
    desc_item: str
    monto_item: float
    cantidad_item: int


class IdentificacionPagador(TypedDict):
    tipo_doc_pagador: int
    numero_doc_pagador: int
    cuit_doc_pagador: int


class DireccionPagador(TypedDict):
    calle_dom_pagador: str
    numero_dom_pagador: str
    adicional_dom_pagador: str
    cp_dom_pagador: str
    ciudad_dom_pagador: str
    provincia_dom_pagador: int
    pais_dom_pagador: int


class TelefonoPagador(TypedDict):
    codigo_telef_pagador: int
    numero_telef_pagador: int


class Pagador(TypedDict):
    nombre_pagador: NotRequired[str]
    apellido_pagador: NotRequired[str]
    fechanac_pagador: NotRequired[str]  # YYYY-MM-DD
    email_pagador: str
    identificacion_pagador: IdentificacionPagador
    domicilio_pagador: NotRequired[DireccionPagador]
    telefono_pagador: NotRequired[TelefonoPagador]
    cbu_pagador: NotRequired[int | str]


class ExpiracionTarjeta(TypedDict):
    mes_vencimiento_tarjeta_fp: int
    anio_vencimiento_tarjeta_fp: int


class InfoTarjeta(TypedDict):
    tipo_identificacion_tarjeta_fp: int
    numero_identificacion_tarjeta_fp: int


class DireccionTarjeta(TypedDict):
    calle_direccion_tarjeta_fp: str
    numero_direccion_tarjeta_fp: str


class Tarjeta(TypedDict):
    numero_tarjeta_fp: str | int
    banco_tarjeta_fp: str
    vencimiento_tarjeta_fp: ExpiracionTarjeta
    codigo_seg_tarjeta_fp: str
    cuotas_tarjeta_fp: int
    titular_tarjeta_fp: str
    identificacion_tarjeta_fp: InfoTarjeta
    fechanac_tarjeta_fp: str  # YYYY-MM-DD
    direccion_tarjeta_fp: DireccionTarjeta


class Operacion(TypedDict):
    numero_operacion: NotRequired[str]
    identificador_externo_2: NotRequired[str]
    identificador_externo_3: NotRequired[str]
    identificador_externo_4: NotRequired[str]
    identificador_cliente: NotRequired[str]
    id_moneda_operacion: int
    monto_operacion: float
    opc_pdf: NotRequired[bool]
    opc_fecha_vencimiento: NotRequired[str]  # YYYY-MM-DD
    opc_devolver_qr: NotRequired[bool]
    opc_devolver_codbarras: NotRequired[bool]
    opc_generar_pdf: NotRequired[bool]
    opc_operaciones_lote: NotRequired[list[OperacionLote]]
    opc_fp_excluidas: NotRequired[str]
    opc_tp_excluidos: NotRequired[str]
    opc_fp_permitidas: NotRequired[str]
    detalle_operacion: list[DetalleOperacion]
    pagador: Pagador
    fecha_2do_venc: NotRequired[str]  # YYYY-MM-DD
    monto_operacion_2do_venc: NotRequired[float]
    tipo_operacion: NotRequired[int]
    codigo_publicacion: NotRequired[int]
    url_boleta: NotRequired[str | None]
    url_ok: NotRequired[str]
    url_error: NotRequired[str]
    opc_T30_cerrado: NotRequired[bool]
    opc_T30_reutilizable: NotRequired[bool]
    opc_T30_require_orden: NotRequired[bool]
    opc_T30_requiere_orden: NotRequired[bool]


class FormaPago(TypedDict):
    id_fp: int
    monto_fp: float
    tarjeta: NotRequired[Tarjeta]


class FiltroSolicitudLote(TypedDict):
    fp: list[FormaPago]
    operacion: Operacion
    convenio: int


class DatosClienteRecurrente(TypedDict):
    identificador_cliente: str
    identificador_tarjeta: str
    proximo_vencimiento: NotRequired[bool]


class DatosClienteCuentaRecurrente(TypedDict):
    identificador_cliente: str
    medio: MedioRecurrente
    identificador_cuenta: NotRequired[str]


class DatosSuscripcion(TypedDict):
    fecha: str
    monto: float


class SuscripcionCliente(TypedDict):
    identificador_cliente: str
    identificador_tarjeta: NotRequired[str]
    identificador_cuenta: NotRequired[str]


class OperacionQr(TypedDict):
    id_transaccion: int
    etiqueta: str


class OperacionPagoLoteItem(TypedDict):
    id_transaccion: int
    importe: float


class PagoLote(TypedDict):
    id_transaccion: int
    forma_pago: int
    fecha_pago: str  # YYYY-MM-DD
    importe: float
    operaciones: list[OperacionPagoLoteItem]


class CuentaClienteAgregar(TypedDict):
    identificador_cliente: str
    tipo_operacion: int
    cuit: NotRequired[int]
    cbu: str
    fecha_adhesion: str  # YYYY-MM-DD


class OrdenQr(TypedDict):
    id_caja: NotRequired[int]
    id_transaccion: NotRequired[int]
    importe: float
    concepto: NotRequired[str]
    vencimiento: NotRequired[str]  # YYYY-MM-DD
    identificador_2: NotRequired[str]
    identificador_3: NotRequired[str]
    identificador_4: NotRequired[str]
    email_pagador: NotRequired[str]
    detalle_orden: NotRequired[str]


class SolicitudPagoPinpadData(TypedDict):
    id_transaccion: int
    monto: float
    terminal: str
