
import socket
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import json


k3 = "abcdefghijklmnopqrstuvwxyz012345".encode()

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    k1 = get_random_bytes(16)

    
    cipher = AES.new(k3, AES.MODE_CFB)
    ct_bytes = cipher.encrypt(pad(k1, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    keyy = b64encode(k1).decode('utf-8')
    #ct = b64encode(ct_bytes).decode('utf-8')
    #result = json.dumps({'k3':k3,'iv':iv, 'ciphertext':ct})
    print('iv ' + iv)
    print('encr key ' + b64encode(ct_bytes).decode('utf-8'))
    print('key ' + keyy)

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn_a, address_a = server_socket.accept()  # accept new connection
    conn_b, address_b = server_socket.accept()  # accept new connection
    
    print("Connection from: " + str(address_a))

    
    #while not a_sent_message:
    # receive data stream. it won't accept data packet greater than 1024 bytes

    data = conn_a.recv(1).decode()
    print("Mode: " + data)

    
    
    conn_b.send(data.encode())  # send data to the client

    conn_b.send(ct_bytes)
    conn_b.send(cipher.iv)
    
    conn_a.send(ct_bytes)
    conn_a.send(cipher.iv)
    


    while True:
        data = conn_a.recv(16)
        print('recv ' + b64encode(data).decode('utf-8'))
        conn_b.send(data)
        
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
