#!/usr/bin/env python
#coding: utf-8

import multiprocessing
import settings
import pickle

from socket import *
from threading import Thread
from multiprocessing import Process, Manager
from Crypto.PublicKey import RSA
from Crypto.Util import randpool

class Operacoes1Servidor:
    def __init__(self, ip):
        self.ip = ip
        self.address = (ip, settings.SERVIDOR_OP1_PORTA)
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        self.MAX_PACOTE = 1024
        
        blah = randpool.RandomPool()
        self.RSAKey = RSA.generate(1024, blah.get_bytes)   
        self.RSAPubKey = self.RSAKey.publickey()

    def enviar(self, valor, endereco):
        print '\033[0;32mResultado: \033[1;33m{}\033[0m\n'.format(valor)
        valor = self.clientePubKey.encrypt(str(valor), 32)[0]
        self.conn.send(valor)
        self.conn.close()

    def subtracao(self, x, y):
        try:
            return str(float(x) - float(y))
        except:
            return 'ERRO'

    def soma(self, x, y):
        try:
            return str(float(x) + float(y))
        except:
            return 'ERRO'
            
    def divisao(self, x, y):
        try:
            return str(float(x) / float(y))
        except ZeroDivisionError:
            return 'INFINITO'
        except:
            return 'ERRO'

    def produto(self, x, y):
        try:
            return str(float(x) * float(y))
        except:
            return 'ERRO'

    def iniciar(self):
        while 1:
            self.conn, addr = self.server_socket.accept()
            self.clientePubKey = pickle.loads(self.conn.recv(1024))
            self.conn.send(pickle.dumps(self.RSAPubKey))

            data = self.RSAKey.decrypt(self.conn.recv(1024))
            data = data.split()
            args = '\033[0;32m e \033[1;33m'.join(data[1:])
            print '\033[1;33m{}\033[0;32m de \033[1;33m{}\033[0m'.format(data[0], args)

            if data[0] == 'soma':
                Thread(target=self.enviar, args=(self.soma(data[1], data[2]), addr)).start()
            elif data[0] == 'subtracao':
                Thread(target=self.enviar, args=(self.subtracao(data[1], data[2]), addr)).start()
            elif data[0] == 'produto':
                Thread(target=self.enviar, args=(self.produto(data[1], data[2]), addr)).start()
            elif data[0] == 'divisao':
                Thread(target=self.enviar, args=(self.divisao(data[1], data[2]), addr)).start()

op = Operacoes1Servidor(settings.SERVIDOR_OP1_IP)
op.iniciar()
