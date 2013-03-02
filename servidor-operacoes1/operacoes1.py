#!/usr/bin/env python
#coding: utf-8

import multiprocessing
import settings

from socket import *
from threading import Thread
from multiprocessing import Process, Manager

class Operacoes1Servidor:
	def __init__(self, ip):
		self.ip = ip
		self.address = (ip, settings.SERVIDOR_OP1_PORTA)
		self.server_socket = socket(AF_INET, SOCK_STREAM)
		self.server_socket.bind(self.address)
		self.server_socket.listen(5)
		self.MAX_PACOTE = 1024

	def enviar(self, valor, endereco):
		aux = 0
		tam = len(valor)
		#if tam > self.MAX_PACOTE:
		#	for i in xrange(tam / self.MAX_PACOTE):
		#		pacote = valor[i*self.MAX_PACOTE:(i+1)*self.MAX_PACOTE]
		#		self.server_socket.sendto(pacote, endereco)
		#else:
		#	self.server_socket.sendto(valor, endereco)
		print '\033[0;32mResultado: \033[1;33m{}\033[0m\n'.format(valor)
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
		while(1):
			self.conn, addr = self.server_socket.accept()
			recv_data = self.conn.recv(1024)
			data = recv_data.split()
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
