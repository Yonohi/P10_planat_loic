# Generated by Django 3.2.8 on 2021-12-07 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem_tracking', '0019_alter_contributor_permission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='auteur',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='probleme',
            new_name='issue',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='assigne',
            new_name='assignee_user',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='auteur',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='priorite',
            new_name='priority',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='projet',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='statut',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='balise',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='titre',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='auteur',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='titre',
            new_name='title',
        ),
    ]
