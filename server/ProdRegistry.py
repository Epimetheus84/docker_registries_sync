from server.DockerRegistry import DockerRegistry


class ProdRegistry(DockerRegistry):
    ADDRESS = 'localhost:5005'
    USERNAME = ''
    PASSWORD = ''
