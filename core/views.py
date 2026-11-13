import logging
import smtplib

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from core.forms import ContactMessageForm


logger = logging.getLogger(__name__)


def page(request, template_name):
    context = {}
    if template_name == "contact.html":
        context["contact_sent"] = request.GET.get("sent") == "1"
    return render(request, template_name, context)


@require_POST
def submit_contact(request):
    form = ContactMessageForm(request.POST)
    if not form.is_valid():
        return HttpResponse(
            "Please check your name, email, subject, and message, then try again.",
            status=400,
            content_type="text/plain",
        )

    contact_message = form.save()
    email = EmailMessage(
        subject="New portfolio contact message",
        body=(
            f"Name: {contact_message.name}\n"
            f"Email: {contact_message.email}\n"
            f"Subject: {contact_message.subject}\n\n"
            f"{contact_message.message}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECIPIENT],
        reply_to=[contact_message.email],
    )
    try:
        sent = email.send(fail_silently=False)
    except (OSError, smtplib.SMTPException):
        logger.exception(
            "Email notification failed for contact message %s.",
            contact_message.pk,
        )
        return HttpResponse(
            "Your message was saved, but its email notification could not be sent. "
            "Please contact us directly if you need an immediate reply.",
            status=503,
            content_type="text/plain",
        )
    if sent != 1:
        logger.error(
            "Email notification was not sent for contact message %s.",
            contact_message.pk,
        )
        return HttpResponse(
            "Your message was saved, but its email notification could not be sent. "
            "Please contact us directly if you need an immediate reply.",
            status=503,
            content_type="text/plain",
        )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return HttpResponse("OK", content_type="text/plain")
    return redirect("/contact.html?sent=1")
