from sql_connection.insert_function import *
from sql_connection.initial_db import *
from sql_connection.table_creation import *
from sql_connection.consult_function import *


conn = connect_db()

def test_insert():
    data_image1 = {
        "nome": "João Silva",
        "user_email": "nskajsakj",
        "nome_arquivo": "abc12dadsas3.jpg",
        "status": "found"
    }

    data_image2 = {
        "nome": "João Silva",
        "user_email": "joao@example.com",
        "nome_arquivo": "abc1odsfsasio23.jpg",
        "status": "found"
    }

    data_match = {
        "nome": "r3tnuh",
        "email_user_lost": "joao@example.com",
        "email_user_found": "r3tnuh@example.com",
        "nome_arquivo_lost": "abc1odsfsasio23.jpg",
        "nome_arquivo_found": "xyz456.jpg"
    }
    data_user1 = {
		"nome": "João Silva",
		"email": "joao@example.com",
		"contact": "123456789",
	}
    data_user2 = {
		"nome": "R3tnuh",
		"email": "r3tnuh@example.com",
		"contact": "987654321",
	}
    insert_image(conn, data_image1)
    insert_image(conn, data_image2)
    insert_match(conn, data_match)
    insert_user(conn, data_user1)
    insert_user(conn, data_user2)


def consult_test():
	resultados = search_faces(conn, status="found")
	print(resultados)

consult_test()
close_db(conn)


