.PHONY: base up down logs clean

base:
	docker build -t hadoop-hive-spark-base deployment/base

up:
	cd deployment && docker compose up --build -d

down:
	cd deployment && docker compose down

logs:
	cd deployment && docker compose logs -f

clean:
	cd deployment && docker compose down -v