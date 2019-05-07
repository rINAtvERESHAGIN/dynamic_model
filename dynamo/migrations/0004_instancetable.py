# Generated by Django 2.1.8 on 2019-04-06 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynamo', '0003_fieldsformodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fields_for_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamo.FieldsForModel')),
                ('my_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamo.MyModel')),
            ],
        ),
    ]