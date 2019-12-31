import socket as s, random as r, subprocess as sub
import crypt as c
import ssl, os

CA_DIR = ""
key = "H1le0q013i1131839le"


def main():
    socket = s.socket()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("/usr/local/www/Last-Stand-Website/verify/cacert.pem", "/usr/local/www/Last-Stand-Website/verify/privkey.pem", "3sa6a423083V9h774")
    socket.bind(("10.0.0.71", 85))
    socket.listen(10)

    while True:
        try:
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
                    print("correct")
                    with open("req.tmp.csr", "wb") as f:
                        f.write(csr)
                    cwd = os.getcwd()
                    os.chdir("/usr/local/www/LScert/root/ca/intermediate")
                    os.system("openssl ca -batch -config openssl.cnf -extensions server_cert -days 90 -notext -md sha256 -in '" + cwd + "/req.tmp.csr' -out /usr/local/www/Last-Stand-Website/verify/client_cert.pem -passin pass:1LF26r213992c6e594")
                    os.chdir(cwd)
                else:
                    reciever.send("not available")
                    reciever.close()
                    continue
                    
                cloud_num += 1
                cert_f = open("client_cert.pem")
                cert = cert_f.read()
                print(cert)
                reciever.send(cert.encode())
                reciever.close()
                os.remove("client_cert.pem")
                os.remove("req.tmp.csr")
        except:
            continue

main()
