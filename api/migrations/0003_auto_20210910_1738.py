# Generated by Django 3.2.6 on 2021-09-10 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='Vuyisile Ndlovu', max_length=120),
            preserve_default=False,
        ),
    ]