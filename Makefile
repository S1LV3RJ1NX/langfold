up:
	docker-compose --env-file .env up -d

down:
	docker-compose --env-file .env down

build:
	docker-compose --env-file .env up --build -d


restart-backend:
	docker-compose --env-file .env restart langfold-backend
