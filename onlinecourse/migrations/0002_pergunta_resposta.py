# Generated by Django 3.1.3 on 2023-08-27 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_pergunta', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_resposta', models.CharField(max_length=100)),
                ('correta', models.BooleanField(default=False)),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.pergunta')),
            ],
        ),
    ]
