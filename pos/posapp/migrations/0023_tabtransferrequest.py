# Generated by Django 3.0.4 on 2020-04-19 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posapp', '0022_tab_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='TabTransferRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('requestedAt', models.DateTimeField(auto_now_add=True)),
                ('new_owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tab_transfers_gaining', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tab_transfers_requested', to=settings.AUTH_USER_MODEL)),
                ('tab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.Tab')),
            ],
        ),
    ]
