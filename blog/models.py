from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата публикации")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    image = models.ImageField(upload_to='static/blog/images/', default='static/blog/images/post_default.png', verbose_name='Фото')
    fk_tag = models.ManyToManyField("Tag")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    fk_post = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Comment(models.Model):
    image = models.ImageField(upload_to='static/blog/images/comment/', default='static/blog/images/post_default.png')
    title = models.CharField(max_length=30)
    published_date = models.DateTimeField(auto_created=True)
    content = models.TextField()
    fk_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)