# MO Technical Test
![GK6dKYGN_400x400](https://github.com/user-attachments/assets/7f4d8abf-3c1d-4304-86e0-dad647614da2)

Request the creation of an API using the Django Rest Framework to manage and monitor client services.


## Requirments:
1. Docker, Docker compose or Docker Desktop [docker](https://www.docker.com/)
2. Git, [git](https://git-scm.com/)

## How to start API?
### Run app through docker


```
git clone https://github.com/Vidanilo10/mo-technicall-challenge.git
```

```
cd mo-technicall-challenge
```

```
docker compose up
```

### Example: 
![How to start API](https://github.com/user-attachments/assets/05cec7b9-0360-4af9-ab3b-33ca5a3578f9)


## Docs:
1. Swagger, [swagger](http://localhost:8000/swagger/)
2. Redoc, [redoc](http://localhost:8000/redoc/)
3. Postman, [postman](https://drive.google.com/file/d/1bX-zjh8kHyaa2J0NJEOsW25TEsb5Ll0H/view?usp=sharing)

## Tests:
```
docker run --rm mo-technicall-challenge-r-web pytest tests/ --disable-warnings
```
![2025-04-15 12-52-24](https://github.com/user-attachments/assets/77716352-4082-413e-9517-bacf60baf4a3)
