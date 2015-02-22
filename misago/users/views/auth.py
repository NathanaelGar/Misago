from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.utils.six.moves.urllib.parse import urlparse

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from misago.core.embercli import is_ember_cli_request


@sensitive_post_parameters()
@never_cache
@csrf_protect
def login(request):
    if request.method == 'POST':
        redirect_to = request.POST.get('redirect_to')
        if redirect_to:
            is_redirect_safe = is_safe_url(
                url=redirect_to, host=request.get_host())

            if not is_redirect_safe and is_ember_cli_request(request):
                parsed_url = urlparse(settings.MISAGO_EMBER_CLI_ORIGIN)
                trusted_host = '%s:%s' % (parsed_url.hostname, parsed_url.port)
                is_redirect_safe = is_safe_url(
                    url=redirect_to, host=trusted_host)

            if is_redirect_safe:
                redirect_to_path = urlparse(redirect_to).path
                return redirect(redirect_to_path)
    return redirect(settings.LOGIN_REDIRECT_URL)


@never_cache
@csrf_protect
def logout(request):
    if request.method == 'POST' and request.user.is_authenticated():
        auth.logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)
