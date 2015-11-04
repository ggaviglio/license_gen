import requests
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.backends import ModelBackend
from django_project.settings import AUTH_INFORMATION
from dateutil.parser import parse
from datetime import timedelta
import json
import logging
logger = logging.getLogger(__name__)

OKTA_INFORMATION = AUTH_INFORMATION['OKTA']


class OKTABackend(ModelBackend):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, username=None, password=None):
        logger.info("Beginning login for {}".format(username))
        is_valid = False
        headers = {
            'Authorization': 'SSWS {}'.format(OKTA_INFORMATION['API_TOKEN']),
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
        authentication_payload = {
            'username': username,
            'password': password
        }
        r = requests.post(
            OKTA_INFORMATION['IDP_MEGADATA'],
            headers=headers,
            data=json.dumps(authentication_payload)
        )
        try:
            r.raise_for_status()
            is_valid = True
            logger.info("({}) authentication successful".format(username))

        except:
            logger.warn("({}) authentication not successful".format(username))

        if is_valid:
            content = json.loads(r.content.decode('utf-8'))
            user_information = content['_embedded']['user']['profile']
            session_expiry = parse(content['expiresAt'])
            django_session_expiry = session_expiry + timedelta(hours=1)
            exact_username = user_information['login']
            first_name = user_information['firstName']
            last_name = user_information['lastName']
            try:
                user = User.objects.get(username__exact=exact_username)
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                # user.email = email
                user.last_login = timezone.now()
                user.save()
                logger.info("({}) logged in.".format(username))
            except User.DoesNotExist:
                user = User()
                user.username = exact_username
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                # user.email = email
                user.last_login = timezone.now()
                user.save()
                logger.info("({}) logged in - initial.".format(username))
            return user
        else:
            # login failed
            logger.error("({}) login failed.".format(username))
            return None
