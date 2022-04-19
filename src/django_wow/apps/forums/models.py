from django.db import models

from apps.core.models import user_directory_path


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    prev = models.ForeignKey('Board', on_delete=models.DO_NOTHING, related_name='previous_board')
    next = models.ForeignKey('Board', on_delete=models.DO_NOTHING, related_name='next_board')
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_created=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING)
    text = models.CharField('Display Text', max_length=30, blank=True)
    icon = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    fg_color = models.CharField(max_length=6, default='FFFFFF')
    bg_color = models.CharField(max_length=6, default='000000')
    corner_radius = models.PositiveSmallIntegerField(default=0)
    stroke_width = models.PositiveSmallIntegerField(default=5)
    fill = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Forum(models.Model):

    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    prev = models.ForeignKey('Forum', on_delete=models.DO_NOTHING, related_name='previous_forum')
    next = models.ForeignKey('Forum', on_delete=models.DO_NOTHING, related_name='next_forum')
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_created=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.board.name} - {self.name}"


class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.DO_NOTHING)
    comment = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_created=True)
    is_active = models.BooleanField(default=False)
    replies = models.ManyToManyField('Post')
