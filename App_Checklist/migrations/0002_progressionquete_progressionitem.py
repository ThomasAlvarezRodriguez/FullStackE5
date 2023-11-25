# Generated by Django 4.2.7 on 2023-11-25 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_Checklist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressionQuete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obtenu', models.BooleanField(default=False)),
                ('quete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Checklist.quete')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('utilisateur', 'quete')},
            },
        ),
        migrations.CreateModel(
            name='ProgressionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obtenu', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Checklist.item')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('utilisateur', 'item')},
            },
        ),
    ]
