# Administrador de la flotilla de vehículos empresariales

## Link to System Requirements

You can find the system requirements/project tickets on our [Jira Board](https://vecinosvigilantes.atlassian.net/jira/software/projects/VV/boards/2)

## How to run the project:

1. Copy the .example.env file to .env and fill the variables

```bash
cp .example.env .env
```

2. Do the database migration

```bash
python3 -m app.infrastructure.configs.migrate_database
```

3. Run the server with docker

```bash
docker compose up -d --build
```

4. Check for API docs at:

http://127.0.0.1:8000/docs

5. Check for kibana dashboard at:

http://127.0.0.1:5601/app/home