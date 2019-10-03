import socket
import banco_dou as db
from sqlalchemy.sql.expression import func

query = (
    db.session
    .query(db.Bruto)
    .filter(~db.Bruto.entidades.any())
    .order_by(func.random())
    .limit(100)
    )

HOST = '0.0.0.0'  # The server's hostname or IP address
PORT = 65000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    client, addr = s.accept()
    for q in query.all():
        client.send(q.conteudo.encode('ascii'))
        data = client.recv(100)
        if not data:
            break
        data_dec = data.decode('utf8')
        print('Received: ' + data_dec)

        client.send(b'Server echoes: ' + data + b'\n')
