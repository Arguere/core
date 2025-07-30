# Monolog

How to activate the poetry environment:

```bash
 eval $(poetry env activate)
```

How to install the dependencies:

```bash
poetry install
```

Generate migration

```bash
alembic revision --autogenerate -m ""
```

Apply the migration

```bash
alembic upgrade head
```
