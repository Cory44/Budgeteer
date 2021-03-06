# Generated by Django 3.0.3 on 2020-03-30 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgeteer_app', '0005_auto_20200326_1225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='transactioncategory',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgeteer_app.Account'),
        ),
    ]
