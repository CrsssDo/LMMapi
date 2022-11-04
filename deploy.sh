#!/bin/zsh

program_name=$0

function usage {
    echo "Error : You must specify the branch to deploy. (staging or main only)"
    echo "usage: $program_name [branch name]"
    exit 1
}

if [[ $# -eq 0 ]] ; then
    usage
    exit 1
fi

if [[ $1 != "staging" && $1 != "main" ]] ; then
    usage
    exit 1
fi

host="admin-nnv@45.124.95.66"

if [[ $1 == "staging" ]]; then
    host="admin-nnv@103.109.43.24"
fi

ssh ${host} << ENDSSH
  cd ~/app/api
  git pull
  cd ..
  docker compose up api -d --build
  docker compose exec api alembic upgrade head
  exit
ENDSSH

