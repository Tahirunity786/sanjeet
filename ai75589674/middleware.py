from django.core.cache import cache
from django.http import HttpResponseForbidden

from ai75589674.models import TrafficData

class ContactRateLimitMiddleware:
    def __init__(self, get_response, limit_count=5, time_window=60 * 60):  # 5 submissions per hour by default
        self.get_response = get_response
        self.limit_count = limit_count
        self.time_window = time_window

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        key = f"contact_rate_limit_{ip_address}"
        count = cache.get(key, 0)
        if count >= self.limit_count:
            return HttpResponseForbidden("Our team will contact you soon. Be patient!")

        # Increment the count and set the cache expiration
        count += 1
        cache.set(key, count, self.time_window)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# traffic_middleware.py
from django.utils import timezone
from datetime import datetime

class TrafficMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_request(request)
        return response

    def process_request(self, request):
        if not request.user.is_authenticated:
            last_visit_str = request.session.get('last_visit')
            current_time = timezone.now()

            if last_visit_str:
                last_visit = timezone.make_aware(datetime.strptime(last_visit_str, '%Y-%m-%dT%H:%M:%S.%fZ'))
                if (current_time - last_visit).seconds > 300:  # Adjust the time threshold as needed
                    request.session['is_old_user'] = True
                else:
                    request.session['is_old_user'] = False
            else:
                request.session['is_old_user'] = False

            request.session['last_visit'] = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            # Save traffic data to the database
            TrafficData.objects.create(
                device_info=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=self.get_client_ip(request),
                visit_timestamp=current_time,
                is_old_user=request.session['is_old_user']
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
