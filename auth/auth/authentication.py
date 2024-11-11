from ldap3 import Server, Connection, ALL


# Define LDAP server details and base OU
LDAP_SERVER = "ldap://winserver2022.devapp.local:389"
BASE_OU = "OU=IT_NOC,DC=devapp,DC=local"

def authenticateX(username, password):
    """Attempts to authenticate a user within a specific OU."""
    user_dn = f"CN={username},{BASE_OU}"
    server = Server(LDAP_SERVER, get_info=ALL)
    try:
        conn = Connection(server, user=user_dn, password=password)
        if conn.bind():
            conn.unbind()
            return True
        return False
    except Exception as e:
        # Catch all exceptions and provide a generic error message
        return "Can't connect to server to validate user or an unexpected error occurred."


def authenticate(username, password):
    """Simulates LDAP authentication for testing purposes."""
    # Hardcoded credentials for testing
    fixed_username = "admin"
    fixed_password = "123456"
    
    # Check if provided credentials match the fixed ones
    if username == fixed_username and password == fixed_password:
        return True
    else:
        return False