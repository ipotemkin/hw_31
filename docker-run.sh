#docker run --name skyvito-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -d postgres:12.4-alpine

#docker run --name skyvito-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v /Users/igorpotemkin/pg:/var/lib/postgresql/data -d postgres:12.4-alpine

p=$(pwd)"/data"

docker run --name skyvito-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v $p:/var/lib/postgresql/data -d postgres:12.4-alpine
