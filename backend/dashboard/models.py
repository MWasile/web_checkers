from django.contrib.auth import get_user_model
from django.db import models


class UserRank(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    elo = models.IntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Name:{self.user.username}, ELO: {self.elo}'


class UserFriendList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    friends = models.ManyToManyField(get_user_model(), related_name='friends')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Friends of {self.user.username}'


class GlobalRank(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    elo = models.IntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-elo']

    def get_top_5(self):
        return self.objects.all()[:5]

    def can_challenge(self, user):
        min_elo_in_top = self.get_top_5()
        if not user.elo >= min(min_elo_in_top, key=lambda user_: user_.elo):
            return False
        return True

    def __str__(self):
        return f'Top players: {self.user.username}'


class UsersChat(models.Model):
    message_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='friend')

    messages = models.ManyToManyField('Message', related_name='messages')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Chats between {self.message_from.username} and {self.message_to.username}'


class Message(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Message: {self.message[:10]}...'
