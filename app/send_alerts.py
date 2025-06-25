########################################
# app\send_alerts.py
########################################

from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Subscription

def send_subscription_alerts():
    """Send alerts to users who still have alerts remaining and an active subscription."""
    subscriptions = Subscription.objects.all()

    for subscription in subscriptions:
        if subscription.is_active():
            days_remaining = (subscription.get_end_date() - now()).days

            # Send expiry warning if 3 days left
            if days_remaining <= 3:
                message = f"Your subscription expires in {days_remaining} days. Renew now to continue receiving alerts."
                if subscription.email:
                    send_mail(
                        'Subscription Expiry Warning',
                        message,
                        'no-reply@yourapp.com',
                        [subscription.email],
                        fail_silently=True,
                    )

            # Send regular alerts if eligible
            if subscription.can_receive_alert():
                message = f"Your {subscription.package} subscription alert. You have {subscription.get_alert_limit() - subscription.alerts_sent} remaining."
                if subscription.email:
                    send_mail(
                        'Subscription Alert',
                        message,
                        'no-reply@yourapp.com',
                        [subscription.email],
                        fail_silently=True,
                    )

                subscription.alerts_sent += 1
                subscription.save()

                print(f"Sent alert to {subscription.email or subscription.phone_number}")
        else:
            print(f"Subscription expired or limit reached for {subscription.email or subscription.phone_number}")
