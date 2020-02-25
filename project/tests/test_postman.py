from email.mime.multipart import MIMEMultipart

from postman import _prepare_email


class TestPostman:

    def test_prepare_email__email_str__mime_object(self):
        test_email_str = '''
            <!DOCTYPE html>
            <html><body><p>Test email</p></body></html>
        '''

        message_obj = _prepare_email(test_email_str)

        assert isinstance(message_obj, MIMEMultipart)
