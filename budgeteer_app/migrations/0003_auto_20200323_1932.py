# Generated by Django 3.0.3 on 2020-03-23 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgeteer_app', '0002_auto_20200322_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactioncategory',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='current_balance',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
