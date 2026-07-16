from _helpers import get_credentials, create_client, print_result


client = create_client()
request, response = client.obtener_cajas_qr_post(
    **get_credentials(),
)

print_result(request, response)
