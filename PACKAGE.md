## Add a Dockerfile to the same directory as your Python file

You will build a Docker container to run your Darcy AI application. You only need your Python file and a Dockerfile to build the container. Make sure you create this Dockerfile in the same directory as your Python file and change the name from YOURFILE.py to the actual name of your file.
```
FROM darcyai/darcy-ai-coral:dev

RUN python3 -m pip install --upgrade darcyai

COPY YOURFILE.py /src/my_app.py

ENTRYPOINT ["/bin/bash", "-c", "cd /src/ && python3 -u ./my_app.py"]
```

## Build your Docker container

Use the following command to build your Docker container. It may take 10 or 15 minutes if you are building for the first time and you do not have a very fast internet connection. This is because the underlying container [base images](./TERMINOLOGY.md#docker-base-image) will need to be downloaded. After the first build, this process should only take a minute or two.
```
sudo docker build -t darcydev/my-people-ai-app:1.0.0 .
```

## Run your application

Use this Docker command to run your application container right away. You can also use this Docker container with the [Darcy Cloud](https://cloud.darcy.ai) to deploy and manage the application.
```
sudo docker run -d --privileged --net=host -p 3456:3456 -p 8080:8080 -v /dev:/dev darcydev/my-people-ai-app:1.0.0
```