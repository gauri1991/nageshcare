"""
Email utility functions for sending inquiry replies
"""
from django.core.mail import EmailMessage, get_connection
from django.conf import settings as django_settings
from cms.models import SiteSettings
from .models import InquiryReply, ContactMessage, QuoteRequest


def get_email_config():
    """
    Retrieve email configuration from CMS SiteSettings
    Returns a dictionary with email settings
    """
    try:
        site_settings = SiteSettings.objects.get(pk=1)

        # Check if email settings are configured
        if not site_settings.email_host_user or not site_settings.email_host:
            return None

        return {
            'host': site_settings.email_host,
            'port': site_settings.email_port,
            'username': site_settings.email_host_user,
            'password': site_settings.email_host_password,
            'use_tls': site_settings.email_use_tls,
            'signature': site_settings.email_reply_signature,
        }
    except SiteSettings.DoesNotExist:
        return None


def send_inquiry_reply(
    inquiry_type,
    inquiry_id,
    subject,
    message,
    replied_by_user=None,
    attachment_file=None
):
    """
    Send an email reply to a contact message or quote request

    Parameters:
    - inquiry_type: 'contact' or 'quote'
    - inquiry_id: ID of the ContactMessage or QuoteRequest
    - subject: Email subject
    - message: Email message body
    - replied_by_user: User object of the person replying (optional)
    - attachment_file: File object to attach (optional)

    Returns:
    - Dictionary with success status and InquiryReply object
    """
    # Get email configuration
    email_config = get_email_config()

    if not email_config:
        return {
            'success': False,
            'error': 'Email settings not configured in CMS. Please configure SMTP settings first.',
            'reply_record': None
        }

    # Get the inquiry object
    contact_message = None
    quote_request = None
    recipient_email = None
    recipient_name = None

    if inquiry_type == 'contact':
        try:
            contact_message = ContactMessage.objects.get(pk=inquiry_id)
            recipient_email = contact_message.email
            recipient_name = contact_message.name
        except ContactMessage.DoesNotExist:
            return {
                'success': False,
                'error': 'Contact message not found',
                'reply_record': None
            }

    elif inquiry_type == 'quote':
        try:
            quote_request = QuoteRequest.objects.get(pk=inquiry_id)
            recipient_email = quote_request.email
            recipient_name = quote_request.name
        except QuoteRequest.DoesNotExist:
            return {
                'success': False,
                'error': 'Quote request not found',
                'reply_record': None
            }

    else:
        return {
            'success': False,
            'error': 'Invalid inquiry type. Must be "contact" or "quote"',
            'reply_record': None
        }

    # Add signature to message
    full_message = f"{message}\n\n{email_config['signature']}"

    # Create email connection
    connection = get_connection(
        host=email_config['host'],
        port=email_config['port'],
        username=email_config['username'],
        password=email_config['password'],
        use_tls=email_config['use_tls'],
        fail_silently=False,
    )

    # Create InquiryReply record (before sending)
    reply_record = InquiryReply(
        inquiry_type=inquiry_type,
        contact_message=contact_message,
        quote_request=quote_request,
        reply_from=email_config['username'],
        reply_to=recipient_email,
        reply_subject=subject,
        reply_message=full_message,
        replied_by=replied_by_user,
        email_sent_successfully=False,
    )

    # Handle attachment if provided
    if attachment_file:
        reply_record.attachment = attachment_file

    # Save reply record (will have email_sent_successfully=False initially)
    reply_record.save()

    # Try to send email
    try:
        email = EmailMessage(
            subject=subject,
            body=full_message,
            from_email=email_config['username'],
            to=[recipient_email],
            connection=connection,
        )

        # Attach file if provided and already saved
        if attachment_file and reply_record.attachment:
            email.attach_file(reply_record.attachment.path)

        # Send the email
        email.send()

        # Update reply record as successful
        reply_record.email_sent_successfully = True
        reply_record.save()

        # Mark contact message as read if it's a contact inquiry
        if contact_message:
            contact_message.is_read = True
            contact_message.save()

        return {
            'success': True,
            'error': None,
            'reply_record': reply_record,
            'recipient': recipient_name,
            'recipient_email': recipient_email
        }

    except Exception as e:
        # Update reply record with error
        reply_record.error_message = str(e)
        reply_record.save()

        return {
            'success': False,
            'error': f'Failed to send email: {str(e)}',
            'reply_record': reply_record
        }


def test_email_configuration():
    """
    Test if email configuration is valid
    Returns tuple: (is_valid, error_message)
    """
    email_config = get_email_config()

    if not email_config:
        return (False, "Email settings not configured in CMS")

    try:
        connection = get_connection(
            host=email_config['host'],
            port=email_config['port'],
            username=email_config['username'],
            password=email_config['password'],
            use_tls=email_config['use_tls'],
            fail_silently=False,
        )
        connection.open()
        connection.close()
        return (True, "Email configuration is valid")
    except Exception as e:
        return (False, f"Email configuration error: {str(e)}")
