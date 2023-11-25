# Generated by Django 4.2.7 on 2023-11-25 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Checklist', '0002_progressionquete_progressionitem'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='progressionquete',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='progressionquete',
            name='quete',
        ),
        migrations.RemoveField(
            model_name='progressionquete',
            name='utilisateur',
        ),
        migrations.AddField(
            model_name='profilutilisateur',
            name='items_obtenus',
            field=models.ManyToManyField(blank=True, to='App_Checklist.item'),
        ),
        migrations.AddField(
            model_name='profilutilisateur',
            name='quetes_obtenues',
            field=models.ManyToManyField(blank=True, to='App_Checklist.quete'),
        ),
        migrations.AlterField(
            model_name='profilutilisateur',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='ProgressionItem',
        ),
        migrations.DeleteModel(
            name='ProgressionQuete',
        ),
    ]