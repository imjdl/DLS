from django.db import models

# Create your models here.


class Log(models.Model):

    IP = models.CharField(max_length=15)
    qtype = models.CharField(max_length=10)
    text = models.TextField()
    recvdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.IP + ':::' + self.text + ':::' + self.recvdate.strftime('%Y-%m-%d %H:%M:%S')
