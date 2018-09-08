# Generated by Django 2.1.1 on 2018-09-03 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.CharField(max_length=15)),
                ('qtype', models.CharField(max_length=10)),
                ('text', models.TextField()),
                ('recvdata', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
