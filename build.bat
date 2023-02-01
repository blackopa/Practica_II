docker build -f Dockerfile -t automatizationpdf:latest .
docker run --name db -d --env-file .env -v "%cd%/data:/var/lib/postgresql/data" -p 5432:5432 postgres:14.1-alpine
sleep 5
docker run -it --rm --link db:db -w /usr/src/app/ -p 80:8080 automatizationpdf:latest
