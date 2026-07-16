from _helpers import get_credentials, create_client, print_result

client = create_client()
request, response = client.obtener_cuentas_cliente_post(
    **get_credentials(),
    datos_cliente=[
        {
            "identificador_cliente": "CLI001",
            "medio": "op_pago_recurrente_medio_debito_directo",
        }
    ],
)

print_result(request, response)
