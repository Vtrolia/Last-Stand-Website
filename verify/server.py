import socket as s, random as r
import crypt as c


CA_DIR = ""
key = "H1le0q013i1131839le"


def main():
    socket = s.socket()
    socket.bind(("127.0.0.1", 9001))
    socket.listen()

    while True:
        cloud_num = 1234
        salt = r.randint(0, 65535)
        salt = str(salt)
        passphrase_hash = c.crypt(key, salt)
        reciever, muda = socket.accept()
        data = reciever.recv(4096).decode()
        reciever.send("1".encode())
        cloud = False
        if c.crypt(data, salt) == passphrase_hash:
            cloud = True
        else:
            cloud = False

        csr = reciever.recv(5000)
        file = ""
        if cloud:
            file = CA_DIR + "cloud_req/"
        else:
            file = CA_DIR + "verify_req/"

        with open(file + "request" + str(cloud_num) + ".csr", "wb") as f:
            f.write(csr)
        cloud_num += 1

        cert = open("cacert.pem").read()
        reciever.send(cert.encode())
        reciever.close()


main()
