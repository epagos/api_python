from _helpers import get_credentials, build_demo_operation, create_client, print_result

client = create_client()
request, response = client.solicitud_pago_recurrente_suscripcion_post(
    **get_credentials(),
    datos_operacion_pago=build_demo_operation(250.0),
    suscripcion=[
        {"fecha": "2026-06-20", "monto": 250.0},
        {"fecha": "2026-07-20", "monto": 250.0},
    ],
    suscripcion_modalidad="mensual",
    descripcion="Suscripcion demo",
    convenio=31047,
    medio="op_pago_recurrente_medio_debito_directo",
    clientes=[{
        "identificador_cliente": "CLI001",
        "identificador_cuenta": "1AF06C14-3451-44AB-B423-74CFC2F41B95",
    },
    ],
)

print_result(request, response)
