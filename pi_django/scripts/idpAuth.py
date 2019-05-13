import oauth2 as oauth
import requests
import base64, random
import urllib.parse
import binascii
import time, collections, hmac, hashlib
import codecs
import json
import os
from urllib.parse import urlparse
from hashlib import sha1
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session


REQUEST_TOKEN_URL = 'http://identity.ua.pt/oauth/request_token'
ACCESS_TOKEN_URL = 'http://identity.ua.pt/oauth/access_token'
AUTHORIZATION_URL = 'http://identity.ua.pt/oauth/authorize'
GET_EMAIL_DATA_URL = 'http://identity.ua.pt/oauth/get_data?format=JSON&scope=uu'
GET_NAME_DATA_URL = 'http://identity.ua.pt/oauth/get_data?format=JSON&scope=name'


class UniversityOauth(object):


    oauth_token = None
    oauth_token_secret = None
    email = None
    is_authorized = False
    verifier = None


    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        '''
        Parameters:
            consumer_key: String
                - The consumer_key from registering application
                  on Instagram.
            consumer_secret: String
                - The consumer_secret from registering application
                  on Instagram.
        '''

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret


    def get_authorize_url(self):
        '''
            
        Where we get the oauth_token and oauth_token_secret from request_token_url,
        returns an authorize url.
        
        From the redirect url [provided when we registered the app] we obtain the oauth verifier.

        '''

        oauth = OAuth1Session(self.consumer_key, self.consumer_secret)
        fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)

        #temporary
        self.oauth_token = fetch_response.get('oauth_token')
        self.oauth_token_secret = fetch_response.get('oauth_token_secret')

        print(self.oauth_token)
        print(self.oauth_token_secret)


        authorization_url = oauth.authorization_url(AUTHORIZATION_URL)


        return authorization_url 

    
    def get_access_token_url(self, oauthVerifier):

        '''
            
        Get access token from redirect url.
        Parameters:
            oauthVerifier: String
        '''

        print("token inicial: " + self.oauth_token)

        oauth = OAuth1Session(self.consumer_key, self.consumer_secret, resource_owner_key = self.oauth_token, resource_owner_secret = self.oauth_token_secret, verifier=oauthVerifier)

        oauth_tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)


        #permanent
        self.oauth_token = oauth_tokens.get('oauth_token')
        self.oauth_token_secret = oauth_tokens.get('oauth_token_secret')

        print("token permanente: " + self.oauth_token)
        print(self.oauth_token_secret)
    


    #API CALLS
    def get_email(self):

        oauth = OAuth1Session(self.consumer_key, self.consumer_secret, resource_owner_key= self.oauth_token, resource_owner_secret= self.oauth_token_secret)
        r = oauth.get(GET_EMAIL_DATA_URL)
        email = r.content.decode('utf-8')
        json_acceptable_string = email.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        self.email = d.get('email')
        print(self.email)


    def get_name(self):

        oauth = OAuth1Session(self.consumer_key, self.consumer_secret, resource_owner_key = self.oauth_token, resource_owner_secret = self.oauth_token_secret)
        r = oauth.get(GET_NAME_DATA_URL)
        print(r.content)



def generateSignature(parameters, link, method, consumer_secret):
    
    '''
    Generates the signature.
    '''
    
    params = urllib.parse.urlencode(collections.OrderedDict(sorted(parameters.items())))
    
    print(params)
    
    #Create Signature Base String
    signatureBaseString = (method.upper()+'&'+percentEncode(str(link))+'&'+percentEncode(params))
    
    print("sig_base= " + signatureBaseString)
    
    #Get the signing key
    signingKey = createSigningKey(consumer_secret)
    
    print("signing_key= " + signingKey)
    
    return calculateSignature(signingKey, signatureBaseString)



def calculateSignature(signingKey, signatureBaseString):
    '''
    Calculate signature using HMAC-SHA1
    '''
    key_bytes= bytes(signingKey , 'latin-1')
        
    #print(signingKey)
    #print(key_bytes)
    #print(signatureBaseString)
        
    msg = signatureBaseString.encode()
        
    #print(msg)
    hashed = hmac.new(key_bytes, msg, hashlib.sha1)
        
    sig = binascii.b2a_base64(hashed.digest())[:-1]
        
    return percentEncode(sig)
    
    '''
    
    raw = signatureBaseString.encode("utf-8")
    key = signingKey.encode("utf-8")
    
    
    hashed = hmac.new(key, raw, sha1)
    
    return base64.encodebytes(hashed.digest()).decode('utf-8')
    '''


def createSigningKey(consumerSecret):
    '''
    Creates the key to sign the request with (consumerSecret + Token if we have the Token already)
    '''
    
    signingKey = percentEncode(consumerSecret) + '&'
    
    return signingKey


def createAuthHeader(parameters):
    '''
    Format authorization header with oath parameters.
    '''
    
    orderedParameters = collections.OrderedDict(sorted(parameters.items()))
    authHeader = ('%s="%s"' % (k, v) for k, v in orderedParameters.items())
    
    return ', '.join(authHeader)

def percentEncode(string):
    
    return urllib.parse.quote(string, safe='~')



