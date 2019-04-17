package pi.multi_auth;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    public void signInHandler(View view)
    {
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://192.168.1.220:8080/api/token_request/";
        final EditText textView = findViewById(R.id.input_username);
        JSONObject postparams = new JSONObject();
        final String username = ((EditText)findViewById(R.id.input_username)).getText().toString();
        final String password = ((EditText)findViewById(R.id.input_password)).getText().toString();


        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {
                        try
                        {
                            JSONObject result = new JSONObject(response);
                            Log.d("mydebug", "onResponse : " + response);

                            if (result.getString("status").equals("granted"))
                            {
                                Toast.makeText(LoginActivity.this, "Login Successful!", Toast.LENGTH_LONG).show();

                                Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                                intent.putExtra("token", result.getString("token"));
                                startActivity(intent);
                            } else
                            {
                               Toast.makeText(LoginActivity.this, result.getString("reason"), Toast.LENGTH_LONG).show();
                            }
                        } catch (Exception e)
                        {
                            Toast.makeText(LoginActivity.this, "An error has ocurred!", Toast.LENGTH_LONG).show();
                        }
                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(LoginActivity.this, "An error has ocurred.", Toast.LENGTH_LONG).show();
                    }
                }
        ) {
            @Override
            protected Map<String, String> getParams()
            {
                Map<String, String> params = new HashMap<String, String>();
                params.put("username", username);
                params.put("password", password);

                return params;
            }
        };

        queue.add(postRequest);
    }
}
