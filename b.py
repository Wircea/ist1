import socket
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
import json
from Crypto.Cipher import AES

k3 = "abcdefghijklmnopqrstuvwxyz012345".encode()

def parseJSON(file):
    # Open the existing JSON file for loading into a variable
    with open(file) as f:
        data = json.load(f)
    return data

def byte_xor(byte_array1, byte_array2): #should change
    result = bytearray()
    for byte1, byte2 in zip(byte_array1, byte_array2):
        result.append(byte1 ^ byte2)
    return bytes(result)

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    


    data = client_socket.recv(1).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal

    ct = client_socket.recv(32)
    iv = client_socket.recv(16)

    print('key encr ' + b64encode(ct).decode('utf-8'))
    print('iv ' + b64encode(iv).decode('utf-8'))

    cipher = AES.new(k3, AES.MODE_CFB, iv)
    pt = cipher.decrypt(ct)

    print('key: ' + b64encode(pt).decode('utf-8'))

    currentIV = iv

    
    if(data == '0'):
        while True:
            with open("output.txt", "ab") as myfile:
                block = client_socket.recv(16)
                
                
                print('----')
                #print(b64encode(block).decode('utf-8'))
                ciph = AES.new(pt, AES.MODE_CFB, iv)
                encr = ciph.decrypt(block)
                print('  Cryped: ' + b64encode(block).decode('utf-8'))
                print('Decryped: ' + b64encode(encr).decode('utf-8'))
                #print(encr)
                mesaj = byte_xor(encr, currentIV)
                print(mesaj)
                myfile.write(mesaj)
                #print("Writing " + b64encode(mesaj).decode('utf-8'))
                currentIV = block
        
    else :
        while True:
            with open("output.txt", "ab") as myfile:
                block = client_socket.recv(16)

               
                
                print(b64encode(block).decode('utf-8'))
                cipher = AES.new(pt, AES.MODE_CFB, iv)
                encr = cipher.encrypt(currentIV)

                print(' Cryped: ' + b64encode(encr).decode('utf-8'))

                mesaj = byte_xor(encr, block)

                print(' Xorred: ' + b64encode(mesaj).decode('utf-8'))
                
                print(mesaj)
                myfile.write(mesaj)
                currentIV = encr
            
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
