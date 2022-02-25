# Darcy AI Application Deployment Guide

Once you have built a Darcy AI application, you can deploy it to as many devices as you want. Use this guide to get devices set up on the [Darcy Cloud](https://cloud.darcy.ai) and create your own deployment YAML files and deploy your applications.

## Make sure your Darcy AI application container is available

If you followed the instructions in the [Build Guide](./BUILD.md) you probably created an application container called `darcydev/my-people-ai-app:1.0.0`. All Docker container identifiers are made of three parts. The first part, which is `darcydev` in this case, is the organization name. You must be a member of an organization in order to upload container images to that organization in [Docker Hub](https://hub.docker.com).

If you don't already have an account, create one now at [https://hub.docker.com](https://hub.docker.com). You will be given an organization which is your username.

If you used `darcydev` as your organization then you won't be able to upload your container image to Docker Hub. You can run your build command again but use a different container identifier and the build will be very quick. Docker will just make a copy of the container image with the new identifier.

The second part of the identifier is the container name. It comes after the `/` and it can be whatever you want. You can think of this as something like a file name. The third pard is the tag. It comes after the `:` and it can also be whatever you want. A standard practice is to use the tag to identify different versions of the same application container.

Once you have a new identifier for your Darcy AI application container and you have built the container image, you can add it to Docker Hub using the command `docker push YOUR_ORGANIZATION/YOUR_APP:tag.goes.here` where you have replaced the placeholders with the appropriate information, of course. You will use this identifier in your application deployment YAML file below.


## Add your devices to the Darcy Cloud

Use the Darcy Cloud to manage your device and your edge AI applications. If you don't already have an account, you can create one now for free. Create an account or log in at [https://cloud.darcy.ai](https://cloud.darcy.ai).

Once you are in your Darcy Cloud account, add your device as a node in your current project. You can use any of several methods to add a node, such as the "add node" button or the "plus button" in the bottom left. Follow the instructions in the pop-up window to add your device as a node.

<img src="./docs/img/darcy-cloud-add-node-button.png" height="100" /> <img src="./docs/img/darcy-cloud-plus-node.png" height="100" /> <img src="./docs/img/darcy-cloud-plus-item-button.png" height="100" />

## Create your application YAML

Here is a sample YAML file to work with.

```
kind: Application
apiVersion: iofog.org/v3
metadata:
  name: your-application-name
spec:
  microservices:
    - name: your-microservice-name
      agent:
        name: your-darcy-cloud-node-name
      images:
        arm: 'YOUR_ORGANIZATION/YOUR_APP:tag.goes.here'
        x86: 'YOUR_ORGANIZATION/YOUR_APP:tag.goes.here'
      container:
        rootHostAccess: true
        ports: []
        volumes:
          - containerDestination: /dev
            hostDestination: /dev
            type: bind
            accessMode: rw
```

You can find this sample YAMl file in the `examples/deploy/` directory called [app_deployment.yml](./examples/deploy/app_deployment.yml).

Your application deployment YAML file contains the information that the Darcy Cloud uses to load and run your Darcy AI application on any device. Replace the placeholder fields with your own information and save the file with whatever file name you like, such as `my-app-deploy.yml`. 

## Deploy your Darcy AI application
