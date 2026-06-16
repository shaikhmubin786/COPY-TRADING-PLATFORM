from models import BrokerEnum

class BrokerService:

    def encrypt_secret(self, value):
        return value

    def decrypt_secret(self, value):
        return value

    async def validate_credentials(
        self,
        broker,
        api_key,
        api_secret,
        access_token
    ):
        return True, "Valid"

    async def test_connection(
        self,
        broker,
        api_key,
        api_secret,
        access_token
    ):
        return True, "Connected", "Valid", "Connection Success"

    async def refresh_session(
        self,
        broker,
        api_key,
        api_secret,
        access_token
    ):
        return True, "Refreshed", access_token

broker_service = BrokerService()