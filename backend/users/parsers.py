import json

from services.custom_parsers import CustomMultiParser
from users.models import User


class UserMultiParser(CustomMultiParser):

    @staticmethod
    def decode_nested(decoded_data: dict) -> dict:
        print(decoded_data)
        user_type = decoded_data.get('type', User.UserType.CUSTOMER)
        nested_decoded_data = decoded_data[user_type]
        if not nested_decoded_data.startswith('{') and nested_decoded_data.endswith('}'):
            return decoded_data

        decoded_data[user_type] = json.loads(nested_decoded_data)
        return decoded_data
