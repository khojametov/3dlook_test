### Setup Python Environment
```shell
python3.8 -m venv venv
source venv/bin/activate
```

Install requirements
```shell
pip install -r requirements/dev.txt
```

### Configure environment variables
```shell
cp env_example .env
```
change .env according your settings

### Setting up Database and Redis
```shell
docker-compose up -d
```

### Migrate migrations
```shell
make migrate
```

### Create Super User
```shell
python3.8 src/manage.py createsuperuser
```

### Running tests
```shell
make test
```

### Install pre-commit
```shell
pre-commit install
```
