# Generated by Django 2.1.5 on 2019-02-21 06:01

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20190220_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]