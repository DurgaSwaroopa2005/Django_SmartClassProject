from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('Student', 'Student'), ('Teacher', 'Teacher')], max_length=10, null=True),
        ),
    ]