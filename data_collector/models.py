import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Search(models.Model):
    fields = ("id","user_id")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #todo add registration
    #user_id = models.CharField('UserId', max_length=50, default = "dfasd")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField('Name', max_length=50, default = "NewSearch")
    link = models.TextField('Link')
    date = models.DateTimeField('Date of search', auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/searches/{self.id}'
    
    def link_lines(self):
        return [el.strip() for el in self.link.split('\n')]
    
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    class Meta:
        verbose_name = 'Search'
        verbose_name_plural = 'Searches'
