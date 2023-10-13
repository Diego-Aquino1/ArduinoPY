from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify

from flask_cors import CORS, cross_origin # para que no genere errores de CORS al hacer peticiones

from Backend.models.task_model import TaskModel

task_blueprint = Blueprint('task_blueprint', __name__)

model = TaskModel()

################# Actividad ################################


@task_blueprint.route('/actividad/delete_actividad', methods=['POST'])
@cross_origin()
def delete_task():
    return jsonify(model.delete_actividad(int(request.json['id_act'])))

@task_blueprint.route('/actividad/get_actividad', methods=['POST'])
@cross_origin()
def actividad():
    return jsonify(model.get_actividad(int(request.json['id_act'])))

@task_blueprint.route('/actividad/get_actividades', methods=['POST'])
@cross_origin()
def actividads():
    return jsonify(model.get_evaluate())


################# Administrador ################################

@task_blueprint.route('/administrador/add_administrador', methods=['POST'])
@cross_origin()
def create_administrador():
    content = model.add_administrador(request.json['rol']) 
    return jsonify(content)    

@task_blueprint.route('/administrador/delete_administrador', methods=['POST'])
@cross_origin()
def delete_administrador():
    return jsonify(model.delete_administrador(int(request.json['ID_Administrador'])))

@task_blueprint.route('/administrador/get_administrador', methods=['POST'])
@cross_origin()
def administrador():
    return jsonify(model.get_administrador(int(request.json['ID_Administrador'])))

@task_blueprint.route('/administrador/get_administradors', methods=['POST'])
@cross_origin()
def administradors():
    return jsonify(model.get_administradors())
