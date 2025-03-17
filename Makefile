up:
	template=${t} docker-compose --env-file .env up -d

down:
	template=${t} docker-compose --env-file .env down

build:
	template=${t} docker-compose --env-file .env up --build -d

redis-cli:
	docker-compose --env-file .env exec redis redis-cli -h langfold-redis -p 6380 -a ${p}
