# MMGG-BE

### INFO

Chungnam National University Open Data Contest
Title : Notice Subscription Service (NSS)

### Description

Docker-compose contains Mysql databases and API backend server to send requests to frontend. it is development repository, actual service will be set to AWS EC2 and RDS


### Features

- Server side processing

### Installation

```
git clone https://github.com/MoaMoaGGyung/MMGG-BE.git
docker-compose up (or to skip debug -d option)

docker-compose down : stop containers
docker-compose build : build containers
#(not necessaries)

```


### Environment

- Docker Ubuntu 20.04 LTS   
- Server Backend : Fastapi

### DevOps

- Docker-compose
- Docker



### API

You can check API Swagger docs and Test API requests
http://localhost:8080/docs

### Testing

Installation 항목에서 서술한대로 진행후
1. http://localhost:8080/docs 접속 (Swagger)
2. /execute-sql-file 항목을 클릭후 Execute
3. response로 success~~ 응답을 받은후
4. /departments 항목에서 execute하여 departments_id 확인후
5. /posts/{department_id}에 department_id에 1을 넣은후 execute하면 
6. notion에 있는 api처럼 response가 생성되는 것을 확인 가능


### TO-DO
[] API를 요청하여 학과 - Code를 작업하여 저장할 필요가 있음
[] 2,3 API 작성
[] API로 부터 일정 주기로 DB에 저장후 -> Logstash -> es indexing pipeline






  



