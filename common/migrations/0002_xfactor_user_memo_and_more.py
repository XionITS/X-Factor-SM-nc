# Generated by Django 4.0.3 on 2023-07-13 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='xfactor_user',
            name='memo',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='xfactor_userauth',
            name='xfactor_auth',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth', to='common.xfactor_auth'),
        ),
        migrations.AlterField(
            model_name='xfactor_userauth',
            name='xfactor_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='common.xfactor_user'),
        ),
    ]
