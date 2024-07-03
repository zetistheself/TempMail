import requests
import random
import string


class Mail():
    def __init__(self):
        self.ready_domains = []
        self.address = None
        self.password = None
    
    def check_connection(self) -> int:
        """
        Checks the connection to the Mail.tm API.
        """
        try:
            r = requests.get('https://api.mail.tm')
            return r.status_code
        except Exception as e:
            print(e)
        return r.status_code
    
    def get_domains(self) -> list:
        """
        Returns a list of all domains that the user has access to.

        Returns:
            list: A list of all domains that the user has access to.
        """
        try:
            r = requests.get('https://api.mail.tm/domains')
            self.ready_domains = [domain["domain"] for domain in r.json()["hydra:member"]]
            return self.ready_domains
        except Exception as e:
            print(e)
    
    def create_account(self, domain=None, address=None, password=None) :
        if domain is None:
            self.get_domains()
            domain = self.ready_domains[random.randrange(0, len(self.ready_domains))]
        if address is None:
            address = "".join(random.choice(string.ascii_lowercase) for i in range(random.randrange(5, 13)))
        if password is None:
            password = "".join(random.choice(string.ascii_lowercase) for i in range(random.randrange(8, 15)))
        try:
            r = requests.post('https://api.mail.tm/accounts', json={
                "address": address + "@" + domain,
                "password": password,
            })
            self.address = address + "@" + domain
            self.password = password
            return r.json()["id"]
        except Exception as e:
            print(e)
        return r.status_code

    def me(self, token):
        """
        Retrieves the authenticated user.

        Args:
            token (str): The authentication token.

        Returns:
            dict: The authenticated user.
        """
        try:
            r = requests.get(
                "https://api.mail.tm/me",
                headers={"authorization": f"Bearer {token}"},
            )
            return r.json()
        except Exception as e:
            print(e)
        return r.status_code
    
    def get_token(self, address, password):
        """
        Gets a token for the given email address and password.

        Args:
            address (str): The email address of the account.
            password (str): The password of the account.

        Returns:
            str: The token for the account.
        """
        try:
            r = requests.post('https://api.mail.tm/token', json={
                "address": address,
                "password": password,
            })
            return r.json()["token"]
        except Exception as e:
            print(e)
        return r.status_code
    
    def get_messages(self, token):
        """
        Retrieves all messages for the authenticated user.

        Args:
            token (str): The authentication token.

        Returns:
            list: A list of messages.
        """
        try:
            r = requests.get(
                "https://api.mail.tm/messages",
                headers={"authorization": f"Bearer {token}"},
            )
            return r.json()["hydra:member"]
        except Exception as e:
            print(e)
            return []
    
    def get_message(self, token, message_id):
        """
        Retrieves a message for the authenticated user.

        Args:
            token (str): The authentication token.
            message_id (str): The ID of the message.

        Returns:
            dict: The message.
        """
        try:
            r = requests.get(
                f"https://api.mail.tm/messages/{message_id}",
                headers={"authorization": f"Bearer {token}"},
            )
            return r.json()
        except Exception as e:
            print(e)
            return {}
    
    def delete_message(self, token, message_id):
        """
        Deletes a message for the authenticated user.

        Args:
            token (str): The authentication token.
            message_id (str): The ID of the message.
        """
        try:
            r = requests.delete(
                f"https://api.mail.tm/messages/{message_id}",
                headers={"authorization": f"Bearer {token}"},
            )
            return r.status_code
        except Exception as e:
            print(e)
            return r.status_code
    
    def mark_as_read(self, token, message_id):
        """
        Marks a message as read.

        Args:
            token (str): The authentication token.
            message_id (str): The ID of the message.
        """
        try:
            r = requests.patch(
                f"https://api.mail.tm/messages/{message_id}",
                headers={"authorization": f"Bearer {token}"},
            )
            return r.status_code
        except Exception as e:
            print(e)
            return r.status_code
    
    def get_message_html(self, token, message_id) -> string: 
        """
        Retrieves the HTML content of a message.

        Args:
            token (str): The authentication token.
            message_id (str): The ID of the message.

        Returns:
            str: The HTML content of the message.
        """
        try:
            r = requests.get(
                f"https://api.mail.tm/messages/{message_id}",
                headers={"authorization": f"Bearer {token}"},
            )
            html = r.json()['html']
            return html[0].replace("&lt;", "<").replace("&gt;", ">")
        except Exception as e:
            print(e)
            return ""