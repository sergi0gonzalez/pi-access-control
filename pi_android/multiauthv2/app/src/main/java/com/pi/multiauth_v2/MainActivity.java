package com.pi.multiauth_v2;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.support.annotation.NonNull;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.pi.multiauth_v2.fragments.AuthenticateFragment;
import com.pi.multiauth_v2.fragments.CredentialsFragment;
import com.pi.multiauth_v2.fragments.LogsFragment;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private String token;
    public Fragment fragment;
    private String baseUrl;
    Toolbar myToolbar;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            FragmentManager fragmentManager;
            FragmentTransaction fragmentTransaction;

            switch (item.getItemId()) {

                case R.id.navigation_authenticate:
                    fragmentManager = getSupportFragmentManager();
                    fragmentTransaction = fragmentManager.beginTransaction();
                    fragment = new AuthenticateFragment();
                    fragmentTransaction.replace(R.id.framelayout, fragment);
                    fragmentTransaction.commit();
                    myToolbar.setTitle("IEETASec");
                    return true;
                case R.id.navigation_credentials:
                    fragmentManager = getSupportFragmentManager();
                    fragmentTransaction = fragmentManager.beginTransaction();
                    fragment = new CredentialsFragment(token);
                    fragmentTransaction.replace(R.id.framelayout, fragment);
                    fragmentTransaction.commit();
                    myToolbar.setTitle("Credential");
                    return true;
                case R.id.navigation_logs:
                    fragmentManager = getSupportFragmentManager();
                    fragmentTransaction = fragmentManager.beginTransaction();
                    fragment = new LogsFragment(token);
                    fragmentTransaction.replace(R.id.framelayout, fragment);
                    fragmentTransaction.commit();
                    myToolbar.setTitle("Latest logs");
                    return true;
            }
            return false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        baseUrl = getResources().getString(R.string.base_url);

        myToolbar = (Toolbar) findViewById(R.id.main_toolbar);
        setSupportActionBar(myToolbar);
        myToolbar.setTitleTextColor(Color.WHITE);
        myToolbar.setTitle("IEETASec");

        Intent intent = getIntent();
        token = intent.getStringExtra("token");
        SharedPreferences prefsfortoken = getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);;

        if (token == null)
        {
            token =  prefsfortoken.getString("token", "null");
        } else
        {
            prefsfortoken.edit().putString("token", token).apply();
        }

        Log.w("DEBUG", "token=" + token);

        FragmentManager fragmentManager;
        FragmentTransaction fragmentTransaction;
        Fragment fragment;

        fragmentManager = getSupportFragmentManager();
        fragmentTransaction = fragmentManager.beginTransaction();
        fragment = new AuthenticateFragment();
        fragmentTransaction.replace(R.id.framelayout, fragment);
        fragmentTransaction.commit();

        BottomNavigationView navView = findViewById(R.id.nav_view);
        navView.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        RequestQueue queue = Volley.newRequestQueue(this);
        final Context context = this;
        String url = baseUrl + "api/get_email/";
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try
                {
                    JSONObject result = new JSONObject(response);
                    final SharedPreferences prefs = getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);
                    prefs.edit().putString("email", result.getString("email")).apply();
                    Log.w("DEBUG", result.getString("email"));

                } catch (Exception e)
                {
                    Toast.makeText(MainActivity.this, "An error has ocurred!", Toast.LENGTH_LONG).show();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainActivity.this, "An error has ocurred.", Toast.LENGTH_LONG).show();
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("Authorization", "Token " + token);
                return params;
            }
        };

        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }

}
