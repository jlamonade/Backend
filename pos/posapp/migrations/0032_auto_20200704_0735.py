# Generated by Django 3.0.7 on 2020-07-04 07:35
from datetime import datetime

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid

zero_id = uuid.UUID('00000000-0000-0000-0000-000000000000')


def create_default(apps, schema_editor):
    User = apps.get_model('posapp', 'User')
    Account = apps.get_model('posapp', 'Account')
    Transaction = apps.get_model('posapp', 'Transaction')

    default_account = Account(name="DEFAULT ACCOUNT IN CZK", currency_id=203)
    default_account.save()

    default_transaction = Transaction(
        id=zero_id,
        account=default_account,
        amount=0,
        created_by=User.objects.first(),
        timestamp=datetime.now())
    default_transaction.save()


def to_transactions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'contenttype')
    StateLog = apps.get_model('django_fsm_log', 'StateLog')
    User = apps.get_model('posapp', 'User')
    Account = apps.get_model('posapp', 'Account')
    Transaction = apps.get_model('posapp', 'Transaction')
    Expense = apps.get_model('posapp', 'Expense')
    TillMoneyCount = apps.get_model('posapp', 'TillMoneyCount')
    PaymentMethod = apps.get_model('posapp', 'PaymentMethod')
    TillEdit = apps.get_model('posapp', 'TillEdit')

    default_account = Account.objects.first()

    PaymentMethod.objects.all().update(account=default_account)

    expenses = Expense.objects.all()
    for expense in expenses:
        if expense.state == "paid":
            log = StateLog.objects.filter(
                content_type=ContentType.objects.get_for_model(expense),
                object_id=expense.id
            ).order_by('timestamp').last()
            expense.transaction = Transaction(
                account=default_account,
                amount=-expense._amount,
                created_by=log.by,
                timestamp=log.timestamp
            )
            expense.transaction.save()
            expense.save()

    counts = TillMoneyCount.objects.all()
    for count in counts:
        if count.till.state == "C":
            count.transaction = Transaction(
                account=count.paymentMethod.account,
                amount=count._amount,
                created_by=count.till.countedBy or User.objects.first(),
                timestamp=count.till.countedAt
            )
            count.transaction.save()
            count.save()

    edits = TillEdit.objects.all()
    for edit in edits:
        edit.transaction = Transaction(
            account=default_account,
            amount=edit.amount,
            created_by=edit.count.till.countedBy or User.objects.first(),
            timestamp=edit.created
        )
        edit.transaction.save()
        edit.save()

    Transaction.objects.get(id=zero_id).delete()


def to_amount(apps, schema_editor):
    Expense = apps.get_model('posapp', 'Expense')
    TillMoneyCount = apps.get_model('posapp', 'TillMoneyCount')
    TillEdit = apps.get_model('posapp', 'TillEdit')

    expenses = Expense.objects.all()
    for expense in expenses:
        if expense.state == "paid":
            expense._amount = -expense.transaction.amount
            expense.save()

    counts = TillMoneyCount.objects.all()
    for count in counts:
        if count.till.state == "C":
            count._amount = count.transaction.amount
            count.save()

    edits = TillEdit.objects.all()
    for edit in edits:
        edit.amount = edit.transaction.amount,
        edit.save()


class Migration(migrations.Migration):

    dependencies = [
        ('posapp', '0031_member_squashed_0032_member_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('currency', models.ForeignKey(limit_choices_to={'enabled': True}, on_delete=django.db.models.deletion.PROTECT, to='posapp.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=3, max_digits=15)),
                ('timestamp', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='posapp.Account')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(code=create_default, reverse_code=migrations.RunPython.noop),
        migrations.AddField(
            model_name='paymentmethod',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='posapp.Account'),
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='amount',
            new_name='_amount',
        ),
        migrations.RenameField(
            model_name='tillmoneycount',
            old_name='amount',
            new_name='_amount',
        ),
        migrations.AddField(
            model_name='expense',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='posapp.Transaction'),
        ),
        migrations.AddField(
            model_name='tillmoneycount',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='posapp.Transaction'),
        ),
        migrations.AddField(
            model_name='tilledit',
            name='transaction',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='posapp.Transaction'),
            preserve_default=False,
        ),
        migrations.RunPython(code=to_transactions, reverse_code=to_amount),
        migrations.AlterField(
            model_name='paymentmethod',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='posapp.Account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='tilledit',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='tilledit',
            name='created',
        ),
    ]
