from server.DockerRegistry import DockerRegistry


class ProdRegistry(DockerRegistry):
    ADDRESS = 'unix://var/run/docker.sock'
