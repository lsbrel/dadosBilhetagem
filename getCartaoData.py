from bs4 import BeautifulSoup
import requests
import sys

dataMap =[
    'nfabrica',
    'nserie',
    'data',
    'hora',
    'status'
]

def saveOnFile(value, data, id=0):
    if(value == 1):
        file = open(sys.argv[4], 'a')
        file.write(data)
        file.write('\n')
    else:
        file = open('cartoes_error_log.txt', 'a')
        file.write(data)
        file.write('\n')
        
    file.close()

def retrieveAllInfoFromCard(id, cookie):
    url = f'https://www.sbevcg.com.br/sbe-web/relatorio/DetalheDoUsuario.html?idUsuario={id}&tipoDetalhe=cartao&sub=true'
    data = {}
    num = 0
    response = requests.get(url, cookies=cookie, verify=False)
    if response.text == 500:
        print("Cartao Inexistente ou faltando informaçoes")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    td_tags = soup.find_all('tr', 'row_on', limit=1)

    for line in td_tags:
        # print(line.text)
        for index, campo in enumerate(line.text.split()):
            if(campo == 'Sim'):
                break
            if(dataMap[index] == 'hora'):
                continue
            if(index > 3):
                break
            # print(f'{dataMap[index]} - {campo}')
            data[dataMap[index]] = campo

    for tipo in soup.find_all('td'):
        if(tipo.text == '1'):
            num = 1
            continue
        elif num == 1:
            # print(tipo.text)
            data['categoria'] = tipo.text
            break
        
    return data


def retrieveDataCartao(id_inicial, id_final, cookie):
    # Variaveis inicializadas e sanitizadas
    id_inicial = int(id_inicial)
    id_final = int(id_final)
    cookie = {
        "JSESSIONID": cookie
    }  
    print(f'Tentativa em id: {id_inicial}')
    # Acessando o site
    while id_inicial > id_final:
        sanitazedData = {}
        url = f'https://www.sbevcg.com.br/sbe-web/relatorio/DetalheDoUsuario.html?idPessoaFisica={id_inicial}&tipoDetalhe=usuario&sub=true'
        response = requests.get(url, cookies=cookie, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Pega todas as tags img que possuam a classe clicavel tenham uma funcao de onclick
            img_tags = soup.find_all('img', 'clicavel', onclick=True)
            # Para cada uma das tags, pegar o atributo id (Ex: usuario_827263), primeiro
            # divide ele pela underline e depois dividier pela ' pq ele foi convertido para str()
            cards_id = [str(id_card.get_attribute_list("id")).split("_")[1].split("'")[0] for id_card in img_tags]
            for cartao in cards_id:
                sData = retrieveAllInfoFromCard(cartao, cookie)
                print(f"'id_pessoa': '{id_inicial}', 'ncartao':'{cartao}' , 'data_cartao': {sData}")
                # break
            break
        else:
            print(f"Falaha em id {id_inicial}")
            # saveOnFile(0, f'Error no id {id_inicial}')
            break
        id_inicial += 1



# Funcao main 
# utilizacao
# python3 getCartaoData.py id_inicial id_final cookies arquivo_de_saida.txt
if __name__ == "__main__":
    print("Script para pegar cartoes de cada id de pessoa")
    print(f"Arquivo de saida: {sys.argv[4]}")
    print("Arquivo de erros: cartoes_error_log.txt")
    print(f"comecando de id {sys.argv[1]} até {sys.argv[2]}")
    retrieveDataCartao(sys.argv[1], sys.argv[2], sys.argv[3])


# https://www.sbevcg.com.br/sbe-web/relatorio/DetalheDoUsuario.html?idUsuario={id_cartao}&tipoDetalhe=cartao&sub=true