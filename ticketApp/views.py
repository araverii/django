from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Ticket
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Main page, instructs user to log in, contains list of tickets
# Navigation bar included, includes a dropdown menu where user can change profile details
def ticket_panel(request):
    context = {
        'tickets': Ticket.objects.all()
    }

    return render(request, 'ticketApp/ticket_panel.html', context)

# Creates a page where there is a table of the user's tickets. If an admin, can view all users' tickets.
# Sorts via urgency in descending order (10 being the most priority)
class TicketListView(ListView):
    model = Ticket
    template_name = 'ticketApp/ticket_panel.html'
    context_object_name = 'tickets'
    ordering = ['-urgency']

# A single, separate page containing details of the ticket, options for updating/deleting included
class TicketDetailView(DetailView):
    model = Ticket

# Ticket creation, where when a ticket is submitted, and email confirmation will be sent to the user.
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'ticket_type', 'urgency', 'description']
    template_name = 'ticketApp/write.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        message = f'We have received your ticket! Our staff will be in contact with you as soon as possible.'
        message+= f'\n\nTitle: {form.instance.title}'
        message+= f'\nUser: {form.instance.author}'
        message+= f'\nDate: {timezone.now()}'
        message+= f'\nType: {form.instance.ticket_type}'
        message+= f'\nUrgency: {form.instance.urgency}'
        message+= f'\nDescription: {form.instance.description}'
        message+= f'\n\nIf there are any additional information, please update your ticket in the ALG Helpdesk website or respond to this email.'
        message+= f'\n\nThank you, and have a good day!'
        send_mail(
            'Ticket has been received',
            message,
            settings.EMAIL_HOST_USER,
            [self.request.user.email],
            )
        return super().form_valid(form)

# Updates the ticket
class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['title', 'ticket_type', 'urgency', 'description']
    template_name = 'ticketApp/write.html'

    def form_valid(self,form):
        form.save()
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Deletes the ticket
class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'

    def test_func(self):
            post = self.get_object()
            if self.request.user == post.author:
                return True
            return False



