# criar um banco de dados para controle de horas
# dados da tabela: projeto, data, entrada, saída, total nesse dia e projeto
# criar um relatório para saber quanto fez com aquele projeto
import datetime
import mysql.connector
import csv

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='banco_de_horas'
)

cursor = conexao.cursor()


print('-' * 100)
titulo = 'BANCO DE HORAS'
print(titulo.center(100))
print('-' * 100)

while True:
    print('[1] ADICIONAR DADOS')
    print('[2] GERAR RELATÓRIO')
    print('[3] SAIR')
    opc = int(input('Selecione uma opção: '))

    if opc == 1:
        while True:
            print('-' * 100)
            projeto = input('Em qual projeto você trabalhou? ')
            dia = input('Data (aaaa-mm-dd): ')
            entrada = int(input('Horário de entrada (relógio de 24h): '))
            saida = int(input('Horário de saída (relógio de 24h): '))
            total = saida - entrada
            try:
                comando =f'INSERT INTO horas VALUES (default, "{projeto}", "{dia}", {entrada}, {saida}, {total})'
                cursor.execute(comando)
                conexao.commit()
                print('Valores adicionados ao Banco de Horas!')
            except:
                print('Algo deu errado!')
            resp = input('Deseja continuar (S/N)? ').upper()
            if resp == 'N':
                break


    if opc == 2:
        custo = int(input('Quanto você cobra por hora de trabalho? '))
        print('-' * 100)
        c = 'SELECT projeto FROM horas group by projeto'
        cursor.execute(c)
        resultado = cursor.fetchall()
        total_projeto = len(resultado) # quantos projetos diferentes a pessoa trabalhou
        c_dois = 'SELECT sum(total) FROM horas'
        cursor.execute(c_dois)
        r = cursor.fetchall()
        total_horas = r[0][0] # total de horas que a pessoa trabalhou
        total_din = custo * r[0][0] # total feito pela pessoa
        c_tres = 'SELECT projeto, sum(total) FROM horas GROUP BY projeto'
        cursor.execute(c_tres)
        res = cursor.fetchall()
        with open("relatorio.csv", mode="w") as csvfile:
            fieldnames = ["projeto", "horas", "reais"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, len(res)):
                writer.writerow({"projeto": f"{res[i][0]}", "horas": f"{res[i][1]}","reais": f"{res[i][1]*custo}"})
        print('Relatório de cada projeto:')
        for i in range(0, len(res)):
            print(f'No projeto {res[i][0]}, você trabalhou {res[i][1]} horas e fez {res[i][1]*custo} reais.')
        print(f'Você trabalhou um total de {total_horas} horas em {total_projeto} projetos diferentes e fez um total de {total_din} reais!')
        print('-' * 100)

    if opc == 3:
        print('-' * 100)
        final = 'FINALIZANDO...'
        print(final.center(100))
        print('-' * 100)
        break
