from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

URGENCY_CHOICES=[(x,x) for x in range(1,11)]
TICKET_TYPE_CHOICES=[
('Service Request', 'Service Request'),
('Incident', 'Incident'),
('Problem', 'Problem'),
('Change Request',' Change Request'),
]

# Model for a ticket
class Ticket(models.Model):
    title = models.CharField(max_length = 100)
    ticket_type = models.CharField(max_length = 15, choices = TICKET_TYPE_CHOICES, default = 'Service Request')
    urgency = models.IntegerField(choices = URGENCY_CHOICES, default = 1)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})


