# Generated manually to set user field to non-nullable

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stool', '0003_stoolrecord_user'),
    ]

    operations = [
        migrations.RunSQL(
            # Provide a SQL statement to update any NULL values in 'user' column with a default user ID
            # You should replace '1' with the ID of your default user
            # This assumes that you have at least one user in your database
            sql="UPDATE stool_stoolrecord SET user_id = (SELECT id FROM auth_user LIMIT 1) WHERE user_id IS NULL;",
            reverse_sql="",  # No reverse operation needed
        ),
        migrations.AlterField(
            model_name='stoolrecord',
            name='user',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, related_name='stool_records', to=settings.AUTH_USER_MODEL),
        ),
    ]