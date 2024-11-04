docker build . -t fullaware/asteroidmining:latest
docker push fullaware/asteroidmining:latest

helm upgrade asteroidmining ./charts/ -n asteroidmining --create-namespace
kubectl rollout restart deploy asteroidmining -n asteroidmining