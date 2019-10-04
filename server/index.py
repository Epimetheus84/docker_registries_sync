from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from server.DevRegistry import DevRegistry
from server.DockerClient import DockerClient
from server.ProdRegistry import ProdRegistry

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

dev_reg = DevRegistry()
prod_reg = ProdRegistry()
docker_cli = DockerClient()
docker_cli.login(DevRegistry.ADDRESS, DevRegistry.USERNAME, DevRegistry.PASSWORD)
docker_cli.login(ProdRegistry.ADDRESS, ProdRegistry.USERNAME, ProdRegistry.PASSWORD)

# http сервис должен уметь:
# список имеджей на деве
@api.route('/images/dev', methods=['GET'])
def get_dev_images():
    images = dev_reg.images_list()
    return jsonify(images)

# список имеджей на проде
@api.route('/images/prod', methods=['GET'])
def get_prod_images():
    images = prod_reg.images_list()
    return jsonify(images)

# перенос с дева на прод
@api.route('/move/to_prod/', methods=['POST'])
def move_to_prod(src_tag, dest_tag):

    # return jsonify(companies)
    pass

# и наоборот
@api.route('/move/to_dev/', methods=['POST'])
def move_to_dev(src_tag, dest_tag):
    # return jsonify(companies)
    pass

# удаление с любого из
@api.route('/remove/<string:server>', methods=['DELETE'])
def remove(server):
    # return jsonify(companies)
    pass

# url, в котором по крону синхронизируются все имеджи
api.run(port=8080)

# image_id = dev_reg.get_image_id(image)
# print(image_id)
#
# pulled_image = docker_cli.pull_image(dev_reg.ADDRESS, image['name'], image['tag'])
#
# ubuntu = docker_cli.get_image('localhost:5000/my-ubuntu:latest')
# docker_cli.remove_image(pulled_image)
#
# dev_reg.remove_image(image)
