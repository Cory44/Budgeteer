# Generated by Django 3.0.3 on 2020-03-25 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgeteer_app', '0003_auto_20200323_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactioncategory',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
