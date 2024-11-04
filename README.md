# Classic Asteroid Mining Game

## Risks of getting lucky in space  

## Run from Docker
```
docker build . -t fullaware/asteroids:latest
docker run -p 8000:8000 fullaware/asteroids:latest 
```
## OR run `docker-compose` to include MongoDB
```
docker compose up --build --force-recreate --no-deps --remove-orphans [-d]
```