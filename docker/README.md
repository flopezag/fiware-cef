# Quick reference

-	**Where to get help**:  
	[The Docker Community Forums](https://forums.docker.com/) or [the Docker Community Slack](https://blog.docker.com/2016/11/introducing-docker-community-directory-docker-community-slack/).

-	**Where to file issues**:  
	[https://github.com/flopezag/fiware-cef/issues](https://github.com/flopezag/fiware-cef/issues).

-	**Maintained by**:  
	[The FIWARE Foundation team](https://github.com/flopezag).

-	**Source of this description**:  
	[Docs deployment in docker](https://github.com/flopezag/fiware-cef/blob/master/docker/README.md), 
    ([history](https://github.com/flopezag/fiware-cef/commits/master/docker/README.md)).

-	**Supported Docker and Docker-Compose versions**:  
	[The Docker Engine 18.09.1 version](https://github.com/docker/docker-ce/releases/tag/v18.09.1) and 
	[the docker-compose version 1.23.2, build 1110ad01](https://github.com/docker/compose/releases/tag/1.23.2).
	(down to docker engine 18.09.1 and docker-compose 1.23.2, build 1110ad01 on a best-effort basis).

## How to use FIWARE-CEF with Docker

In order to deploy and execute the service with docker, you need to follow some steps. If the image is not generated,
the first step consists on generating the corresponding image. See section **Create the Docker Image**. If the docker
image is available in the [Docker Registry](https://cloud.docker.com/u/flopez/repository/docker/flopez/fiware-cef), you
can follow the steps defined in the section **Docker Compose deployment**.

You need to have docker in your machine. See the [documentation](https://docs.docker.com/installation/) on how to do 
this. 


----
## Create the Docker Image

The first steps is to login inside the docker system through the execution of the command:

```console
docker login
```

In order to create the proper image you need to have installed docker engine.
The first command is used to generate the docker image from the defined Dockerfile.

```console
docker build -f Dockerfile -t fiware/fiware-cef:1.0.0 .
```

It creates the corresponding docker image tagged with fiware/fiware-cef. Currently, the only version that was 
supported and generated is the 1.0.0. Down versions to 1.0.0 are on a best-effort basis. The next step is 
upload the image into a repository (in our case [Docker Hub](https://hub.docker.com/)).

```console
docker push fiware/fiware-cef:1.0.0
```

## Docker Compose deployment

The [docker-compose folder](https://github.com/flopezag/fiware-cef/docker) provides you the corresponding 
docker-compose description file in order to deploy a complete instance of FIWARE-CEF synchroniza<tion file
using docker-compose. Before executing the service it is needed that you create two files, jirasync.py and
the database jirasync.db.

The first file contains the configuration data to access to the Jira services. You can execute the following
command to make a copy of the sample configuration file deployed in the repository:

````console
cp ./jirasync/conf/jirasync.ini ./docker/jirasync.ini
```` 

After the proper definition of the values, you can execute the command:

```console
docker-compose -f docker-compose.yml up
```

## License

These scripts are licensed under Apache License 2.0.
