# shellcheck disable=SC2046
docker rm -f $(docker ps -a -q)
# shellcheck disable=SC2046
docker rmi $(docker images -q)