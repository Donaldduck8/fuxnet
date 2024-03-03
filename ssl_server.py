import socket
import ssl

def create_ssl_server(address):
    # Create a socket and wrap it in SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    ssl_sock = context.wrap_socket(sock, server_side=True)
    ssl_sock.bind(address)
    ssl_sock.listen(5)
    return ssl_sock

def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data}")
            response = b'Echo: ' + data
            conn.sendall(response)
    finally:
        conn.close()

def main():
    ssl_server = create_ssl_server(('0.0.0.0', 4444))
    print('SSL server started on port 4444...')
    while True:
        conn, addr = ssl_server.accept()
        print(f'Connected by {addr}')
        handle_client(conn)

if __name__ == '__main__':
    main()