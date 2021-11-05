# Generated by Django 3.2.8 on 2021-10-29 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problem_tracking', '0010_projet_auteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probleme',
            name='projet',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='problemes', to='problem_tracking.projet'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='Auteur',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='projets', to=settings.AUTH_USER_MODEL),
        ),
    ]
