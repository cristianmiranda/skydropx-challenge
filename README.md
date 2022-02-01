# 🧐 Project Tracker

![ci](https://github.com/cristianmiranda/skydropx-challenge/actions/workflows/ci.yml/badge.svg) ![Website](https://img.shields.io/website?down_message=offline&label=webapp&logo=google-cloud&up_message=online&url=https%3A%2F%2Fprojecttracker-ie2endhizq-uc.a.run.app) [![codecov](https://codecov.io/gh/cristianmiranda/skydropx-challenge/branch/master/graph/badge.svg)](https://codecov.io/gh/cristianmiranda/skydropx-challenge)

🔗 https://projecttracker-ie2endhizq-uc.a.run.app
```bash
admin_username = admin
admin_password = bhwaXVDITBYiZRNdcADe4th29VL6oFSy
```

## ☁️ Cloud Provisioning y Deployment

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


## 🐋 Despliegue local con Docker

1. Iniciar servicios de DB y webapp
```bash
cp .env.local .env
docker-compose up -d
```

2. Aplicar migration scripts
```bash
docker-compose run --rm web python manage.py migrate
```


## 🖥️ Desarrollo en ambiente local

Para desarrollar localmente contamos con dos opciones en cuanto a la conexión con la base de datos:
1. Utilizar una base de datos instalada localmente
2. Utilizar la base de datos en la nube utilizando `cloud_sql_proxy`

### 🔹 DB local

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

4. Iniciar aplicación

   ```bash
   python manage.py runserver
   ```

### 🔹 DB remota

Luego de haber desplegado la aplicación utilizando Terraform:

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
   
4. Iniciar la aplicación utilizando un flag para que Django utilice el proxy

   ```bash
   USE_CLOUD_SQL_AUTH_PROXY=true python manage.py runserver
   ```


## 🧪 Tests

Al igual que al desarrollar localmente, para ejecutar tests también hay dos opciones (DB local vs. DB remota).

### 🔹 DB local
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

### 🔹 DB remota
```bash
cloud_sql_proxy -instances=${PROJECT_ID}:us-central1:projecttracker=tcp:0.0.0.0:5432
```
```bash
# Unit tests
USE_CLOUD_SQL_AUTH_PROXY=true pytest

# BDD integration tests
USE_CLOUD_SQL_AUTH_PROXY=true python manage.py behave
```

## ♻️ Modificaciones

Al realizar modificaciones al modelo, también debemos generar los migration scrips que serán los encargados de aplicar los cambios necesarios en nuestra base de datos.

```bash
python manage.py makemigrations projecttracker
```

Para desplegar nuevos cambios (incluyendo los realizados en el modelo), debemos ejecutar lo siguiente:
```bash
gcloud builds submit --config cloudbuild-full.yaml
```

---

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

#### Skydropx Python Challenge 2022
