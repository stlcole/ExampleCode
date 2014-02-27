from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.template.defaultfilters import slugify


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

    email = models.EmailField(
        max_length=254,
        verbose_name='login email address',
        unique=True, db_index=True
    )
    email_backup = models.EmailField(max_length=254, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ParticipantManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_absolute_url(self):
        return reverse('participant-profile', kwargs={'pk': self.pk})


class Profile(models.Model):
    participant = models.OneToOneField(Participant, editable=False)
    first_name = models.CharField(
        max_length=30,
        verbose_name='common first name',
    )
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    slug = models.SlugField(null=True, blank=True, editable=False)

    def __unicode__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            name = """{} {}""".format(self.first_name, self.last_name)
            self.slug = slugify(name)

        if not self.formal_name:
            self.formal_name = "{} {}".format(self.first_name, self.last_name)

        super(Profile, self).save()