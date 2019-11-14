# -*- coding: utf-8 -*-
import requests
import os
from log import log
from datetime import datetime
import time

from schema import SCHEMA
import json


class DockerRegistry:
    ADDRESS = 'localhost:5000'
    USERNAME = ''
    PASSWORD = ''
    date_cache_file_path = ''

    def __init__(self, address='', username='', password=''):
        self.ADDRESS = address
        self.USERNAME = username
        self.PASSWORD = password
        self.date_cache_file_path = 'cache/' + address + '_dates.json'
        self.headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}

    def repositories_list(self):
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/_catalog', headers=self.headers)
        return response.json()['repositories'] if 'repositories' in response.json() else []

    def repository_tags(self, repo):
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/' + repo + '/tags/list', headers=self.headers)
        return response.json()['tags'] if 'tags' in response.json() else []

    # ids of all images
    def images_list(self):
        res = {}
        repositories = self.repositories_list()

        for repository in repositories:
            tags = self.repository_tags(repository)
            if tags is None:
                continue

            filtered_tags = list()
            for tag in tags:
                filtered_tags.append({
                    'name': tag,
                    'created': self.get_creation_date(repository, tag)
                })

            filtered_tags.sort(key=lambda t: t['created'], reverse=True)
            res[repository] = filtered_tags

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

    def check_if_can_be_removed(self, repo, tag):
        image_id = self.get_image_id(repo, tag)

        duplicate_images = self.find_duplicates(repo, tag, image_id)

        print(log('find duplicates for image ' + repo + ':' + tag +
                  ' : ' + (', '.join(duplicate_images)) if duplicate_images.__len__() > 0 else 'no one'))

        return duplicate_images

    def remove_image(self, repo, tag):
        image_id = self.get_image_id(repo, tag)
        print(log('Docker registry ' + self.ADDRESS + ' remove image ' + repo + ':' + tag))

        if not image_id:
            return False

        self.remove_date_from_cache(repo, tag)
        duplicates = self.find_duplicates(repo, tag, image_id)
        for duplicate in duplicates:
            self.remove_date_from_cache(repo, duplicate)

        requests.delete(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + image_id,
                        headers=self.headers)

        return True

    def remove_date_from_cache(self, repo, tag):
        date_cache_file = open(self.date_cache_file_path, 'r')
        data = json.load(date_cache_file)
        date_cache_file.close()

        if repo + ':' + tag in data:
            del data[repo + ':' + tag]
            date_cache_file = open(self.date_cache_file_path, 'w')
            json.dump(data, date_cache_file)
            date_cache_file.close()

    def get_creation_date(self, repo, tag):
        if not os.path.exists(self.date_cache_file_path):
            data = {}
        else:
            date_cache_file = open(self.date_cache_file_path, 'r')
            data = json.load(date_cache_file)
            date_cache_file.close()

        if repo + ':' + tag not in data:
            date = self.request_creation_date(repo, tag)
            data[repo + ':' + tag] = date
            date_cache_file = open(self.date_cache_file_path, 'w')
            json.dump(data, date_cache_file)
            date_cache_file.close()
        else:
            date = data[repo + ':' + tag]

        return date

    def request_creation_date(self, repo, tag):
        response = requests.get(SCHEMA + self.ADDRESS + '/v2/' + repo + '/manifests/' + tag)

        response = response.json()
        if 'history' not in response:
            return 0

        json_response = json.loads(response['history'][0]['v1Compatibility'])

        datetime_object = datetime.strptime(json_response['created'][:-4], '%Y-%m-%dT%H:%M:%S.%f')
        return time.mktime(datetime_object.timetuple())
