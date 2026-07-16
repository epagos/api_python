from _helpers import get_credentials, create_client, print_result


client = create_client()
request, response = client.generar_orden_qr_post(
    **get_credentials(),
    orden={
        "id_caja": 58,
        "importe": 1000,
    },
)

print_result(request, response)
