#!/usr/bin/python
#coding: utf-8

import socket
import sys
import threading
import functools
import settings
import hashlib
from Crypto.Cipher import AES
import pickle
from Crypto.PublicKey import RSA
from Crypto.Util import randpool


def Decorator_funcoes():
    class _Decorator_funcoes(object):
        def __init__(self, fn):
            self.fn = fn

        def __get__(self, obj, type=None):
            return functools.partial(self, obj)

        def __call__(self, *args, **kwargs):
            #threading.Thread(target=self.fn, args=args).start()
            return self.fn(*args)

    return _Decorator_funcoes

def Decorator_requisita():
    class _Decorator_requisita(object):
        def __init__(self, fn):
            self.fn = fn

        def __get__(self, obj, type=None):
            return functools.partial(self, obj)

        def __call__(self, *args, **kwargs):
            objeto_operacao = args[0]
            tipo = args[1]
            print '\033[0;32mPerguntando quem tem a operação: \033[1;33m{}\033[0m'.format(tipo)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            endereco = (settings.SERVIDOR_DNS_IP, settings.SERVIDOR_DNS_PORTA)
            try:
                msg = objeto_operacao.criptografa_mensagem_dns(tipo)
                s.sendto(msg, endereco)
                resposta, endereco = s.recvfrom(objeto_operacao.MAX_PACOTE)
                resposta = objeto_operacao.decriptografa_mensagem_dns(resposta).strip()
            except socket.timeout:
                msg_erro = 'dns_desconectado'
                print '\033[1;31m{}\033[0m'.format(msg_erro)
                return msg_erro
            except socket.error:
                msg_erro = 'sem_conexao'
                print '\033[1;31mFalha na conexão com o Servidor DNS\033[0m'
                return msg_erro
            if resposta == settings.MSGS_ERRO['erro']:
                print '\033[0;32mOperação \033[1;33m{} \033[0;32minexistente\033[0m'.format(tipo)
                return 'operacao_inexistente'
            else:
                ip_servidor_operacoes = resposta
                print '\033[1;33m{} \033[0;32mtem a operação \033[1;33m{}\033[0m'.format(ip_servidor_operacoes, tipo)
                resultado = self.fn(objeto_operacao, tipo, args[2], ip_servidor_operacoes)
                if resultado == settings.MSGS_ERRO['erro']:
                    print '\033[1;31mServidor de Operações retornou erro\033[0m'
                    return 'servidor_operacoes_erro'
                return resultado

    return _Decorator_requisita


class Operacoes(object): 
    def __init__(self, servidor_dns_ip):
        self.servidor_dns_ip = servidor_dns_ip
        self.porta = settings.CLIENTE_PORTA
        self.MAX_PACOTE = 1024
        self.md5 = hashlib.md5('Linux').hexdigest()
        self.aes = AES.new(self.md5, AES.MODE_ECB)
        blah = randpool.RandomPool()
        self.rsa_privatekey = RSA.generate(1024, blah.get_bytes)
        self.rsa_publickey = self.rsa_privatekey.publickey()


    @Decorator_funcoes()
    def subtracao(self, x, y):
        tipo = settings.OPERACOES['subtracao']['nome']
        resultado = self.requisita(tipo, (x, y))
        return resultado

    @Decorator_funcoes()
    def soma(self, x, y):
        tipo = settings.OPERACOES['soma']['nome']
        resultado = self.requisita(tipo, (x, y))
        return resultado

    @Decorator_funcoes()
    def produto(self, x, y):
        tipo = settings.OPERACOES['produto']['nome']
        resultado = self.requisita(tipo, (x, y))
        return resultado

    @Decorator_funcoes()
    def divisao(self, x, y):
        tipo = settings.OPERACOES['divisao']['nome']
        resultado = self.requisita(tipo, (x, y))
        return resultado

    @Decorator_funcoes()
    def levenshtein(self, x, y):
        tipo = settings.OPERACOES['levenshtein']['nome']
        resultado = self.requisita(tipo, (x, y))
        return resultado

    def gera_mensagem_16(self, msg):
        return msg + ' ' * (16 - len(msg) % 16)

    def criptografa_mensagem_dns(self, msg):
        msg = self.gera_mensagem_16(msg)
        msg = self.aes.encrypt(msg)
        return msg

    def decriptografa_mensagem_dns(self, msg):
        msg = self.aes.decrypt(msg)
        return msg

    @Decorator_requisita()
    def requisita(self, mensagem, args, servidor_ip=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        endereco = (servidor_ip, self.porta)
        try:
            s.connect(endereco)
        except socket.timeout:
            print '\033[1;31mFalha na conexão com o Servidor de Operações \033[1;33m{}'.format(servidor_ip)
            return 'falha_conexao_servidor_operacoes'
        except socket.error:
            print '\033[1;31mFalha na conexão com o Servidor de Operações \033[1;33m{}'.format(servidor_ip)
            return 'falha_conexao_servidor_operacoes'
        if(len(args) == 1):
          mensagem = "{} {}".format(mensagem, *args)
        elif(len(args) == 2):
          mensagem = "{} {} {}".format(mensagem, *args)
        print '\033[0;32mRequisitando \033[1;33m{} \033[0;32mpara \033[1;33m{} \033[0m'.format(mensagem, endereco[0])
        try:
            s.send(pickle.dumps(self.rsa_publickey))
            publickey_servidor_string = s.recv(self.MAX_PACOTE)
            publickey_servidor = pickle.loads(publickey_servidor_string)
            msg_criptografada = publickey_servidor.encrypt(mensagem, 32)[0]

            s.send(msg_criptografada)
            dados_criptografados = s.recv(self.MAX_PACOTE)
            dados = self.rsa_privatekey.decrypt(dados_criptografados)
        except socket.timeout:
            print '\033[1;31mFalha na conexão com o Servidor de Operações \033[1;33m{}'.format(servidor_ip)
            return 'falha_conexao_servidor_operacoes'
        except socket.error:
            print '\033[1;31mFalha na conexão com o Servidor de Operações \033[1;33m{}'.format(servidor_ip)
            return 'falha_conexao_servidor_operacoes'

        #dados = ''
        #dado, endereco = s.recvfrom(self.MAX_PACOTE)
        #while dado != 'FIM':
        #  dados += dado
        #  dado, _ = s.recvfrom(self.MAX_PACOTE)
        return dados


if __name__=='__main__':
    print '\033[0;34m === Cliente iniciado ===\033[0m'
    print ''
    operacoes = Operacoes(settings.CLIENTE_IP)
    print '\033[0;32mOperações Disponíveis:\033[0m'
    for operacao in settings.OPERACOES.keys():
        print '\033[1;33m{}\033[0m'.format(settings.OPERACOES[operacao]['nome'])
    print ''

    try:
        while True:
            operacao = raw_input('\033[0;32mOperação: \033[0m')
            if operacao in settings.OPERACOES:
                dados_operacao = settings.OPERACOES[operacao]
                valores = []
                for i in xrange(dados_operacao['num_args']):
                    valores.append(raw_input('\033[0;32m{}º argumento: \033[0m'.format(i+1)))
                resultado = operacoes.__getattribute__(dados_operacao['funcao'])(*valores)
                if resultado not in settings.MSGS_ERRO:
                    if len(valores) == 1:
                        print '\033[0;32m{} de \033[1;33m{} \033[0;32mé \033[1;33m{}\033[0m'.format(dados_operacao['nome'], valores[0], resultado)
                    else:
                        valores = '\033[0;32m e \033[1;33m'.join(valores)
                        print '\033[0;32m{} de \033[1;33m{} \033[0;32mé \033[1;33m{}\033[0m'.format(dados_operacao['nome'], valores, resultado)
                else:
                    pass
            else:
                print '\033[0;32mOperação \033[1;33m{} \033[0;32minexistente\033[0m'.format(operacao)
            print ''
    except KeyboardInterrupt:
        print '\n\033[0;34m === Cliente finalizado ===\033[0m'
        exit()
    