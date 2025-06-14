from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project, Resume
from .forms import ContactForm


def home(request):
    projects = Project.objects.all().order_by('-created_at')
    resume = Resume.objects.first()  
    return render(request, 'home.html', {'projects': projects, 'resume': resume})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the message to database
            form.save()

            # Send email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Message from {name} <{email}>:\n\n{message}"

            try:
                send_mail(subject, full_message, email, ['usamaibrahim737@gmail.com']) 
                messages.success(request, "Message sent successfully!")
            except:
                messages.error(request, "Failed to send email. Please try again later.")

            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
