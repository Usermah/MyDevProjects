from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Project, Resume

import os
from dotenv import load_dotenv
import resend

load_dotenv()
resend.api_key = os.environ.get("RESEND_API_KEY")

def home(request):
    projects = Project.objects.all().order_by('-created_at')
    resume = Resume.objects.first()
    return render(request, 'home.html', {'projects': projects, 'resume': resume})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Admin email content
            full_message = f"""
                <h3>New Message from Portfolio Contact Form</h3>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong><br>{message}</p>
            """

            try:
                # Only send to admin
                resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": ["usamaibrahim737@gmail.com"],
                    "subject": subject,
                    "html": full_message
                })

                messages.success(request, "Message sent successfully!")

            except Exception as e:
                print("Email sending error:", e)
                messages.error(request, "Failed to send email. Try again later.")

            return redirect('contact')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def about(request):
    return render(request, 'about.html')
