import requests
import json

from schema import SCHEMA


class DockerRegistry:
    ADDRESS = 'localhost:5000'
    USERNAME = ''
    PASSWORD = ''

    def __init__(self, address, username, password):
        self.ADDRESS = address
        self.USERNAME = username
        self.PASSWORD = password
        self.headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}

    def repositories_list(self):
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/_catalog', headers=self.headers)
        return response.json()['repositories']

    def repository_tags(self, repo):
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/' + repo + '/tags/list', headers=self.headers)
        return response.json()['tags']

    # ids of all images
    def images_list(self):
        res = []
        repositories = self.repositories_list()

        for repository in repositories:
            tags = self.repository_tags(repository)
            if tags is None:
                continue

            for tag in tags:
                image = {'name': repository, 'tag': tag}
                res.append(image)

        return res

    def get_image_data(self, repo, tag):
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + tag,)
        return response.json()

    def remove_image(self, repo, tag):
        image_data = self.get_image_data(repo, tag)
        print(image_data)
        # empty_manifest = '{' \

        #                  '"name": <name>,' \
        #                  '"tag": <tag>,' \
        #                  '"fsLayers": [' \
        #                  '{' \
        #                  '"blobSum": "<digest>"' \
        #                  '},' \
        #                  ']' \
        #                  '],' \
        #                  '"history": <v1 images>,' \
        #                  '"signature": <JWS>' \
        #                  '}'
        put_res = requests.put(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + tag,
                     json.dumps(image_data))
        print(put_res.json())
        image_data = self.get_image_data(repo, tag)
        print(image_data)
        # requests.delete(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + image_id,
        #              headers=self.headers)
        return True

