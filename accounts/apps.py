from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    # Iporting our user signal
    def ready(self):
    	import accounts.mysignal
