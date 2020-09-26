from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    location_fk = models.ForeignKey('scraping.Location',
                                    verbose_name='Город',
                                    on_delete=models.SET_NULL,
                                    blank=True,
                                    null=True)
    specialty_fk = models.ForeignKey('scraping.Specialty',
                                     verbose_name='Язык программирования',
                                     on_delete=models.SET_NULL,
                                     blank=True,
                                     null=True)
    email_field = models.EmailField(verbose_name='Адрес электронной почты',
                                    max_length=255,
                                    unique=True)
    is_subscriber = models.BooleanField(default=True, verbose_name='Подписка')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')

    objects = MyUserManager()

    USERNAME_FIELD = 'email_field'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email_field

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'
