# Generated by Django 3.0.6 on 2020-05-22 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200522_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='fk_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='fk_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
