from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):
        """Creates and saves a new User"""
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Transactions(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    description = models.TextField()
    waiting = models.BooleanField()
    transaction_from = models.UUIDField(null=True)
    transaction_to = models.UUIDField(null=True)


class Wallet(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    transactions = models.ManyToManyField(Transactions)


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    text = models.TextField()
    created_at = models.DateTimeField()
    last_edit = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Organization(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    name = models.CharField(max_length=20, null=True, blank=True)
    users = models.ManyToManyField(User)
    wallet = models.ForeignKey(Wallet, to_field='uuid', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY = (
        ('height', 'height'), ('normal', 'normal'), ('low', 'low')
    )
    STATUSES = (
        ('wait', 'Waiting to accept'), ('work', 'Not finished'), ('finished', 'Finished')
    )
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    name = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    priority = models.CharField(max_length=200, choices=PRIORITY)
    time_limit = models.DateTimeField()
    users = models.ManyToManyField(User)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=200, choices=STATUSES)
    comments = models.ManyToManyField(Comment)

    def __str__(self):
        return self.name


class SubTask(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    time_limit = models.DateTimeField()
    users = models.ManyToManyField(User)
    task = models.ForeignKey(Task, to_field='uuid', on_delete=models.CASCADE, null=True)
    comments = models.ManyToManyField(Comment)

    def __str__(self):
        return self.name


class Note(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=20, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField()
    last_edit = models.DateTimeField()
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
