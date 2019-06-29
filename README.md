## Development

Clone the project with the following command:

```bash
$ git clone https://github.com/dmytrostriletskyi.git
$ cd heroku-load-balancer
```

To build the project, use the following command:

```bash
$ docker build -t heroku-load-balancer . -f Dockerfile
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -p 7979:7979 -v $PWD:/heroku-load-balancer \
      -e PORT=7979 \
      -e HEROKU_API_KEY='8af7dbb9-e6b8-45bd-8c0a-87787b5ae881' \
      -e PIPELINE_IDENTIFIER='f64cf79b-79ba-4c45-8039-57c9af5d4508' \
      --name heroku-load-balancer heroku-load-balancer
```

If you need to enter the bash of the container, use the following command:

```bash
$ docker exec -it heroku-load-balancer bash
```

Clean all containers with the following command:

```bash
$ docker rm $(docker ps -a -q) -f
```

Clean all images with the following command:

```bash
$ docker rmi $(docker images -q) -f
```
