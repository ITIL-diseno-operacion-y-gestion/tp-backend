import requests
import random
from faker import Faker

fake = Faker()

url = "https://itil-api.onrender.com/incidentes/tickets"

for x in range(1):
    ticket = {
        "id": 0,
        "id_usuario": random.randint(1, 3),
        "forma_de_notificacion": random.choice(
            ["email", "telefono", "presencial", "carta"]
        ),
        "reportador": fake.name(),
        "usuarios_afectados": fake.name(),
        "servicios_afectados": fake.sentence(),
        "prioridad": random.choice(["alta", "media", "baja"]),
        "categoria": "Alguna",
        "informacion_adicional": fake.text(),
        "fecha_de_alta": "string",
    }
    print(ticket)
    x = requests.post(url, json=ticket)
    print(x.status_code)
    print(x.text)
