import boto3
import hmac
import hashlib
import base64
from botocore.exceptions import ClientError

def get_secret_hash(username, client_id, client_secret):
    """Calculate the secret hash for Cognito authentication"""
    message = username + client_id
    dig = hmac.new(
        client_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def create_cognito_user_and_get_token(user_pool_id, client_id, client_secret, username="testuser", password="TempPass123!"):
    """Create a user in Cognito and get an access token"""
    cognito_client = boto3.client('cognito-idp', region_name='us-west-2')
    
    try:
        # Create user
        cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            TemporaryPassword=password,
            MessageAction='SUPPRESS'
        )
        
        # Set permanent password
        cognito_client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True
        )
        print(f"✓ Created user: {username}")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            print(f"✓ User {username} already exists")
        else:
            print(f"Error creating user: {e}")
            return None
    
    try:
        # Authenticate and get tokens
        secret_hash = get_secret_hash(username, client_id, client_secret)
        
        response = cognito_client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': secret_hash
            }
        )
        
        access_token = response['AuthenticationResult']['AccessToken']
        print(f"✓ Got access token for user: {username}")
        return access_token
        
    except ClientError as e:
        print(f"Error authenticating user: {e}")
        return None