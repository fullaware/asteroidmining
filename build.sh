docker build . -t fullaware/asteroidmining:latest
docker push fullaware/asteroidmining:latest

helm upgrade asteroidmining ./asteroidmining/ -n asteroidmining --create-namespace
kubectl rollout restart deploy asteroidmining-app -n asteroidmining