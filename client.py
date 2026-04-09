import socket
import os

def send_file(filename, clientSocket):
    filesize = os.path.getsize(filename)
    clientSocket.send(f"FILE:{filename}:{filesize}".encode("utf-8"))
    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(1024)
            if not bytes_read:
                break
            clientSocket.sendall(bytes_read)
    print(f"{filename} sent.")

def run_client():
    serverIp = "127.0.0.1"
    serverPort = 9300

    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((serverIp, serverPort))

        while True:
            response = clientSocket.recv(1024)
            if not response:
                break
            response = response.decode("utf-8")

            if response.lower() == "closed":
                print("Client disconnected")
                break

            print("Received: " + response)
            message = input("Enter message: ")

            if message.lower() == "file1":
                send_file("file1.txt", clientSocket)
            elif message.lower() == "file2":
                send_file("file2.txt", clientSocket)
            else:
                clientSocket.send(message.encode("utf-8"))
    except Exception as e:
        print("Client exception:", e)
    finally:
        clientSocket.close()

if __name__ == "__main__":
    run_client()
