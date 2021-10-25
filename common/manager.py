from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, mobile1, password=None, **extra_fields):
        if not mobile1:
            raise ValueError('Mobile is require')

        user = self.model(mobile1=mobile1, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile1, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Must be superuser')

        return self.create_user(mobile1, password, **extra_fields)


