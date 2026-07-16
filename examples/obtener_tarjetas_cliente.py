from _helpers import get_credentials, create_client, print_result


client = create_client()
request, response = client.obtener_tarjetas_cliente_post(
    **get_credentials(),
    datos_cliente=[
        {
            "identificador_cliente": "CLI001",
        }
    ],
)

print_result(request, response)
