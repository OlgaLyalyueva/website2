from django.db import migrations
from django.contrib.auth.models import User


def set_avatar(apps, schema_editor):
    Avatar = apps.get_model('blog', 'Avatar')
    for row in User.objects.all().values():
        a = Avatar()
        a.fk_user_id = row['id']
        a.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200531_1828'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(set_avatar, reverse_code=migrations.RunPython.noop),
    ]