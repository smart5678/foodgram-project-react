# Foodgram workflow
## Clone repo from git:
Clone this repo via one of the following commands:
- https: 
  ```bash
  git clone https://github.com/smart5678/foodgram-project-react.git
  ```
- SSH:
  ```bash
  git clone git@github.com:smart5678/foodgram-project-react.git
  ```

## Sample Usage
You must have installed Docker and docker-compose on the remote server before running this project. [Docker installation manual](https://docs.docker.com/engine/install/)
### Run project:
```bash
sudo docker-compose up
```

### First run:

From ./infra/ folder:

- Make migrations:
```bash
sudo docker-compose exec web python manage.py migrate --noinput
```
- Create superuser:
```bash
sudo docker-compose exec web python manage.py createsuperuser
```
- Load sample data:
```bash
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
- CollectStatic
```bash
sudo docker-compose exec web python manage.py collectstatic --no-input 
```
### Passing pytest:
```bash
sudo docker-compose exec web pytest
```

## Configurations Files:
### Nginx
./infra/default.conf

Must be copied to product server to /etc/nginx/conf.d 

### Database Settings:
Can be stored in `./.env`

You must provide this environment variables for database settings:
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<db_name>
POSTGRES_DB=<db_name>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<password>
DB_HOST=db
DB_PORT=5432
```

After make changes in configuration use:
```bash
docker-compose up --build
```
for rebuild Django image
## License
This project is licensed under the MIT license.
### Author - https://github.com/smart5678
