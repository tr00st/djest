from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.core import mail
from django.http.response import HttpResponseRedirect

from uuid import uuid4
from bs4 import BeautifulSoup
import json


class BaseCase(TestCase, dict):

    def __init__(self, *args, **kwargs):
        super(BaseCase, self).__init__(*args, **kwargs)

    def assert_redirect_to(self, part):
        self.assertTrue(
            isinstance(self.response, HttpResponseRedirect)
        )
        self.assertTrue(
            part in self.response.url
        )
        
    def assert_mail_count(self, n):
        self.assertEqual(len(mail.outbox), n)
        
    def reverse(self, *args, **kwargs):
        return reverse_lazy(*args, **kwargs)

    def content(self):
        content = None
        if hasattr(self.response, 'rendered_content'):
            content = self.response.rendered_content
        elif hasattr(self.response, 'content'):
            content = self.response.content
        return content
        
    def json(self):
        try:
            return json.loads(self.content())
        except:
            return None
        
    def wout(self):
        '''
        Write out the current response's rendered_content
        to a file in /tmp/out.html TODO: Use temporary
        builtin python module.
        '''
        content = self.content()
        
        self.debug(content)
        if content:
            with open('/tmp/out.html', 'w') as f:
                f.write(content.encode('utf8'))

    def debug(self, message):
        '''
        Utility method for debugging. Make sure
        settings.TEST_DEBUG is defined and set to
        True. When used, self.debug_buffer will contain
        concatinated debug messages.
        '''
        if (not hasattr(settings, 'TEST_DEBUG')) or (
            not settings.TEST_DEBUG
        ):
            return
        if not hasattr(self, 'debug_buffer'):
            self.debug_buffer = ''
        try:
            message = BeautifulSoup(message).body.get_text()
        except:
            pass

        while '\n\n' in message:
            message = message.replace('\n\n', '\n')
            
        self.debug_buffer += (
             message +
            '\n------------------------------\n'
        )
        
    def nop(*args, **kwargs):
        # use for mocking
        # don't do anything
        pass
        
    def new(self, name, klass, m_kwargs ):
        if name in self:
            raise ValueError('Model already exists %s' % name)
        m = klass(**m_kwargs)
        m.save()
        self[name] = m
        return m

    def post(self, url, data):
        self.response = self.client.post(
            url,
            data,
            follow = True
        )

        if hasattr(
            self.response, 'context'
        ) and self.response.context:
        
            if 'errorlist' in self.response.context.keys():
                self.wout()
                raise Exception('Form did not validate?')

            if 'form' in self.response.context:
                if self.response.context['form']._errors:
                    self.wout()
                    raise Exception('Form did not validate?')

        return self.response

    def get(self, url):
        self.response = self.client.get(url)
        return self.response
    
    def uuid4(self):
        return uuid4().hex

    def assert_in_title(self, test):
        soup_title = BeautifulSoup(
            self.response.rendered_content
        ).title.get_text().lower()
        test = test.lower()
        if not test in soup_title:
            raise AssertionError('%s is not in %s' % (
                test,
                soup_title
            ))
        self.assertTrue(True)
