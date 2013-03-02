#coding: utf-8

SERVIDOR_DNS_IP = '10.3.1.19'
SERVIDOR_DNS_PORTA = 8888
CLIENTE_IP = '10.3.1.20'
CLIENTE_PORTA = 8888

OPERACOES = {
                'subtracao' : {'nome': 'subtracao', 'funcao': 'subtracao', 'num_args' : 2}, 
                'soma' : {'nome': 'soma', 'funcao': 'soma', 'num_args' : 2}, 
                'produto' : {'nome': 'produto', 'funcao': 'produto', 'num_args' : 2}, 
                'divisao' : {'nome': 'divisao', 'funcao': 'divisao', 'num_args' : 2}, 
                'fatorial' : {'nome': 'fatorial', 'funcao': 'fatorial', 'num_args' : 1},
            }
DNS_ERRO_MSG = 'DNS_ERRO'
SERVIDOR_ERRO = 'ERRO'