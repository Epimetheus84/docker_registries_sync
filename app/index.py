# -*- coding: utf-8 -*-
import requests
import yaml
import json
import os
import datetime

from log import log
from flask import Flask, jsonify, request, send_from_directory
from threading import Thread

from DockerRegistry import DockerRegistry
from DockerClient import DockerClient

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

api = Flask(__name__)

LOC_FILE = 'process.json'
STATUS_AVAILABLE = 'available'

data = {'status': 'available', 'logs': []}
with open(LOC_FILE, 'w') as locfile:
    json.dump(data, locfile)
    locfile.close()


def init_vars():
    global src_reg, dst_reg, docker_cli
    try:
        src_reg = DockerRegistry(cfg['src_registry']['ADDRESS'], cfg['src_registry']['USERNAME'],
                                 cfg['src_registry']['PASSWORD'])
        dst_reg = DockerRegistry(cfg['dst_registry']['ADDRESS'], cfg['dst_registry']['USERNAME'],
                                 cfg['dst_registry']['PASSWORD'])

        docker_cli = DockerClient()
        docker_cli.login(src_reg.ADDRESS, src_reg.USERNAME, src_reg.PASSWORD)
        docker_cli.login(dst_reg.ADDRESS, dst_reg.USERNAME, dst_reg.PASSWORD)
    except requests.exceptions.RequestException as e:
        print('docker registry connection error', e)


def add_to_loc(action, status='default'):
    if os.path.exists(LOC_FILE):
        with open(LOC_FILE, 'r') as locfile:
            data = json.load(locfile)
            locfile.close()

    if data['status'] == STATUS_AVAILABLE:
        data = {'status': 'blocked', 'logs': []}

    now = datetime.datetime.now()
    time = str(now.strftime("%H:%M:%S"))
    print(data)

    data['logs'].append({
        'time': time,
        'status': status,
        'value': action
    })

    with open(LOC_FILE, 'w') as locfile:
        json.dump(data, locfile)
        locfile.close()


src_reg = dst_reg = DockerRegistry()
docker_cli = DockerClient

init_vars()


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def get_resource(path):
    if not path or path == 'settings':
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
@api.route('/api/images/src', methods=['GET'])
def get_src_images():
    images = src_reg.images_list()
    return jsonify(images)


# список имеджей на проде
@api.route('/api/images/dst', methods=['GET'])
def get_dst_images():
    images = dst_reg.images_list()
    return jsonify(images)


# перенос с одного сервера на другой
@api.route('/api/move/to_<string:server>/', methods=['POST'])
def move(server):
    if is_busy():
        return 'im busy'

    req = request.get_json()
    images = req['images']

    bg_thread = Thread(target=move_images, args=(images, server))
    bg_thread.start()

    return 'OK'


def move_images(images, server='src'):
    pull_server = dst_reg.ADDRESS
    push_server = src_reg.ADDRESS
    if server == 'dst':
        pull_server = src_reg.ADDRESS
        push_server = dst_reg.ADDRESS

    for image in images:
        src_repo, src_tag = image.split(':')
        add_to_loc(image + ' will be moved from ' + pull_server + ' to ' + push_server)
        move_image(pull_server, push_server, src_repo, src_tag)
        add_to_loc(image + ' has been moved from ' + pull_server + ' to ' + push_server)

    finish_process()


def move_image(pull_server, push_server, src_repo, src_tag):
    # скачиваем с дева по соурс тегу
    pulled_image_name = docker_cli.pull_image(pull_server, src_repo, src_tag)
    add_to_loc(src_repo + ':' + src_tag +
               ' pulled from ' + pull_server)
    pulled_image = docker_cli.get_image(pulled_image_name)

    # меняем в теге урл на прод
    new_tag = src_tag
    new_repo = push_server + '/' + src_repo

    pulled_image.tag(repository=new_repo, tag=new_tag)
    add_to_loc(src_repo + ':' + src_tag +
               ' get new tag ' + new_repo + ':' + new_tag)

    # пушим на проду
    docker_cli.push_image(new_repo, new_tag)
    add_to_loc(new_repo + ':' + new_tag +
               ' pushed to ' + push_server)

    # удаляем локальный имейдж
    docker_cli.remove_image(pulled_image_name)
    add_to_loc('local image ' + src_repo + ':' + src_tag +
               ' has been removed ')

    # удаляем имейдж с новым тегом
    docker_cli.remove_image(new_repo + ':' + new_tag)
    add_to_loc('local image ' + new_repo + ':' + new_tag +
               ' has been removed ')


@api.route('/api/check_if_can_be_removed/<string:server>', methods=['POST'])
def check_if_can_be_removed(server):
    req = request.get_json()

    if 'images' not in req \
            or req['images'].__len__() < 1:
        return ''

    docker_reg = src_reg
    if server == 'dst':
        docker_reg = dst_reg

    response = {}
    for image in req['images']:
        src_repo, src_tag = image.split(':')
        duplicates = docker_reg.check_if_can_be_removed(src_repo, src_tag)
        if duplicates.__len__() < 1:
            continue

        response[image] = duplicates

    return jsonify(response)


# удаление с любого из
@api.route('/api/remove/<string:server>/', methods=['POST'])
def remove(server):
    if is_busy():
        return 'im busy'

    req = request.get_json()

    if 'images' not in req or not req['images']:
        return ''

    images = req['images']
    bg_thread = Thread(target=remove_images, args=(images, server))
    bg_thread.start()

    response = {
        'status': 'ok'
    }

    return jsonify(response)


def remove_images(images, server):
    docker_reg = src_reg
    if server == 'dst':
        docker_reg = dst_reg

    for src_image in images:
        add_to_loc(src_image + ' will be removed from ' + docker_reg.ADDRESS)
        src_repo, src_tag = src_image.split(':')
        result = docker_reg.remove_image(src_repo, src_tag)
        if not result:
            add_to_loc(src_image + ' error during removing from ' + docker_reg.ADDRESS, 'error')
        else:
            add_to_loc(src_image + ' has been removing from ' + docker_reg.ADDRESS)

    finish_process()


def filter_tags(images):
    res = list()
    for image_name, tags in images.items():
        if cfg['repositories'].__len__() > 0 \
                and cfg['repositories'][0] != '' \
                and image_name not in cfg['repositories']:
            continue
        for prefix in cfg['prefixes']:
            for tag in tags:
                if not tag.startswith(prefix):
                    continue
                res.append({
                    'name': image_name,
                    'tag': tag
                })

    return res


@api.route('/api/get_settings', methods=['GET'])
def get_settings():
    return jsonify(cfg)


@api.route('/api/save_settings', methods=['POST'])
def save_settings():
    new_cfg = request.get_json()
    global cfg

    with open("config.yml", 'w+') as cfgfile:
        yaml.safe_dump(new_cfg, cfgfile, allow_unicode=True, encoding='utf-8')

    print(log('configs changed, prev configs:'
              + json.dumps(cfg)
              + ', new configs:'
              + json.dumps(new_cfg)))

    cfg = new_cfg
    init_vars()

    return 'Ok'


def is_busy():
    if not os.path.exists(LOC_FILE):
        return False

    with open(LOC_FILE, 'r') as locfile:
        data = json.load(locfile)
        locfile.close()

    if data['status'] == STATUS_AVAILABLE:
        return False

    return True


# метод синхронизации всех докер имеджей
@api.route('/api/synchronize/', methods=['GET'])
def start_synchronize():
    if is_busy():
        return 'im busy'

    print(log('synchronization started'))
    bg_thread = Thread(target=synchronize, args=())
    bg_thread.start()

    return 'OK'


def synchronize():
    # получаем список имеджей слева
    src_images = src_reg.images_list()
    # получаем список имеджей справа
    dst_images = dst_reg.images_list()
    # вытаскиваем только нужные, основываясь на префиксах тегов
    src_images = filter_tags(src_images)
    dst_images = filter_tags(dst_images)
    # создаем список лишних на проде
    excess_images = [item for item in dst_images if item not in src_images]
    # сносим лишние
    for excess_image in excess_images:
        src_image = excess_image['name'] + ':' + excess_image['tag']
        add_to_loc(src_image + ' error during removing from ' + src_reg.ADDRESS, 'error')
        result = dst_reg.remove_image(excess_image['name'], excess_image['tag'])
        if not result:
            add_to_loc(src_image + ' error during removing from ' + src_reg.ADDRESS, 'error')
        else:
            add_to_loc(src_image + ' has been removing from ' + src_reg.ADDRESS)

    # создаем список недостающих на проде
    missing_images = [item for item in src_images if item not in dst_images]
    # переносим недостающие
    for missing_image in missing_images:
        src_image = missing_image['name'] + ':' + missing_image['tag']
        add_to_loc(src_image + ' will be moved from ' + src_reg.ADDRESS + ' to ' + dst_reg.ADDRESS)
        move_image(src_reg.ADDRESS, dst_reg.ADDRESS, missing_image['name'], missing_image['tag'])
        add_to_loc(src_image + ' has been moved from ' + src_reg.ADDRESS + ' to ' +  dst_reg.ADDRESS)

    finish_process()


@api.route('/api/are_you_busy', methods=['GET'])
def are_you_busy():
    with open(LOC_FILE, 'r') as locfile:
        data = json.load(locfile)
        locfile.close()

    return jsonify(data)


def finish_process():
    with open(LOC_FILE, 'r') as locfile:
        data = json.load(locfile)
        locfile.close()

    data['status'] = STATUS_AVAILABLE

    with open(LOC_FILE, 'w') as locfile:
        json.dump(data, locfile)
        locfile.close()


if __name__ == "__main__":
    api.run(port=8000)
