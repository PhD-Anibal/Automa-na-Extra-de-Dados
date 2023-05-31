#CODIGO INICIAL PARA EXTRAIR LINKS POR ESTADO

import time
import csv
import os
import requests
import datetime
from datetime import date
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


def driversetup():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless") #esta linha é para não abrir a janela do chrome
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    return driver

def pagesource(url):
    driver = driversetup()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    driver.close()
    return soup

def extrair_links(driver):
    div_mae = driver.find_element(by=By.XPATH, value='//*[@id="root-app"]/div/div[2]/section')

    html_content = div_mae.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content,'html.parser')

    product_links = soup.find_all("a", class_="ui-search-item__group__element shops__items-group-details ui-search-link")

    links = []
    for link in product_links:
        links.append(link["href"])
    return links

def pagina_por_estado(url):
    driver = driversetup()
    driver.get(url)

    # Encontra o botão "Entendi" e clica nele para fechar o banner
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Entendi')]"))
        )
        element.click()
    except:
        pass

    #visitamos todas as páginas do link e pegamos os links e escrevemos no arquivo.
    product_links_total = []
    existe_outra_pagina=True
    while(existe_outra_pagina):
        try:
            product_links=extrair_links(driver)
            product_links_total.extend(product_links) #aqui vamos adicionando os resultados de cada pagina
            pag_next = driver.find_element(By.CSS_SELECTOR, "li[class='andes-pagination__button andes-pagination__button--next shops__pagination-button']").find_element(By.TAG_NAME, 'a')
            # Clica no botão "Próximo"
            pag_next.click()
            # Espera até que a próxima página esteja carregada
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root-app"]/div/div[2]/section'))
            )
        except:
            existe_outra_pagina=False
    driver.quit()
    return product_links_total

def pagesource(url):
    driver = driversetup()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    driver.close()
    return soup

def converte_frase_float(frase):
    frase=frase.replace('Precio anterior: ','')
    frase=frase.replace(' reales','')
    frase=frase.replace(' reale','')    
    frase=frase.replace(' con ','.')
    frase=frase.replace(' centavos','')
    frase=frase.replace(' centavo','')
    return frase


def dados_de_cada_produto(url):
    oferta=False
    driver=driversetup()

    try:
        driver.get(url)
    except WebDriverException:
        print("Erro: Não foi possível resolver o endereço.")
        url_com_erro=url
        descricao='-'
        preco_anterior=0
        preco_atual=0
        return (descricao,preco_anterior,preco_atual,url_com_erro)

    #se tudo da certo que espere 5 seg carregar a página            
    time.sleep(5)


    from selenium.webdriver.common.by import By
    try: 
        div_mae1 = driver.find_element(by=By.XPATH, value='//*[@id="breadcrumb"]/div/nav/ol/li[4]/a')
        print
        div_mae = driver.find_element(by=By.XPATH, value='//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]')

        html_content = div_mae.get_attribute('outerHTML')
        soup=BeautifulSoup(html_content,'html.parser')
        lista_titulo = soup.find('h1', class_='ui-pdp-title')
        lista_preco_anterior=soup.find_all("span",class_="andes-visually-hidden")
        preco_anterior=lista_preco_anterior[1].get_text()
        preco_anterior=float(converte_frase_float(preco_anterior))
        if lista_preco_anterior[1].get_text().find("Precio anterior: ") != -1:
            try:
                preco_atual=lista_preco_anterior[2].get_text()
                preco_atual=float(converte_frase_float(preco_atual))
            except ValueError:
                preco_atual=lista_preco_anterior[3].get_text() #no caso da janela ter mais uma coluna a direita
                preco_atual=float(converte_frase_float(preco_atual))        
        else:
            preco_atual=preco_anterior #quer dizer que não está em oferta
        lista_preco = soup.find_all("span", class_="andes-money-amount__fraction")
        driver.quit()
        descricao=lista_titulo.get_text()
        url_com_erro=None
        return (descricao,preco_anterior,preco_atual,url_com_erro)
    except:
        url_com_erro=url
        descricao='-'
        preco_anterior=0
        preco_atual=0
        return (descricao,preco_anterior,preco_atual,url_com_erro)
    
def links_de_cada_link_por_estado():
    # Carregar os dados do arquivo CSV dos estados de Brasil
    df_loaded = pd.read_csv('estados.csv', index_col='state')
    states_dic = df_loaded['abbreviation'].to_dict()

    now = datetime.datetime.now()
    print("começa o código as:" + str(now))

    with open('links_de_cada_produto.csv', 'w', newline='', encoding='utf-8') as arquivo_links_csv:
        for state in states_dic.values():
            url='https://lista.mercadolivre.com.br/beleza-cuidado-pessoal/higiene-pessoal/higiene-bucal-em-'+ state +'/colgate_NoIndex_True#'
            product_links_estado[state] = pagina_por_estado(url)
            escritor = csv.writer(arquivo_links_csv, delimiter=';')
            escritor.writerow([product_links_estado[state]])
        
    now = datetime.datetime.now()
    print("fim de obtenção de links por Estado as:" + str(now))
    return product_links_estado

#CODIGO FINAL PARA EXTRAIR DADOS DE CADA LINK
def extrair_dados_de_cada_link(product_links_estado,quantidade_elementos_lidos, continuar_pesquisa=None):    
    data_atual = date.today()
    data_formatada = data_atual.strftime('%Y_%m_%d')
    nome_csv_com_data=str(data_formatada)+'.csv'

    #para o caso de uma pesquisa nova ou pesquisa que quer eliminar os dados anteriores de outra pesquisa do mesmo dia
    # **********************************************************************************************************************
    if not os.path.exists(nome_csv_com_data) or quantidade_elementos_lidos==0:
        if continuar_pesquisa!='s': # no caso que não estou procurando endereços que não foram achados em uma anterior pesquisa
            with open('links_nao_achados.csv', 'w', newline='', encoding='utf-8') as arquivo2_csv:
                print('Um arquivo chamado links_nao_achados.csv é criado caso exista um problema de achar algum produto')
                # O arquivo não existe, então cria um novo arquivo com o cabeçalho
            with open(nome_csv_com_data, 'w', newline='', encoding='utf-8') as arquivo_csv:
                # Realize as operações com o arquivo CSV aqui
                print('Os dados serão almacenados no arquivo: ' + str(nome_csv_com_data))
                escritor = csv.writer(arquivo_csv)
                escritor.writerow(['Estado', 'Preço Anterior', 'Preço Atual', 'Descrição'])

    # abre o arquivo CSV para adicionar os dados
    with open(nome_csv_com_data, 'a', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv, delimiter=';')

        elementos=0
        for estado in product_links_estado:
            print(estado)

            for produto in product_links_estado[estado]:
                if elementos>=quantidade_elementos_lidos:
                    url=produto
                    resultado=dados_de_cada_produto(url)
                    descricao=resultado[0]
                    preco_anterior=resultado[1]
                    preco_atual=resultado[2]
                    url_com_erro=resultado[3]
                    if url_com_erro is None:
                        escritor.writerow([estado, preco_anterior, preco_atual, descricao, url])
                    elif continuar_pesquisa!='s' and continuar_pesquisa!='sim':
                        print('Não se achou:' + str(url_com_erro))
                        with open('links_nao_achados.csv', 'a', newline='', encoding='utf-8') as arquivo2_csv:
                            escritor2 = csv.writer(arquivo2_csv, delimiter=';')
                            escritor2.writerow([estado, url_com_erro])
                        time.sleep(5) #pelas duvidas de erro de internet
                else:
                    elementos=elementos+1

    now = datetime.datetime.now()
    print("fim do código as:" + str(now))
    
    
# COMEÇO DO CÓDIGO:
product_links_estado={}
product_links_perdidos={} #links que não foram encontrados
quantidade_elementos_lidos=0
continuar_pesquisa=''
# Solicitar ao usuário que digite um valor se quer continuar uma procura anterior
print('* Se já fez uma pesquisa anterior que foi interrompida e quer continuar ela do digitar a data dela,')
print('**Se quiser interromper a pesquisa não tem problema e pode continuar ela depois sempre e quando')
print('tenha superado a primeira etapa de extração dos links')
continuar_pesquisa = input('escreva o nome da base de dados: (ano_mes_dia) ')

if continuar_pesquisa!='':
    # Carregar os dados do arquivo em um DataFrame do Pandas
        nome_csv_com_data = continuar_pesquisa + '.csv'
        if os.path.exists(nome_csv_com_data):
            df = pd.read_csv(nome_csv_com_data, header=None)
            quantidade_valores = df.count(axis=0)
            quantidade_elementos_lidos = sum(quantidade_valores)    

            # Contar o número total de elementos em todas as linhas
            print('Lidos anteriormente: ' + str(quantidade_elementos_lidos) + ' elementos')
            product_links_estado=links_de_cada_link_por_estado()
            extrae_resultados=extrair_dados_de_cada_link(product_links_estado, quantidade_elementos_lidos)
        else:
            print('o arquivo não existe, fim do programa')
else:
    #salva em um arquivo a lista por se se interrompe o código e quero continuar a leitura dela
    product_links_estado=links_de_cada_link_por_estado()
    extrae_resultados=extrair_dados_de_cada_link(product_links_estado,quantidade_elementos_lidos)

continuar_pesquisa = input('Deseja tentar achar os links perdidos: (s/n) ')
if continuar_pesquisa=='s':
    with open('links_nao_achados.csv', 'r', newline='', encoding='utf-8') as arquivo3_csv:

        # Ler cada linha do arquivo
        for linha in arquivo3_csv:
            product_links_estado = {}
            # Dividir a linha em chave e valor usando o ponto e vírgula como separador
            chave, valor = linha.strip().split(';')
            if chave not in product_links_estado:
                product_links_estado[chave] = []            
            # Adicionar a chave e valor ao dicionário
            product_links_estado[chave].append(valor) 
            extrae_resultados=extrair_dados_de_cada_link(product_links_estado,0,continuar_pesquisa)            
            print('fim')
