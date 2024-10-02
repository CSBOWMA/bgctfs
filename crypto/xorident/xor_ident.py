import socket, threading
from os import urandom
from Crypto.Util.number import bytes_to_long

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (HOST, PORT)
TEXTSIZE = 16


def intro(conn: socket.socket):
    sendstr = "I am the Oracle. I will encrypt anything you send me (16 characters) with my (super) secure XOR cipher. The key is the flag!\n"
    conn.sendall(sendstr.encode())


def game(plaintext: bytes, conn: socket.socket):
    for i in range(3):
        sendstr = "(" + chr(i+ord('1')) + "/3) >>> "
        conn.sendall(sendstr.encode())
        rec_text = conn.recv(128)[:-1].decode()
        if len(rec_text) != 16:
            conn.sendall(b"Length 16 required.\n\n")
            continue
        enc_text = (bytes_to_long(bytes.fromhex(rec_text)) ^ bytes_to_long(plaintext)).to_bytes(8, 'big')
        if enc_text == plaintext:
            sendstr = b"That encrypts to: " + plaintext.hex().encode() + b". Which is the key!\n"
            sendstr += b"\nSo the flag is: bgctf{" + plaintext.hex().encode() + b"}\n"
            conn.sendall(sendstr)
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            return
        else:
            sendstr = b"Wrong that encrypts to " + enc_text.hex().encode() + b"\n"
            conn.sendall(sendstr)

    conn.sendall(b'You failed.\n')
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    return


def startGame(conn: socket.socket, addr: str):
    print(f"connection from: {addr}")
    
    intro(conn)
    game(urandom(8), conn)

    return

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    print(f"binded on addr {ADDR}")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=startGame, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()

