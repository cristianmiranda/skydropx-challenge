from django.db import migrations

import os
import google.auth
from google.cloud import secretmanager as sm


# This data migration allows you to programatically create a django admin user
# This will run in Cloud Build, which requires Cloud Build to have access to the secret.

def createsuperuser(apps, schema_editor):
    superuser_password = None
    settings = ["SUPERPASS"]

    if all(k in os.environ.keys() for k in set(settings)):
        superuser_password = os.environ["SUPERPASS"]
    else:
        # Retrieve secret from Secret Manager
        _, project = google.auth.default()
        client = sm.SecretManagerServiceClient()
        name = f"projects/{project}/secrets/superuser_password/versions/latest"
        superuser_password = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    # Create a new user using acquired password
    from django.contrib.auth.models import User
    User.objects.create_superuser("admin", password=superuser_password)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunPython(createsuperuser)
    ]
