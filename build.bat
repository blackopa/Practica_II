mkdir data
docker build -f Dockerfile -t automatizationpdf:latest .
REM docker run --name db -d --env-file .env -v "%cd%/data:/var/lib/postgresql/data" -p 5432:5432 postgres:14.1-alpine
sleep 20
docker run -it --rm -w /usr/src/app/ -p 80:8080 automatizationpdf:latest
