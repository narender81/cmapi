# covidapi

# docker commands

in v1.config.db_config.py change the below line

app.config["MONGO_URI"] = "mongodb://192.168.0.11:27017/test"

to
app.config["MONGO_URI"] = "mongodb://<ipaddressofmachine>:27017/test"


docker-compose build
docker-compose up -d

docker ps

Narenders-MacBook-Pro:covidapi nbongoni$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
a9b87d836c16        covidapi_web        "flask run"              4 seconds ago       Up 3 seconds        0.0.0.0:5000->5000/tcp     covidapi_web_1
54fedb4f2227        mongo:4.2-bionic    "docker-entrypoint.s…"   5 seconds ago       Up 3 seconds        0.0.0.0:27017->27017/tcp   covidapi_mongodb_1



Test:

# In browser check:

http:://127.0.0.1:5000

should return 
# Hello word
