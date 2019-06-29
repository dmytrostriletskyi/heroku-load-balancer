Automatic (with no manual configuring) load balancer for your Heroku pipeline production applications.

[![Release](https://img.shields.io/github/release/dmytrostriletskyi/heroku-load-balancer.svg)](https://github.com/dmytrostriletskyi/heroku-load-balancer/releases)
[![Build Status](https://travis-ci.com/dmytrostriletskyi/heroku-load-balancer.svg?branch=develop)](https://travis-ci.com/dmytrostriletskyi/heroku-load-balancer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

  * [Getting started](#getting-started)
    * [What is a load balancer](#what-is-a-load-balancer)
    * [Motivation](#motivation)
    * [How to use](#how-to-use)
    * [How it works](#how-it-works)
  * [Development](#development)

## Getting started

### What is a load balancer

A load balancer is a device that distributes network or application traffic across a cluster of servers. A load balancer 
sits between the client and the server farm accepting incoming network and application traffic and distributing the 
traffic across multiple backend servers. By balancing application requests across multiple servers, a load balancer 
reduces individual server load and prevents any one application server from becoming a single point of failure, 
thus improving overall application availability and responsiveness.

![Illustation on how load balancer works](https://habrastorage.org/webt/iy/-s/vx/iy-svxvpqwnquwvciv7qm3pfm1u.png)

### Motivation

[Heroku](https://heroku.com) does not have `load balancer` paid feature to balancing your applications. It is the drawback
comparing to [Digital Ocean](https://www.digitalocean.com/products/load-balancer) and [Amazon Web Services](https://aws.amazon.com/elasticloadbalancing/)
which do have it.

### How to use

1. Press the button named `Deploy to Heroku` below.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/dmytrostriletskyi/heroku-load-balancer/tree/create-docs)

2. Enter the name for the application which will host the load balancer. Choose the region and add to the pipeline if needed.

<img src="https://habrastorage.org/webt/xq/rp/nl/xqrpnlgqh0-3o1kldfk2pflvtvy.png" width="900" height="440">

3. Visit the [Heroku account setting page](https://dashboard.heroku.com/account), find the `API Key` section, reveal the key and
paste it to the `HEROKU_API_KEY` field. 

<img src="https://habrastorage.org/webt/v0/g7/wt/v0g7wtn1qltm8-_jpfdug4djkya.png" width="900" height="104">

3. Open the preferable pipeline and copy its identifier from the URL. On the screenshoot it is `f64cf79b-79ba-4c45-8039-57c9af5d4508` mentioned by red arrow at the top.

<img src="https://habrastorage.org/webt/he/0j/c-/he0jc-ubwjfxajbn85lg_ysa14m.png" width="900" height="400">

4. Return to the deploying page, paste the identifier to the `PIPELINE_IDENTIFER` field.

<img src="https://habrastorage.org/webt/zu/1v/wo/zu1vwo1y54o_efk9jqdrxpwpgeg.png" width="900" height="90">

5. Press the button named `Deploy app`. The process of deploying will start immediately as illustrated below.

<img src="https://habrastorage.org/webt/0o/7l/k0/0o7lk0gv5lzp5ij14yepe17a4g4.png" width="900" height="340">

6. When build is finished, you can manage your application (rename, etc.) and view it (open URL in the browser).

<img src="https://habrastorage.org/webt/wh/lo/sp/whlospuzvfmazjpdsrf52iduxf0.png" width="900" height="128">

7. To check if load balancer works properly, just open logs of each production back-end servers 
(`heroku logs --tail -a application-name` in the terminal), and send the request to the load balancer application. 
As the result, the load balancer will proxy your request to the each back-end server in round-robin method (one by one in order).

<img src="https://habrastorage.org/webt/zm/bn/vj/zmbnvj7ztr3ho4y6xt6mfxt2qh4.png" width="900" height="480">

### How it works

1. You specify pipeline's identifier (`PIPELINE_IDENTIFER`) to create load balancer for its applications in `production` stage.
2. Through the [Heroku API](https://devcenter.heroku.com/categories/platform-api) using your `HEROKU_API_KEY`, URLs of applications are fetched.
3. Then [configuration file for load balancing](http://nginx.org/en/docs/http/load_balancing.html) based on fetched URLS is created.
4. And served by the [Nginx](https://nginx.org/en) in round-robin method (one by one in order).

## Development

Clone the project with the following command:

```bash
$ git clone https://github.com/dmytrostriletskyi/heroku-load-balancer.git
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
