# Administrador de la flotilla de vehículos empresariales

## Link to System Requirements

You can find the system requirements/project tickets on our [Jira Board](https://vecinosvigilantes.atlassian.net/jira/software/projects/VV/boards/2)

## For running on development:

- Recommended python version: 3.11

1. Create enviroment:

```bash
python3 -m venv env
```

2. Activate enviroment:

On Windows:

```bash
env\Scripts\activate
```

On Unix or MacOS:

```bash
source env/bin/activate
```

3. Install dependencies

```bash
pip3 install -r requirements.txt
```

4. Do the database migration

```bash
python3 -m app.infrastructure.configs.migrate_database
```

5. Run the server

```bash
uvicorn app.main:app --reload
```

6. Check for API docs at:

http://127.0.0.1:8000/docs

