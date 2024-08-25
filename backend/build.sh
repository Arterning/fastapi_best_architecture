docker build -t fba-server . -f ./backend.dockerfile
docker build -t fba-celery .  -f ./celery.dockerfile