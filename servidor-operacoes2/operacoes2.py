#!/usr/bin/python
#coding: utf-8

import multiprocessing
import settings
import pickle

from socket import *
from threading import Thread
from multiprocessing import Process, Manager
from Crypto.PublicKey import RSA
from Crypto.Util import randpool


class Operacoes2Servidor:
    def __init__(self, ip):
        self.ip = ip
        self.address = (ip, settings.SERVIDOR_OP2_PORTA)
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

    def soma(self, x, y):
        try:
            resultado = str(float(x) + float(y))
            return resultado
        except:
            return 'ERRO'

    def levenshtein(self, a, b):
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a,b = b,a
            n,m = m,n

        current = range(n+1)
        for i in range(1,m+1):
            previous, current = current, [i]+[0]*n
            for j in range(1,n+1):
                add, delete = previous[j]+1, current[j-1]+1
                change = previous[j-1]
                if a[j-1] != b[i-1]:
                    change = change + 1
                current[j] = min(add, delete, change)

        return str(current[n])

    def iniciar(self):
        while 1:
            self.conn, addr = self.server_socket.accept()
            self.clientePubKey = pickle.loads(self.conn.recv(1024))
            self.conn.send(pickle.dumps(self.RSAPubKey))

            data = self.RSAKey.decrypt(self.conn.recv(1024))
            data = data.split()
            args = '\033[0;32m e \033[1;33m'.join(data[1:])
            print '\033[1;33m{}\033[0;32m de \033[1;33m{}\033[0m'.format(data[0], args)

            if data[0] == "soma":
                Thread(target=self.enviar, args=(self.soma(data[1], data[2]), addr)).start()
            elif data[0] == "levenshtein":
                Thread(target=self.enviar, args=(self.levenshtein(data[1], data[2]), addr)).start()

op = Operacoes2Servidor(settings.SERVIDOR_OP2_IP)
op.iniciar()