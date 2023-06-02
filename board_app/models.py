from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader import fields


class Post(models.Model):
    tanks = 'Танки'
    hills = 'Хиллы'
    dd = 'ДД'
    traders = 'Торговцы'
    gildsmasters = 'Гилдмастеры'
    questgilvers = 'Квестгиверы'
    blacksmiths = 'Кузнецы'
    tanners = 'Кожевники'
    potions_makers = 'Зельевары'
    spell_masters = 'Мастера заклинаний'

    CATEGORY_TYPES = [
        (tanks, 'Танки'),
        (hills, 'Хиллы'),
        (dd, 'ДД'),
        (traders, 'Торговцы'),
        (gildsmasters, 'Гилдмастеры'),
        (questgilvers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (traders, 'Кожевники'),
        (potions_makers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),
    ]

    header = models.CharField(max_length=25)
    content = fields.RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=CATEGORY_TYPES)
    time = models.DateTimeField(auto_now_add=True)


class PostResponses(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accept = models.BooleanField(default=False)


class Email(models.Model):
    text = models.TextField()
