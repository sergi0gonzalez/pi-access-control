package pi.multi_auth.oauth;

import com.github.scribejava.core.model.OAuth1RequestToken;
import com.github.scribejava.core.oauth.OAuth10aService;

public class OAuthResponseHelper {
    private OAuth10aService service;
    private OAuth1RequestToken requestToken;
    private String url;
    private String verifier;

    public OAuth10aService getService() {
        return service;
    }

    public void setService(OAuth10aService service) {
        this.service = service;
    }

    public OAuth1RequestToken getRequestToken() {
        return requestToken;
    }

    public void setRequestToken(OAuth1RequestToken requestToken) {
        this.requestToken = requestToken;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getVerifier() {
        return verifier;
    }

    public void setVerifier(String verifier) {
        this.verifier = verifier;
    }
}
