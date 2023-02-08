from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
	# One-to-One relationship means that a user can only have one customer and customer can only have one user
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def _str__(self):
		return self.name
