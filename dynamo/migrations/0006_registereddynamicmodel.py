# Generated by Django 2.1.8 on 2019-04-23 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamo', '0005_auto_20190422_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredDynamicModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('token', models.UUIDField()),
            ],
        ),
    ]