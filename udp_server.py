import socket

def udp_server(host='127.0.0.1', port=12345):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Bind the socket to the host and port
        sock.bind((host, port))
        print(f"UDP server up and listening at {host}:{port}")

        # Keep the server running
        while True:
            # Receive message
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print(f"Received message: {data.decode()} from {addr}")

            # Optionally, you can send a response back to the client
            # response = "Message received"
            # sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    udp_server()