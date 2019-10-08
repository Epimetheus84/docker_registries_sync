import yaml
from flask import Flask, jsonify, request, send_from_directory

from DockerRegistry import DockerRegistry
from DockerClient import DockerClient

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

api = Flask(__name__)

dev_reg = DockerRegistry(cfg['dev_registry']['ADDRESS'], cfg['dev_registry']['USERNAME'],
                         cfg['dev_registry']['PASSWORD'])
prod_reg = DockerRegistry(cfg['prod_registry']['ADDRESS'], cfg['prod_registry']['USERNAME'],
                          cfg['prod_registry']['PASSWORD'])

docker_cli = DockerClient()
docker_cli.login(dev_reg.ADDRESS, dev_reg.USERNAME, dev_reg.PASSWORD)
docker_cli.login(prod_reg.ADDRESS, prod_reg.USERNAME, prod_reg.PASSWORD)

CLIENT_URL = 'http://localhost:3000'


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def get_resource(path):
    if not path:
        path = 'index.html'
    return send_from_directory('client/build', path)


@api.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('client/build/static/js', path)


@api.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('client/build/static/css', path)


# http сервис должен уметь:
# список имеджей на деве
@api.route('/api/images/dev', methods=['GET'])
def get_dev_images():
    images = dev_reg.images_list()
    return jsonify(images)


# список имеджей на проде
@api.route('/api/images/prod', methods=['GET'])
def get_prod_images():
    images = prod_reg.images_list()
    return jsonify(images)


# перенос с одного сервера на другой
@api.route('/api/move/to_<string:server>/', methods=['POST'])
def move(server):
    req = request.get_json()
    images = req['images']

    pull_server = prod_reg.ADDRESS
    push_server = dev_reg.ADDRESS
    if server == 'prod':
        pull_server = dev_reg.ADDRESS
        push_server = prod_reg.ADDRESS

    for src_image in images:
        src_repo, src_tag = src_image.split(':')

        # скачиваем с дева по соурс тегу
        pulled_image_name = docker_cli.pull_image(pull_server, src_repo, src_tag)
        pulled_image = docker_cli.get_image(pulled_image_name)

        # меняем в теге урл на прод
        new_tag = src_tag
        new_repo = push_server + '/' + src_repo

        pulled_image.tag(repository=new_repo, tag=new_tag)

        # пушим на проду
        docker_cli.push_image(new_repo, new_tag)

        # удаляем локальный имейдж
        docker_cli.remove_image(pulled_image_name)

    return 'OK'


# удаление с любого из
@api.route('/api/remove/<string:server>/', methods=['POST'])
def remove(server):
    req = request.get_json()
    src_image = req['image']

    force = False
    if 'force' in req:
        force = True

    docker_reg = dev_reg
    if server == 'prod':
        docker_reg = prod_reg

    response = {
        'status': 'ok'
    }

    src_repo, src_tag = src_image.split(':')

    result = docker_reg.remove_image(src_repo, src_tag, force)
    if type(result) is list:
        response = {
            'status': 'warning',
            'duplicates': result
        }

    return jsonify(response)


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
