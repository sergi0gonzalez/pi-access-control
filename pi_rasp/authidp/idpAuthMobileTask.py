from idpAuthMobile import UniversityOauth

#access_token and access_token_secret received from the mobile auth proccess

idpConnection = UniversityOauth('_key', '_secret', '_access_token', '_access_token_secret')


idpConnection.get_nmec()


#print(idpConnection.get_authorize_url())
#verifier = input('paste the verifier')
#idpConnection.get_access_token_url(verifier)

