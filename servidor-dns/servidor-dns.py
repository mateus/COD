#!/usr/bin/python
#coding: utf-8

import settings
import hashlib

from socket import *
from datetime import datetime
from Crypto.Cipher import AES


class ServidorDNS():
    def __init__(self, ip):
        self.ip = ip
        self.address = (ip, settings.SERVIDOR_DNS_PORTA)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(self.address)
        self.md5 = hashlib.md5('Linux').hexdigest()
        self.aes = AES.new(self.md5, AES.MODE_ECB)

    def envia(self, resultado, endereco):
        if len(resultado) % 16 != 0:
            resultado += ' ' * (16 - len(resultado) % 16)
        resultado = self.aes.encrypt(resultado)
        self.server_socket.sendto(resultado, endereco)

    def hora_atual(self):
        today = datetime.now()

        day = today.day
        if day < 10:
            day = '0{}'.format(day)
        month = today.month
        if month < 10:
            month = '0{}'.format(month)
        year = today.year
        hour = today.hour
        if hour < 10:
            hour = '0{}'.format(hour)
        minute = today.minute
        if minute < 10:
            minute = '0{}'.format(minute)
        second = today.second
        if second < 10:
            second = '0{}'.format(second)
        return '{}/{}/{} {}:{}:{}'.format(day, month, year, hour, minute, second)

    def carrega_tamanhos(self):
        tamanhos = {}
        for operacao in settings.OPERACOES:
            tamanhos[operacao] = { 'atual': -1, 'total_ips': len(settings.OPERACOES[operacao])}
        return tamanhos

    def iniciar(self):
        tamanhos = self.carrega_tamanhos()
        print '\033[1;34m === Servidor de Nomes iniciado === \033[0m \n'
        try:
            while 1:
                recv_data, addr = self.server_socket.recvfrom(1024)
                recv_data = self.aes.decrypt(recv_data).strip()
                print '[{0}] - \033[0;32mRecebendo requisição da operação \033[1;33m{1}\033[0;32m pelo IP \033[1;33m{2} \033[0m'.format(self.hora_atual(), recv_data, addr[0])
                if recv_data in settings.OPERACOES:
                    tamanhos[recv_data]['atual'] = (tamanhos[recv_data]['atual'] + 1) % tamanhos[recv_data]['total_ips']
                    resposta = settings.OPERACOES[recv_data][tamanhos[recv_data]['atual']]
                else:
                    resposta = 'DNS_ERRO'
                self.envia(resposta, addr)
                print '[{0}] - \033[0;32mResposta: \033[1;33m{1} \033[0m\n'.format(self.hora_atual(), resposta)
                with open('dns.log', 'a') as f:
                    f.write('[{0}] - Recebendo requisição da operação "{1}" pelo IP {2}\n'.format(self.hora_atual(), recv_data, addr[0]))
                    f.write('[{0}] - Resposta: {1}\n\n'.format(self.hora_atual(), resposta))
        except KeyboardInterrupt:
            print '\n\033[1;34m === Servidor de Nomes finalizado === \033[0m \n'
            exit()

dns = ServidorDNS(settings.SERVIDOR_DNS_IP)
dns.iniciar()
