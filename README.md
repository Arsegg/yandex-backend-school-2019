# yandex-backend-school-2019

Yandex Backend School project 2019

# Requirements
1. [Install Docker](https://docs.docker.com/install/)
2. [Install Docker-Compose](https://docs.docker.com/compose/install/)
3. [Install git](https://www.atlassian.com/git/tutorials/install-git)

# Installation
```shell script
mkdir app
cd app
git clone git@github.com:Arsegg/yandex-backend-school-2019.git
cd yandex-backend-school-2019
sudo docker-compose up -d
```

# Testing
```shell script
sudo docker-compose -f docker-compose.test.yml up
```