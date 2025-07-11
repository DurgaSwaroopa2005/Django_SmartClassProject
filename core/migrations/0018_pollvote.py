# Generated by Django 3.2.25 on 2025-07-06 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_poll_polloption'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.poll')),
                ('selected_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.polloption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'poll')},
            },
        ),
    ]
