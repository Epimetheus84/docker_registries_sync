import docker
import requests
from log import log

from schema import SCHEMA


class DockerClient:
    ADDRESS = 'unix://var/run/docker.sock'

    def __init__(self):
        self.client = docker.DockerClient(base_url=self.ADDRESS)

    def login(self, address='', username='', password=''):
        address = SCHEMA + address
        print(log('Docker client log into ' + address + ' login:' + str(username) + ' password:' + str(password)))
        self.client.login(registry=address, username=username, password=password)

    def images_list(self):
        images_list = self.client.images.list()
        return images_list

    def get_image(self, image_id):
        try:
            image = self.client.images.get(image_id)
        except docker.errors.ImageNotFound as e:
            print(e, 'check image validity')
            return False

        return image

    def remove_image(self, image):
        try:
            self.client.images.remove(image)
        except requests.exceptions.ReadTimeout:
            print('Read timout error image: ' + image, 'check image validity')

        print(log('Docker client remove image ' + image))
        return True

    def pull_image(self, src, repo, tag):
        repo = src + '/' + repo

        try:
            self.client.images.pull(repository=repo, tag=tag)
        except (docker.errors.ImageNotFound, docker.errors.NotFound) as e:
            print(e, 'check image validity')

        repo_tag = repo + ':' + tag
        print(log('Docker client pull image ' + repo_tag))
        return repo_tag

    def push_image(self, repo, tag):
        self.client.images.push(repository=repo, tag=tag)
        print(log('Docker client push image ' + repo + ':' + tag))

        return True
