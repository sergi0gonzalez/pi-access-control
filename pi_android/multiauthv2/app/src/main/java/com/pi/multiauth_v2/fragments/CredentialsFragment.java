package com.pi.multiauth_v2.fragments;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.pi.multiauth_v2.R;

import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class CredentialsFragment extends Fragment {

    private String token;
    private TextView status, date;
    private String baseUrl;
    private ImageView deleteButton;

    public CredentialsFragment() {
        // Required empty public constructor
    }

    @SuppressLint("ValidFragment")
    public CredentialsFragment(String token)
    {
        this.token = token;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        baseUrl = getResources().getString(R.string.base_url);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_credentials, container, false);

        FloatingActionButton b = v.findViewById(R.id.fetchCredentialButton);
        deleteButton = v.findViewById(R.id.deleteButton);
        status = v.findViewById(R.id.credStatus);
        date = v.findViewById(R.id.credUpdateDate);

        deleteButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                v.startAnimation(AnimationUtils.loadAnimation(getActivity(), R.anim.image_click));
                new DeleteCredentialFragment().show(getFragmentManager(), "DeleteCredentialFragment");
            }
        });

        b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                RequestQueue queue = Volley.newRequestQueue(getActivity());
                String url = baseUrl + "api/get_credential/";

                StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try
                        {
                            JSONObject result = new JSONObject(response);
                            String credential = result.getString("credential");
                            String date = new SimpleDateFormat("yyyy-MM-dd HH:mm").format(new Date());

                            final SharedPreferences prefs = getActivity().getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);
                            SharedPreferences.Editor editor = prefs.edit();
                            editor.putString("credential", credential);
                            editor.putString("credUpdateDate", date);
                            editor.commit();
                            Toast.makeText(getActivity(), "Successfully fetched credential!", Toast.LENGTH_LONG).show();
                            updateCredentialStatusText();

                        } catch (Exception e)
                        {
                            Toast.makeText(getActivity(), "An error has ocurred!", Toast.LENGTH_LONG).show();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getActivity(), "An error has ocurred.", Toast.LENGTH_LONG).show();
                    }
                }) {
                    @Override
                    public Map<String, String> getHeaders() throws AuthFailureError {
                        Map<String, String>  params = new HashMap<String, String>();
                        params.put("Authorization", "Token " + token);
                        return params;
                    }
                };

                queue.add(stringRequest);

            }
        });

        updateCredentialStatusText();

        return v;
    }

    public void updateCredentialStatusText()
    {
        SharedPreferences sharedPref = getActivity().getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);
        if (!sharedPref.contains("credential"))
        {
            status.setText("Status: unavailable");
            date.setText("--");
            status.setTextColor(Color.RED);
            deleteButton.setVisibility(View.INVISIBLE);
        } else {
            status.setText("Status: available");
            date.setText("Last Updated: " + sharedPref.getString("credUpdateDate", "--"));
            status.setTextColor(Color.GREEN);
            deleteButton.setVisibility(View.VISIBLE);
        }
    }
}
