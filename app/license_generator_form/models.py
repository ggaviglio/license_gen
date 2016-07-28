from django.db import models

# Create your models here.
class License(models.Model):
	release_key = models.TextField(default='')
	notes = models.TextField(default='')
	external_id = models.TextField(default='')
	external_id_type = models.TextField(default='')
	license_type = models.TextField(default='')
	account_holder = models.TextField(default='')
	expiry_days = models.IntegerField(null=True)
	max_users = models.IntegerField(null=True)
	no_heartbeat = models.BooleanField(default=False)
	heartbeat_url = models.TextField(default='')
	clustering_enabled = models.BooleanField(default=False)
	license_group = models.TextField(default='')
	expiry_date = models.TextField(default='')
	max_docs = models.IntegerField(null=True)
	cloud_sync = models.BooleanField(default=False)
	server_end_date = models.TextField(default='')
	crypto_doc = models.BooleanField(default=False)
