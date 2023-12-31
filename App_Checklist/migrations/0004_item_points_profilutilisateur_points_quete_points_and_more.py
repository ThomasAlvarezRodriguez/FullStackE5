# Generated by Django 4.2.7 on 2023-11-28 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Checklist', '0003_alter_progressionquete_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profilutilisateur',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quete',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profilutilisateur',
            name='items_obtenus',
            field=models.ManyToManyField(to='App_Checklist.item'),
        ),
        migrations.AlterField(
            model_name='profilutilisateur',
            name='quetes_obtenues',
            field=models.ManyToManyField(to='App_Checklist.quete'),
        ),
    ]
