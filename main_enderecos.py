import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response
from flask import flash, request
from mysql.connector import Error
from contextlib import closing

basic_auth = auth

#Criando a Tabela endereco
def create_table():
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("CREATE TABLE IF NOT EXISTS cadastro.endereco(idCliente INTEGER NOT NULL, rua VARCHAR(100) NOT NULL, numero INT NOT NULL, bairro VARCHAR(60) NOT NULL, cidade VARCHAR(60) NOT NULL, estado VARCHAR(60) NOT NULL, cep VARCHAR(20) NOT NULL, PRIMARY KEY(idEndereco), FOREIGN KEY(idCliente) REFERENCES cliente(id))")

#Criando as Rotas API's para a Tabela Endereço
@app.route('/enderecos', methods = ['POST'])
@basic_auth.required
def add_enderecos():
	try:
		_json = request.get_json(force = True)
		_idCliente = _json['idCliente']
		_idEndereco = _json['idEndereco']
		_rua = _json['rua']
		_numero = _json['numero']
		_bairro = _json['bairro']
		_cidade = _json['cidade']
		_estado = _json['estado']
		_cep = _json['cep']		
		if _rua and _numero and _bairro and _cidade and _estado and _cep and _idEndereco and request.method == 'POST':			
			sqlQuery = "INSERT INTO cadastro.endereco(idCliente, rua, numero, bairro, cidade, estado, cep, idEndereco) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
			bindData = (_idCliente, _rua, _numero, _bairro, _cidade, _estado, _cep, _idEndereco)
			with closing(mysql.connect()) as conn:
				with closing(conn.cursor()) as cursor:
					conn = mysql.connect()
					cursor = conn.cursor(pymysql.cursors.DictCursor)
					cursor.execute(sqlQuery, bindData)
					conn.commit()
					response = jsonify('Employee added successfully!')
					response.status_code = 200
					return response
		else:
			return not_found()
	except Exception as e:
		print(e)

@app.route('/enderecos', methods = ['GET'])
@basic_auth.required
def enderecos():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT idCliente, rua, numero, bairro, cidade, estado, cep, idEndereco FROM cadastro.endereco")
		userRows = cursor.fetchall()
		response = jsonify(userRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/enderecos/<int:idEndereco>', methods =['GET'])
@basic_auth.required
def enderecos_clientes(idEndereco):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT idCliente, rua, numero, bairro, cidade, estado, cep, idEndereco FROM cadastro.endereco WHERE idEndereco = {}".format(idEndereco))
		userRows = cursor.fetchone()
		if not userRows:
			return Response('Endereço não encontrado', status = 404)
		response = jsonify(userRows)
		response.status_code = 200
		return response

	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/enderecos', methods=['PUT'])
@basic_auth.required
def update_enderecos():
	try:
		_json = request.get_json(force = True)
		_idCliente = _json['idCliente']
		_idEndereco = _json['idEndereco']
		_rua = _json['rua']
		_numero = _json['numero']
		_bairro = _json['bairro']
		_cidade = _json['cidade']
		_estado = _json['estado']
		_cep = _json['cep']		
		if _rua and _numero and _bairro and _cidade and _estado and _cep and _idCliente and _idEndereco and request.method == 'PUT':
			sqlQuery = "UPDATE cadastro.endereco SET rua=%s, numero=%s, bairro=%s, cidade=%s, estado=%s, cep=%s, idCliente=%s WHERE idEndereco=%s"
			bindData = (_rua, _numero, _bairro, _cidade, _estado, _cep, _idCliente, _idEndereco)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('User updated successfully!')
			response.status_code = 200
			return response
		else:
			return not_found()

	except Exception as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

@app.route('/enderecos/<int:idEndereco>', methods=['DELETE'])
@basic_auth.required
def delete_endereco(idEndereco):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM cadastro.endereco WHERE idEndereco ={}".format(idEndereco))
		conn.commit()
		response = jsonify('Employee deleted successfully!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
@basic_auth.required
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=5300)