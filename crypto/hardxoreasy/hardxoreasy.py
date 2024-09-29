import socket
import random
import threading 

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3001
ADDR = (HOST, PORT)
TEXTSIZE = 8

#creation of plaintext, key, and encrypted text
def genText():
    readable = False
    plainText = ""
    encText = ""
    xorBytes = [0]*TEXTSIZE
    while not(readable): #regenerates text in case DEL gets included
        for i in range(TEXTSIZE):
            xorBytes[i] = random.randint(1, 63) #keeping plaintext readable
        for i in range(TEXTSIZE):
            plainText  += chr(random.randint(64, 126))
        for i in range(TEXTSIZE):
            encText += chr(xorBytes[i]^ord(plainText[i]))
        if (len(encText) == TEXTSIZE):
            readable = True
        for i in range(TEXTSIZE):
            while True:
                if ord(encText[i]) < 64 or ord(encText[i]) == 127: #checks that text is readable, should be impossible for text to be less that 64
                    plainText = plainText[:i] + str(chr(random.randint(64, 126))) + plainText[i+1:]
                    xorBytes[i] = random.randint(1, 63)
                    encText = encText[:i] + str(chr(xorBytes[i]^ord(plainText[i]))) + encText[i+1:]
                    continue
                break
    return [encText, plainText, xorBytes]


def intro(encText: str, conn: socket.socket):
    sendstr = "Encrypted text: "
    for i in range(TEXTSIZE):
        sendstr += str(encText[i])
    sendstr += "\nThis text was encrypted with a secure algorithm and a random single pad key,"
    sendstr = sendstr + "\nif you happen to guess the text I will give you a flag.\n\n"
    conn.sendall(sendstr.encode())


def game(plainText: str, xorBytes: list[int], conn: socket.socket):
    sendstr = ""
    encRecText = ""
    print(plainText)
    for i in range(3):
        sendstr += "(" + chr(i+49) + "/3) >>> "
        conn.sendall(sendstr.encode())
        recText = str((conn.recv(128)))
        recText = recText[2:]
        recText = recText[:-3]
   #     print(f"length: {len(recText)} text: {recText[0:8]}")
        if(recText == plainText):
            sendstr = "How did you guess the text?? Well here is the flag bgctf{ctfflag}" #flag should be changed
            conn.sendall(sendstr.encode())
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            return
        else:
            encRecText = ""
            for i in range(len(recText)):
                encRecText += chr(xorBytes[i%TEXTSIZE]^ord(recText[i])) 
            sendstr = "Wrong that encrypts to " + encRecText + "\n"

    sendstr = "Wrong that encrypts to " + encRecText + "\n"
    sendstr += "You will never guess the plaintext"
    conn.sendall(sendstr.encode())
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    return


def startGame(conn: socket.socket, addr: str):
    print(f"connection from: {addr}")
    
    text = genText()     
    intro(str(text[0]), conn)
    text = text[1:] #the encrypted text isnt needed as we will almost always be encrypting users input
    game(*text, conn)
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




