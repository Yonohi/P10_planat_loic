# Generated by Django 3.2.8 on 2021-10-29 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem_tracking', '0007_rename_description_commentaire_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='probleme',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='projet', to='problem_tracking.projet'),
        ),
    ]
