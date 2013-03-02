#!/usr/bin/python
#coding: utf-8

import multiprocessing
import settings

from socket import *
from threading import Thread
from multiprocessing import Process, Manager


class Operacoes2Servidor:
    def __init__(self, ip):
        self.ip = ip
        self.address = (ip, settings.SERVIDOR_OP2_PORTA)
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        self.MAX_PACOTE = 1024

    def enviar(self, valor, endereco):
        aux = 0
        tam = len(valor)
        #if tam > self.MAX_PACOTE:
        #   for i in xrange(tam / self.MAX_PACOTE):
        #       pacote = valor[i*self.MAX_PACOTE:(i+1)*self.MAX_PACOTE]
        #       self.server_socket.sendto(pacote, endereco)
        #else:
        #   self.server_socket.sendto(valor, endereco)
        print '\033[0;32mResultado: \033[1;33m{}\033[0m\n'.format(valor)
        self.conn.send(valor)
        self.conn.close()

    def soma(self, x, y):
        try:
            resultado = str(float(x) + float(y))
            return resultado
        except:
            return 'ERRO'

    def fatorial(self, x, y=1):
        resultado = 1
        try:
            num = int(x)
            if num < 0:
                return 'ERRO'
            lista = xrange(y, num+1)
            for n in lista:
                resultado = int(n) * resultado
            x = resultado
            return str(resultado)
        except:
            return 'ERRO'

    def xfatorial2(self, lista, x, inicio=0):
        resultado = 1
        try:
            if x < 0:
                return 'ERRO'
            l = xrange(inicio + 1, x+1)
            for num in l:
                resultado *= int(num)
            #self.n *= resultado
            #print self.n + ' ' + resultado
            #self.fatorial[0] *= resultado
            lista.append(resultado)
            #return str(resultado)
            return str(resultado)
        except:
            return 'ERRO'

    def xfatorial(self, x):
        #self.n = 0
        lista = Manager().list()
        n1 = int(x)/2
        n2 = int(x)
        p1 = Process(target=self.xfatorial2, args=(lista, n1, ))
        p2 = Process(target=self.xfatorial2, args=(lista, n2, n1))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        #print self.n
        resultado = 1
        for l in lista:
            resultado *= l
        #print resultado
        return str(resultado)

    def xfatorial_var_cpus(self, x):
        x = int(x)
        lista = Manager().list()
        numeroCPUs = multiprocessing.cpu_count()
        intervalo = x / numeroCPUs
        nums = []
        for i in xrange(numeroCPUs):
            nums.append(x - (i * intervalo))
        procs = []
        for i in xrange(len(nums)):
            if (i == 0):
                p = Process(target=self.xfatorial2, args=(lista, nums[i]))
            else:
                p = Process(target=self.xfatorial2, args=(lista, nums[i], nums[i-1]))
            procs.append(p)
            p.start()
            
        for i in procs:
            i.join()
        resultado = 1
        for l in lista:
            resultado *= l
        #print resultado
        return str(resultado)

    def iniciar(self):
        while(1):
            self.conn, addr = self.server_socket.accept()
            recv_data = self.conn.recv(1024)
            data = recv_data.split()
            args = '\033[0;32m e \033[1;33m'.join(data[1:])
            print '\033[1;33m{}\033[0;32m de \033[1;33m{}\033[0m'.format(data[0], args)

            if data[0] == "soma":
                Thread(target=self.enviar, args=(self.soma(data[1], data[2]), addr)).start()
            elif data[0] == "fatorial":
                Thread(target=self.enviar, args=(self.fatorial(data[1]), addr)).start()
            elif data[0] == "xfatorial":
                Thread(target=self.enviar, args=(self.xfatorial_var_cpus(data[1]), addr)).start()

op = Operacoes2Servidor(settings.SERVIDOR_OP2_IP)
op.iniciar()
