# Generated by Django 5.0.6 on 2024-05-14 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LearningMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('title', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('description', models.CharField(default='', max_length=400, null=True)),
                ('file_path', models.URLField()),
                ('original_filename', models.CharField(max_length=255)),
                ('stored_filename', models.CharField(max_length=255)),
                ('extension', models.CharField(max_length=4)),
                ('file_size', models.BigIntegerField()),
            ],
            options={
                'db_table': 'learning_material',
            },
        ),
    ]
