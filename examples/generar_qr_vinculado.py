from _helpers import get_credentials, create_client, print_result

client = create_client()
request, response = client.generar_qr_vinculado_post(
    **get_credentials(),
    operaciones_qr=[
        {
            "id_transaccion": 6187616,
            "etiqueta": "Patente",
        },
        {
            "id_transaccion": 6195764,
            "etiqueta": "ABL",
        },
        {
            "id_transaccion": 6187422,
            "etiqueta": "Multa",
        }
    ],
)

print_result(request, response)
