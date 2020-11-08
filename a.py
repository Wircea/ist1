
import socket
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
import json

k3 = "abcdefghijklmnopqrstuvwxyz012345".encode()


def parseJSON(file):
    # Open the existing JSON file for loading into a variable
    with open(file) as f:
        data = json.load(f)
    return data


def byte_xor(byte_array1, byte_array2): 
    result = bytearray()
    for byte1, byte2 in zip(byte_array1, byte_array2):
        result.append(byte1 ^ byte2)
    return bytes(result)

  

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
  
    
    message = input("Choose method: \n0) CBC\n1) OFB\n>")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        ct = client_socket.recv(32)  # receive response

        print('key ' + b64encode(ct).decode('utf-8'))

        ivv = client_socket.recv(16)

        print('iv '+ b64encode(ivv).decode('utf-8'))

        cipher = AES.new(k3, AES.MODE_CFB, ivv)
        pt = cipher.decrypt(ct)        



        print(b64encode(pt).decode('utf-8'))
        
        with open("mesaj.txt", "rb+") as f:

            block = f.read(16)
            print(block)
            
            if(message == '0'):


                currentIV = byte_xor(ivv, block)
                print(b64encode(currentIV).decode('utf-8'))

            
                while len(block) != 0:

                    #block = pad(block,16)
                    cipher = AES.new(pt, AES.MODE_CFB, ivv)
                    encr = cipher.encrypt(currentIV)

                    print('###')
                    print('     Text: ' + b64encode(block).decode('utf-8'))
                    print('   Xorred: '+ b64encode(currentIV).decode('utf-8'))

                    #print(b64encode(encr).decode('utf-8'))
                    client_socket.send(encr)
                    
                    block = f.read(16)
                    print('  Crypted: '+ b64encode(encr).decode('utf-8'))

          
                    currentIV = byte_xor(encr, block)

            else :
                currentIV = ivv

                while len(block) != 0:
                    print('###')
                    print('     Text: ' + b64encode(block).decode('utf-8'))
                    cipher = AES.new(pt, AES.MODE_CFB, ivv)
                    encr = cipher.encrypt(currentIV)
                    print('  Crypted: '+ b64encode(encr).decode('utf-8'))


                    
                    ctext = byte_xor(block, encr)
                    client_socket.send(ctext)

                    print('   Xorred: '+ b64encode(ctext).decode('utf-8'))

                     
                    currentIV = encr
                    block = f.read(16)


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
