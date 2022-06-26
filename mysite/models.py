from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    task=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task


class Contact(models.Model):
    fio=models.CharField(max_length=250,verbose_name='Ism,Familiya,Otasining ismi')
    email=models.EmailField(default='example@gmail.com',verbose_name='Elektron pochta',help_text='Elektron pochtangizni kiriting')
    topic=models.CharField(max_length=100,verbose_name='Mavzu')
    message=models.TextField(verbose_name='Xabar',help_text='Xabarni kiriting')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic
    class Meta:
        verbose_name_plural='Kelib tushgan xabarlar'

