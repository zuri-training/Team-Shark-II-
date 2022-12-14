# Generated by Django 4.1.4 on 2022-12-14 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_comment_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reel',
            name='category',
        ),
        migrations.AddField(
            model_name='reel',
            name='category',
            field=models.ForeignKey(help_text='choose a category for your short video', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='video category'),
        ),
    ]