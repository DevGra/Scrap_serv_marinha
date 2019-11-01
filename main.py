from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import requests
import json
import urllib
import csv

base_url = 'http://www.portaltransparencia.gov.br/servidores/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=detalhar%2Ctipo%2Ccpf%2Cnome%2CorgaoServidorExercicio%2CorgaoServidorLotacao%2Cmatricula%2CtipoVinculo%2Cfuncao&orgaosServidorExercicio=OR70000&tipo=2&ordenarPor=nome&direcao=asc'

pg = requests.get(base_url)
#import pdb; pdb.set_trace()

# -------------------- montagem do link do ajax ---------------
def ajax_principal(offset_size):
    # -- para a paginacao o offset varia de acordo com a qtde de itens por pg
    # -- comeca em 0 e se a qtde de itens exibidos for de 50 por pg, o offset
    # -- vai de 50 em 50 ate a ultima pg, por isso foi criado o iterator.
    codigo = '*'
    offset = str(offset_size)
    base_ajax = 'http://www.portaltransparencia.gov.br/servidores/consulta/resultado?'
    paginacao_simples_ajax = 'paginacaoSimples=true&'
    tamanho_pg_ajax = 'tamanhoPagina=50&'
    offset_ajax = 'offset='+offset+'&'
    direcaoOrdenacao_ajax = 'direcaoOrdenacao=asc&'
    colunaOrdenacao_ajax = 'colunaOrdenacao=nome&'
    colunas_sel = 'colunasSelecionadas=detalhar%2Ctipo%2Ccpf%2Cnome%2CorgaoServidorExercicio%2CorgaoServidorLotacao%2Cmatricula%2CtipoVinculo%2Cfuncao%2CorgaoSuperiorServidorLotacao%2CorgaoSuperiorServidorExercicio%2CunidadeOrganizacionalServidorLotacao%2CunidadeOrganizacionalServidorExercicio%2Ccargo%2Catividade%2Clicenca&'
    orgaos_ajax = 'orgaosServidorExercicio=OR70000&'
    tipo_ajax = 'tipo=2&'
    codigo_ajax = '_=' + '*'

    ajax_full_url = base_ajax + paginacao_simples_ajax + tamanho_pg_ajax + offset_ajax + direcaoOrdenacao_ajax + \
        colunaOrdenacao_ajax + colunas_sel + orgaos_ajax + tipo_ajax + codigo_ajax

    ajax_url = ajax_full_url

    data_ajax = {'paginacaoSimples':'true','tamanhoPagina':'50', 'offset': offset,'direcaoOrdenacao':'asc', \
        'colunaOrdenacao':'nome', 'colunasSelecionadas': 'detalhar,tipo,cpf,nome,orgaoServidorExercicio,orgaoServidorLotacao,matricula,tipoVinculo,funcao,orgaoSuperiorServidorLotacao,orgaoSuperiorServidorExercicio,unidadeOrganizacionalServidorLotacao,unidadeOrganizacionalServidorExercicio,cargo,atividade,licenca', \
                'orgaosServidorExercicio': 'OR70000', 'tipo': '2', '_': codigo
    }

    customHead = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Cookie": "_ga=GA1.3.92766818.1572461530; _gid=GA1.3.369187979.1572461530; JSESSIONID=wdnweolwqz2M18JBFkPl_8K9r3CATwpC3nuxa7a3.idc-jboss2-ap3-p",
            "Host": "www.portaltransparencia.gov.br",
            "Referer": "http://www.portaltransparencia.gov.br/servidores/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=detalhar%2Ctipo%2Ccpf%2Cnome%2CorgaoServidorExercicio%2CorgaoServidorLotacao%2Cmatricula%2CtipoVinculo%2Cfuncao&orgaosServidorExercicio=OR70000&tipo=2&ordenarPor=nome&direcao=asc",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
    #import pdb; pdb.set_trace()
    ajax_response = requests.get(ajax_url, headers=customHead, data=data_ajax)
    #import pdb; pdb.set_trace()
    dict_convenio = json.loads(ajax_response.content)
    #import pdb; pdb.set_trace()
    return dict_convenio
    # --------------------   fim da funcao ajax principal -----------

# teste = ajax_principal(offset)
# dados = teste['data']
# import pdb; pdb.set_trace()
# print("Fim")
# exit()

i = 1
offset_size = 0
l = 1 # somente para controle de quantidades de pagina
#import pdb; pdb.set_trace()
while True:
    nome_arquivo = 'testeservidores.csv'
    ajax_pg_main = ajax_principal(offset_size)
    #import pdb; pdb.set_trace()
    if ajax_pg_main['data']:
        data = ajax_pg_main['data']
        colunas = dict(data[0])
        nm_columns = ''
        #import pdb; pdb.set_trace()
        # try:
        with open(nome_arquivo, mode = 'a', encoding = 'utf-8') as f:
            if  i == 1:
                # pega o nome das colunas em data
                nm_columns = colunas.keys()
                nm_columns = list(nm_columns)
                import pdb; pdb.set_trace()
                writer = csv.DictWriter(f, fieldnames=nm_columns) # lineterminator = '\n'
                writer.writeheader()
                print("FIM DA GRAVACAO DO CABEÇALHO DE SERVIDORES")

            for registro in data:

                print(l)
                print(registro)
                # --------- VALORES DETALHADOS DE CADA CONVENIO ---------
                valores = registro.values()
                valor = list(valores)
                #import pdb; pdb.set_trace()
                with open(nome_arquivo, 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(valor)
                    #csvfile.close()
                #valores.update({'ValorTotal': valor_total, 'Valor_2018': valores })
                #writer.writerow(valor)
                print("FIM DA GRAVACAO DA LINHA DE CONVENIO")
                l += 1
    # verifica se a primera pagina exibe 50 itens, se sim, continua o loop.
    if len(ajax_pg_main['data']) == 50:
        i += 1
        # pq eh 50 por pagina
        offset_size += 50
        continue
    else:
        break
print("FIM DA GRAVACAO DO REGISTRO!")
