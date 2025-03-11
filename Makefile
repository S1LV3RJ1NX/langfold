up:
	template=${t} docker-compose --env-file .env up -d

down:
	template=${t} docker-compose --env-file .env down

build:
	template=${t} docker-compose --env-file .env up --build -d

restart-backend:
	template=${t} docker-compose --env-file .env restart langfold-backend
