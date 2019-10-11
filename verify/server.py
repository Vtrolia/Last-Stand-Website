import socket as s, random as r
import crypt as c
import ssl

CA_DIR = ""
key = "H1le0q013i1131839le"


def main():
    socket = s.socket()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("cacert.pem", "privkey.pem", "3sa6a423083V9h774")
    socket.bind(("127.0.0.1", 9001))
    socket.listen(10)

    while True:
        cloud_num = 1234
        salt = r.randint(0, 65535)
        salt = str(salt)
        passphrase_hash = c.crypt(key, salt)
        sock, muda = socket.accept()

        with ctx.wrap_socket(sock, server_side=True) as reciever:
            data = reciever.recv(4096).decode()
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
