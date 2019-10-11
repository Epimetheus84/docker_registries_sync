import requests
from log import log

from schema import SCHEMA


class DockerRegistry:
    ADDRESS = 'localhost:5000'
    USERNAME = ''
    PASSWORD = ''

    def __init__(self, address='', username='', password=''):
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
        res = {}
        repositories = self.repositories_list()

        for repository in repositories:
            tags = self.repository_tags(repository)
            if tags is None:
                continue

            res[repository] = tags

        return res

    def get_image_id(self, repo, tag):
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + tag,
                                headers=self.headers)

        if 'Docker-Content-Digest' not in response.headers:
            return False

        return response.headers['Docker-Content-Digest']

    def find_duplicates(self, repo, tag, original_id):
        # проверяем существуют ли еще теги с таким id
        duplicate_images = list()

        repo_tags = self.repository_tags(repo)
        repo_tags.remove(tag)

        for repo_tag in repo_tags:
            repo_image_id = self.get_image_id(repo, repo_tag)
            if repo_image_id != original_id:
                continue
            duplicate_images.append(repo_tag)

        return duplicate_images

    def remove_image(self, repo, tag, force=False):
        image_id = self.get_image_id(repo, tag)

        duplicate_images = self.find_duplicates(repo, tag, image_id)

        if not force and duplicate_images.__len__() > 0:
            return duplicate_images

        if not image_id:
            return False

        print(log('Docker registry ' + self.ADDRESS + ' remove image ' + repo + ':' + tag
                  + ((' duplicates:' + ', '.join(duplicate_images)) if duplicate_images.__len__() > 0 else '')))
        requests.delete(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + image_id,
                        headers=self.headers)
        return True
