import socket
import threading

def receive_file(client, filename, filesize):
    with open(filename, "wb") as f:
        bytes_received = 0
        while bytes_received < filesize:
            chunk = client.recv(min(1024, filesize - bytes_received))
            if not chunk:
                break
            f.write(chunk)
            bytes_received += len(chunk)
    print(f"{filename} received successfully.")

def handle_client(client, address):
    try:
        while True:
            request = client.recv(1024)
            if not request:
                break
            request = request.decode("utf8")

            if request.startswith("FILE:"):
                _, filename, filesize = request.split(":")
                filesize = int(filesize)
                receive_file(client, filename, filesize)
            else:
                print(f"Message received from the client {address[0]}:{address[1]}: " + request)

            if request.lower() == "closed":
                client.send("closed".encode("utf8"))
                break

            response = "(Server) Message has been accepted"
            client.send(response.encode("utf8"))
    except Exception as e:
        print("Client handling exception:", e)
    finally:
        client.close()
        print(f"Connection to client {address[0]}:{address[1]} closed")

def run_server():
    serverIp = "127.0.0.1"
    serverPort = 9300

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((serverIp, serverPort))
        server.listen()
        print("Listening on %s:%d" % (serverIp, serverPort))

        while True:
            client, address = server.accept()
            message = "I am a Marian Server"
            client.send(message.encode("utf8"))
            thread = threading.Thread(target=handle_client, args=(client, address, ))
            thread.start()
    except Exception as e:
        print("Server handling exception:", e)
    finally:
        if 'server' in locals():
            server.close()

if __name__ == "__main__":
    run_server()
