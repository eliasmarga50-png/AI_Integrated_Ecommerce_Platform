

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Custom User model for the AI Ecommerce platform.
    """
    objects=UserManager()

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        SELLER = "SELLER", "Seller"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(
        unique=True,
        help_text="User's unique email address."
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    def is_customer(self):
    	
    	"""
    	Return True if this user has the customer role
    	"""
    	return (
    	    self.is_authenticated and 
    	    self.role==self.Role.CUSTOMER
    	)
    	
    def is_seller(self):
    	"""
    	Return True if this user has the seller role
    	"""
    	return(
    	    self.is_authenticated and 
    	    self.role==self.Role.SELLER
    	)
    	
    def is_admin(self):
    	"""
    	Return True if the user has admin role
    	"""
    	return (
    	    self.is_authenticated and
    	    self.role==self.Role.ADMIN
    	)

    def __str__(self):
        return self.username