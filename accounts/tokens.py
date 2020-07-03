from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


"""PasswordResetTokenGenerator is generating a token without persisting 
it in the database so, we extended it to create a unique 
token generator to confirm registration or email address
This is a secured and reliable method"""

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        user_id = six.text_type(user.pk)
        ts = six.text_type(timestamp)
        is_active = six.text_type(user.is_active)
        return f"{user_id}{ts}{is_active}"

account_activation_token = AccountActivationTokenGenerator()