# Adds admin approval status to submitted timesheets.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_timesheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
