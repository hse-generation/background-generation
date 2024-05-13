from django.db import models


class Users(models.Model):
    name = models.CharField("Имя", max_length=10000, null=True, default="User")
    client_id = models.CharField("ID клиента", max_length=10000, null=True)
    status = models.IntegerField("Статус активности", null=True, default=1)
    api_key = models.CharField("Ключ", null=True, max_length=50)
    password = models.CharField("Пароль", max_length=10000, null=True)
    email = models.EmailField("Почта", max_length=10000, null=True)
    profile_picture = models.ImageField(upload_to='avatars', null=True, blank=True, default="avatars/avatar.jpg")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"
        db_table = "accounts"



