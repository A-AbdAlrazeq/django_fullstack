# Generated by Django 2.2.4 on 2023-06-23 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0005_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='exam_app.Team'),
            preserve_default=False,
        ),
    ]