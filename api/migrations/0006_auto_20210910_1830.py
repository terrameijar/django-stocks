# Generated by Django 3.2.6 on 2021-09-10 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='div_cagr',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='div_yield',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='dividend',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='market_cap',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='next_ex_div_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='next_pay_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='payout_ratio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='sector',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]