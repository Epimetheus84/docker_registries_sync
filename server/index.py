from server.DevRegistry import DevRegistry
from server.DockerClient import DockerClient

dev_reg = DevRegistry()
images = dev_reg.images_list()
print(images)

image = images[0]
image_id = dev_reg.get_image_id(image)
print(image_id)

docker_cli = DockerClient()
docker_cli.login(DevRegistry.ADDRESS, DevRegistry.USERNAME, DevRegistry.PASSWORD)
pulled_image = docker_cli.pull_image(dev_reg.ADDRESS, image['name'], image['tag'])

ubuntu = docker_cli.get_image('localhost:5000/my-ubuntu:latest')
docker_cli.remove_image(pulled_image)

dev_reg.remove_image(image)
