from _helpers import get_credentials, create_client, print_result


client = create_client()
request, response = client.solicitud_pago_pinpad_post(
    **get_credentials(),
    solicitud={
        "id_transaccion": 6187422,
        "monto": 290.0,
        "terminal": "F51235A141231A",
    },
)

print_result(request, response)
