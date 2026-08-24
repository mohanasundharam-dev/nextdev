from django.db import migrations


def seed_technologies(apps, schema_editor):
    Tag = apps.get_model('projectapp', 'Tag')
    for name in ('React', 'Django', 'Spring Boot', '.NET', 'Node.js', 'Angular', 'Vue.js', 'Laravel', 'FastAPI'):
        Tag.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ('projectapp', '0002_remove_movie_vote_movie_created_movie_demo_link_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='tag',
            new_name='technology',
        ),
        migrations.RunPython(seed_technologies, migrations.RunPython.noop),
    ]