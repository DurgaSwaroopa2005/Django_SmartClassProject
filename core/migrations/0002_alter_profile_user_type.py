
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], max_length=10),
        ),
    ]