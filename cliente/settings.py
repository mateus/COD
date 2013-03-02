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
                'levenshtein' : {'nome': 'levenshtein', 'funcao': 'levenshtein', 'num_args' : 2},
            }

MSGS_ERRO = {'servidor_dns_desconectado' : 'Servidor DNS desconectado', 
			 'sem_conexao' : 'Verifique sua conexão com a internet', 
			 'operacao_inexistente' : 'Operação inexistente',
			 'servidor_operacoes_desconectado' : 'Servidor de operações desconectado',
			 'falha_conexao_servidor_operacoes' : 'Falha na conexão com o servidor de operações',
			 'servidor_operacoes_erro' : 'Servidor de operações retornou um erro', 
			 'erro' : 'Erro',
			 }