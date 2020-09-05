from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    # Importing our user signal
    def ready(self):
    	import accounts.signals
