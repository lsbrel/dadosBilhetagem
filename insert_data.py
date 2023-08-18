import json
import mysql.connector
from datetime import datetime
import re
import sys

inicio = int(sys.argv[1])

# Dados para a conexão com o banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'amttli84_uso_transporte'
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Função para remover pontos e traços de RG e CPF
def remove_special_chars(text):
    return re.sub(r'[.-]', '', text)

def convert_to_mysql_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        mysql_datetime = date_obj.strftime('%Y-%m-%d')
        return mysql_datetime
    except ValueError:
        return None

def convert_to_mysql_datetime(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        mysql_datetime = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        return mysql_datetime
    except ValueError:
        return None

# Função para inserir os dados do cartão no banco de dados
def insert_card_data(card_data, user_id, cursor):
    query = """
        INSERT INTO cartao (numero_serie, numero_fabrica, habilitado_em, usuario_id, categoria_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    if 'categoria' in card_data:
        card_data['categoria'] = int(card_data['categoria']) + 1
    else:
        card_data['categoria'] = None

    if not 'nserie' in card_data:
        card_data['nserie'] = None

    if not 'nfabrica' in card_data:
        card_data['nfabrica'] = None

    if 'data' in card_data:
        card_data['data'] = convert_to_mysql_date(card_data['data'])
    else:
        card_data['data'] = None

    print(card_data)

    values = (
        card_data['nserie'], card_data['nfabrica'], card_data['data'], user_id, card_data['categoria']
    )

    cursor.execute(query, values)
    connection.commit()

# Função para inserir os dados no banco de dados
def insert_user_data(data, cursor):
    query = """
        INSERT INTO usuario (id_vcg, nome, nome_cartao, sexo, nascimento, cpf, rg, telefone, celular, email, endereco, numero, bairro, cep, status_cadastro, latitude, longitude, cadastro_vcg)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    if data['sexo'] == 1:
        data['sexo'] = 'M'
    else:
        data['sexo'] = 'F'
        
    data['data_cadastro'] = convert_to_mysql_datetime(data['data_cadastro'])
    data['nascimento'] = convert_to_mysql_date(data['nascimento'])
    data['cpf'] = remove_special_chars(data['cpf'])
    data['rg'] = remove_special_chars(data['rg'])

    print(data)

    values = (
        data['id_vcg'], data['nome'].encode("iso-8859-1"), data['nome_cartao'].encode("iso-8859-1"), data['sexo'], data['nascimento'], data['cpf'], data['rg'].encode("iso-8859-1"), data['telefone'].encode("iso-8859-1"), data['celular'].encode("iso-8859-1"), data['email'].encode("iso-8859-1"), data['endereco'].encode("iso-8859-1"), data['numero'].encode("iso-8859-1"), data['bairro'].encode("iso-8859-1"), data['cep'].encode("iso-8859-1"), data['status_cadastro'], data['latitude'], data['longitude'], data['data_cadastro']
    )

    cursor.execute(query, values)
    connection.commit()

    
# Ler o arquivo JSON linha por linha e inserir no banco de dados
file_path = './usuarios_transporte.json'
with open(file_path, 'r', encoding="ISO-8859-1") as json_file:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    for _ in range(inicio - 1):
        next(json_file)

    for line in json_file:
        data = json.loads(line)
        insert_user_data(data, cursor)

        user_id = cursor.lastrowid
        for card_data in data['cartoes']:
            insert_card_data(card_data, user_id, cursor)

    cursor.close()
    connection.close()
    
print("Inserção de dados concluída.")