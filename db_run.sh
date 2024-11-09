docker run --name mysql-local -p 3306:3306 -e MYSQL_ROOT_PASSWORD=test -d mysql:8

# in container
mysql -u root -p

# mysql
CREATE SCHEMA 'fastapi-ca';

# out container
# database.py, user/infra/db_models/user.py, alembic.ini, migrations/env.py, database_models.py
alembic revision --autogenerate -m "add User Table"
alembic upgrade head