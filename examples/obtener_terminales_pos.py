from _helpers import get_credentials, create_client, print_result


client = create_client()
request, response = client.obtener_terminales_pos_post(
    **get_credentials(),
)

print_result(request, response)
