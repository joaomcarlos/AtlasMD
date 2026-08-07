up:
    docker compose up --build -d

down:
    docker compose down

logs:
    docker compose logs -f

build-image:
    cd atlasmd-renderer && docker build -t ghcr.io/joaomcarlos/atlasmd:latest .
