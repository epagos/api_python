from _helpers import get_credentials, create_client, print_result

client = create_client()
request, response = client.obtener_contracargos_post(
    **get_credentials(),
    contracargos={
        "Numero": "CC-6195010",
    },
)

print_result(request, response)
