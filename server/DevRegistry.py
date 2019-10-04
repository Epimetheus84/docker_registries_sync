from server.DockerRegistry import DockerRegistry


class DevRegistry(DockerRegistry):
    ADDRESS = 'localhost:5000'
    USERNAME = ''
    PASSWORD = ''
