# ๐ง Project Tracker

![ci](https://github.com/cristianmiranda/skydropx-challenge/actions/workflows/ci.yml/badge.svg) ![Website](https://img.shields.io/website?down_message=offline&label=webapp&logo=google-cloud&up_message=online&url=https%3A%2F%2Fprojecttracker-ie2endhizq-uc.a.run.app) [![codecov](https://codecov.io/gh/cristianmiranda/skydropx-challenge/branch/master/graph/badge.svg)](https://codecov.io/gh/cristianmiranda/skydropx-challenge)

๐ https://projecttracker-ie2endhizq-uc.a.run.app
```bash
admin_username = admin
admin_password = bhwaXVDITBYiZRNdcADe4th29VL6oFSy
```

https://user-images.githubusercontent.com/972572/152010870-98f6b9e7-2038-478b-b304-5a523f63c1f2.mov

### รndice
- [๐ง Project Tracker](https://github.com/cristianmiranda/skydropx-challenge#-project-tracker)
  * [โ๏ธ Cloud Provisioning y Deployment](https://github.com/cristianmiranda/skydropx-challenge#%EF%B8%8F-cloud-provisioning-y-deployment)
  * [๐ Despliegue local con Docker](https://github.com/cristianmiranda/skydropx-challenge#-despliegue-local-con-docker)
  * [๐ฅ๏ธ Desarrollo en ambiente local](https://github.com/cristianmiranda/skydropx-challenge#%EF%B8%8F-desarrollo-en-ambiente-local)
    + [๐น DB local](https://github.com/cristianmiranda/skydropx-challenge#-db-local)
    + [๐น DB remota](https://github.com/cristianmiranda/skydropx-challenge#-db-remota)
  * [๐งช Tests](https://github.com/cristianmiranda/skydropx-challenge#-tests)
    + [๐น DB local](https://github.com/cristianmiranda/skydropx-challenge#-db-local-1)
    + [๐น DB remota](https://github.com/cristianmiranda/skydropx-challenge#-db-remota-1)
  * [โป๏ธ Modificaciones](https://github.com/cristianmiranda/skydropx-challenge#%EF%B8%8F-modificaciones)

## โ๏ธ Cloud Provisioning y Deployment

1. Configurar proyecto de GCP

   ```bash
   export PROJECT_ID=skydropx-challenge-app-339914
   gcloud config set project $PROJECT_ID
   ```

2. Configurar credenciales de acceso:

   ```bash
   gcloud auth application-default login
   ```

3. Habilitar servicios requeridos:

   ```bash
   gcloud services enable \
     cloudbuild.googleapis.com \
     run.googleapis.com \
     cloudresourcemanager.googleapis.com
   ```

4. Generar imagen base

   ```bash
   gcloud builds submit
   ```

5. Aplicar cambios utilizando Terraform

   ```bash
   terraform init
   terraform apply -var project=$PROJECT_ID
   ```

6. Aplicar database migrations

   ```bash
   gcloud builds submit --config cloudbuild-migrate.yaml
   ```

7. Obtener URL y superuser password:

   ```bash
   terraform output service_url
   terraform output superuser_password
   ```

![image](https://user-images.githubusercontent.com/972572/152024733-726ce280-cb8a-474d-8e91-fb49ab12606a.png)


## ๐ Despliegue local con Docker

1. Iniciar servicios de DB y webapp
```bash
cp .env.local .env
docker-compose up -d
```

2. Aplicar migration scripts
```bash
docker-compose run --rm web python manage.py migrate
```


## ๐ฅ๏ธ Desarrollo en ambiente local

Para desarrollar localmente contamos con dos opciones en cuanto a la conexiรณn con la base de datos:
1. Utilizar una base de datos instalada localmente
2. Utilizar la base de datos en la nube utilizando `cloud_sql_proxy`

### ๐น DB local

1. Copiar el archivo `.env` de ejemplo

   ```bash
   cp .env.local .env 
   ```

2. Iniciar la base de datos con Docker

   ```bash
   docker-compose up db
   ```

3. Aplicar migration scripts

   ```bash
   python manage.py migrate
   ```

4. Iniciar aplicaciรณn

   ```bash
   python manage.py runserver
   ```

### ๐น DB remota

Luego de haber desplegado la aplicaciรณn utilizando Terraform:

1. Install Cloud SQL Auth Proxy and run in a separate process. Generate the command from terraform output:
   
   ```bash
   cloud_sql_proxy -instances=${PROJECT_ID}:us-central1:projecttracker=tcp:0.0.0.0:5432
   ```

2. Inicializar el ambiente virtual e instalar dependencias 
   
   ```bash
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   
4. Iniciar la aplicaciรณn utilizando un flag para que Django utilice el proxy

   ```bash
   USE_CLOUD_SQL_AUTH_PROXY=true python manage.py runserver
   ```


## ๐งช Tests

Al igual que al desarrollar localmente, para ejecutar tests tambiรฉn hay dos opciones (DB local vs. DB remota).

### ๐น DB local
```bash
cp .env.local .env
docker-compose up db
```
```bash
# Unit tests
pytest

# BDD integration tests
python manage.py behave
```

### ๐น DB remota
```bash
cloud_sql_proxy -instances=${PROJECT_ID}:us-central1:projecttracker=tcp:0.0.0.0:5432
```
```bash
# Unit tests
USE_CLOUD_SQL_AUTH_PROXY=true pytest

# BDD integration tests
USE_CLOUD_SQL_AUTH_PROXY=true python manage.py behave
```

## โป๏ธ Modificaciones

Al realizar modificaciones al modelo, tambiรฉn debemos generar los migration scrips que serรกn los encargados de aplicar los cambios necesarios en nuestra base de datos.

```bash
python manage.py makemigrations projecttracker
```

Para desplegar nuevos cambios (incluyendo los realizados en el modelo), debemos ejecutar lo siguiente:
```bash
gcloud builds submit --config cloudbuild-full.yaml
```

---

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
