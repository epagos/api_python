from _helpers import get_credentials, create_client, print_result

client = create_client()
request, response = client.obtener_resultado_debito_post(
    **get_credentials(),
    datos_debito=[6199564],
)

print_result(request, response)
