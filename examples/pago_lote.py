from _helpers import get_credentials, create_client, print_result

client = create_client()
request, response = client.pago_lote_post(
    **get_credentials(),
    pago_lote={
        "id_transaccion": 6199568,
        "forma_pago": 1,
        "fecha_pago": "2026-06-20",
        "importe": 600.5,
        "operaciones": [
            {"id_transaccion": 6199590, "importe": 100.5},
            {"id_transaccion": 6194388, "importe": 500.0},
        ],
    },
)

print_result(request, response)
