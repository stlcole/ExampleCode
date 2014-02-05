from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, UserManager


class ParticipantManager(UserManager):
    def create_user(self, email, password, email_backup=None):
        if not email:
            raise ValueError('You need an email address')

        user = self.model(
            email=ParticipantManager.normalize_email(email),
        )

        if email_backup:
            user.email_backup = ParticipantManager.normalize_email(email_backup)

        user.set_password(password)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, email_backup=None):
        user = self.create_user(email,
                                password=password,
        )

        if email_backup:
            user.email_backup = ParticipantManager.normalize_email(email_backup)

        user.is_admin = True
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save(using=self._db)
        return user


class Participant(AbstractBaseUser):
    """
    Custom BaseUser model derived from django.contrib.auth.models.AbstractBaseUser.
    Based on unique email address rather than 'username'.
    Used for validation purposes. Does not contain any 'profile' information.
    User profile information contained in the model -- MyUserProfile.
    """

    email = models.EmailField(max_length=254, unique=True, db_index=True)
    email_backup = models.EmailField(max_length=254, null=True, blank=True)
    # registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ParticipantManager()

    USERNAME_FIELD = 'email'