# Generated by Django 2.1.5 on 2019-01-23 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190123_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnum',
            name='blog',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog'),
        ),
    ]
