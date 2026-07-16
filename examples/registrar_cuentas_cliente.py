from _helpers import get_credentials, create_client, print_result


client = create_client()
request, response = client.registrar_cuentas_cliente_post(
    **get_credentials(),
    cuentas=[
        {
            "identificador_cliente": "CLI001",
            "tipo_operacion": 1,
            "cuit": 20123456781,
            "cbu": "3220002204000040970011",
        }
    ],
)

print_result(request, response)
