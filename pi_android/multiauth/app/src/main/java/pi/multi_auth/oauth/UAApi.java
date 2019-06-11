package pi.multi_auth.oauth;

import com.github.scribejava.core.builder.api.DefaultApi10a;

public class UAApi extends DefaultApi10a {

    private static final String AUTHORIZE_URL = "http://identity.ua.pt/oauth/authorize";
    private static final String REQUEST_TOKEN_RESOURCE = "http://identity.ua.pt/oauth/request_token";
    private static final String ACCESS_TOKEN_RESOURCE = "http://identity.ua.pt/oauth/access_token";

    protected UAApi() {
    }

    private static class InstanceHolder {
        private static final UAApi INSTANCE = new UAApi();
    }

    public static UAApi instance() {
        return InstanceHolder.INSTANCE;
    }

    @Override
    public String getAccessTokenEndpoint() {
        return ACCESS_TOKEN_RESOURCE;
    }

    @Override
    public String getRequestTokenEndpoint() {
        return REQUEST_TOKEN_RESOURCE;
    }

    @Override
    public String getAuthorizationBaseUrl() {
        return AUTHORIZE_URL;
    }
}