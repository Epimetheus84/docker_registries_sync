import docker

from server.schema import SCHEMA


class DockerClient:
    ADDRESS = 'unix://var/run/docker.sock'

    def __init__(self):
        self.client = docker.DockerClient(base_url=self.ADDRESS)

    def login(self, address, username, password):
        address = SCHEMA + address
        self.client.login(registry=address, username=username, password=password)

    def images_list(self):
        images_list = self.client.images.list()
        return images_list

    def get_image(self, image_id):
        image = self.client.images.get(image_id)
        return image

    def remove_image(self, image):
        self.client.images.remove(image)
        return True

    def pull_image(self, src, repo, tag):
        repo = src + '/' + repo
        self.client.images.pull(repository=repo, tag=tag)
        return repo + ':' + tag

    def push_image(self, repo, tags):
        output = self.client.images.push(repository=repo, tag=tags)

        for line in output:
            print(line)

        return True
