package pi.multi_auth;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.github.scribejava.core.builder.ServiceBuilder;
import com.github.scribejava.core.model.OAuth1AccessToken;
import com.github.scribejava.core.model.OAuth1RequestToken;
import com.github.scribejava.core.oauth.OAuth10aService;

import pi.multi_auth.oauth.OAuthResponseHelper;
import pi.multi_auth.oauth.UAApi;


public class UaAuthFragment extends Fragment
{
    private OAuthResponseHelper OAuth = new OAuthResponseHelper();

    public UaAuthFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_ua_auth, container, false);

        Button uaAuthButton = v.findViewById(R.id.ua_auth_button);
        uaAuthButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new OAuthTask(getActivity()).execute();
            }
        });

        final EditText authText = (EditText) v.findViewById(R.id.AuthText);
        Button saveAuthButton = v.findViewById(R.id.SaveAuthButton);
        saveAuthButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                OAuth.setVerifier(authText.getText().toString());
                new OAuthGetTokenTask(getActivity()).execute();
            }
        });

        return v;
    }



    public class OAuthTask extends AsyncTask<Void, Void, String> {
        private Activity activity;

        public OAuthTask(Activity activity) {
            this.activity = activity;
        }

        @Override
        protected String doInBackground(Void... params) {
            try {
                final OAuth10aService service = new ServiceBuilder("_428f4f4eaaa8d822d8f12693c714b1c57fb54cd9f2")
                        .apiSecret("_eb050ec4abe7c962acc1760d3045940bf20d8b8386")
                        // already using "oob" for callback
                        .build(UAApi.instance());
                OAuth.setService(service);

                final OAuth1RequestToken requestToken = service.getRequestToken();

                OAuth.setRequestToken(requestToken);

                String url = service.getAuthorizationUrl(requestToken);
                OAuth.setUrl(url);

                return url;
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(String result) {
            if(result == null){
                Toast.makeText(activity, "Erro", Toast.LENGTH_SHORT).show();
                return;
            }

            Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(result));
            activity.startActivity(browserIntent);
        }
    }





    public class OAuthGetTokenTask extends AsyncTask<Void, Void, String> {
        private Activity activity;

        public OAuthGetTokenTask(Activity activity) {
            this.activity = activity;
        }

        @Override
        protected String doInBackground(Void... params) {
            try {
                final OAuth1RequestToken requestToken = OAuth.getRequestToken();
                final OAuth1AccessToken accessToken = OAuth.getService().getAccessToken(requestToken, OAuth.getVerifier());

                return accessToken.getRawResponse();
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(String response) {
            if(response == null){
                Toast.makeText(activity, "Erro", Toast.LENGTH_SHORT).show();
                return;
            }

            final SharedPreferences prefs = getActivity().getSharedPreferences("pi.multi_auth", Context.MODE_PRIVATE);
            SharedPreferences.Editor editor = prefs.edit();
            editor.putString("pi.multi_auth.access_token", response);
            editor.commit();
        }
    }

}
