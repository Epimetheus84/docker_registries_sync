import requests

from server.schema import SCHEMA
from docker_registry_client import DockerRegistryClient
from abc import ABC


# abstract class
class DockerRegistry(ABC):
    ADDRESS = ''

    def __init__(self):
        self.client = DockerRegistryClient(SCHEMA + self.ADDRESS)
        self.headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}

    # ids of all images
    def images_list(self):
        res = []
        repositories = self.client.repositories()
        print(repositories)

        for repository in repositories:
            image = {
                'name': repository,
                'tag': ''
            }

            tags = self.client.repository(repository).tags()
            if tags is None:
                continue

            for tag in tags:
                image['tag'] = tag
                res.append(image)

        return res

    # TODO: переделать используя библиотеку DockerRegistryClient, сейчас она еще не способна работать с RegistryV2
    def get_image_id(self, image):
        tag = image['tag']
        repo = image['name']
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + tag, headers=self.headers)
        return response.headers['Docker-Content-Digest']

    def remove_image(self, image):
        image_id = self.get_image_id(image)
        repo = image['name']
        print(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + image_id)
        requests.delete(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + image_id,
                        headers=self.headers)
        return True
