package com.pi.multiauth_v2.fragments;


import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.pi.multiauth_v2.LogsAdapter;
import com.pi.multiauth_v2.R;

import org.json.JSONArray;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class LogsFragment extends Fragment {

    private String token;
    private String baseUrl;

    private RecyclerView recyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;


    public LogsFragment() {
        // Required empty public constructor
    }

    @SuppressLint("ValidFragment")
    public LogsFragment(String token)
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
        final View v = inflater.inflate(R.layout.fragment_logs, container, false);




        /*
        final ProgressDialog progress = new ProgressDialog(getActivity());
        progress.setMessage("Downloading logs...");
        progress.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progress.setIndeterminate(true);
        progress.show();
        */

        RequestQueue queue = Volley.newRequestQueue(getActivity());
        String url = baseUrl + "api/get_latest_logs/";

        StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try
                {
                    JSONObject result = new JSONObject(response);
                    JSONArray result_arr = result.getJSONArray("logs");
                    //progress.dismiss();

                    String[] myDataset = new String[result_arr.length()];

                    for (int i = 0; i<result_arr.length(); i++)
                    {
                        JSONObject log = result_arr.getJSONObject(i);
                        String logstr = log.getString("log_type") + ":::" + log.getString("time_stamp");
                        Log.w("DEBUG", logstr);
                        myDataset[i] = logstr;
                    }


                    recyclerView = (RecyclerView) v.findViewById(R.id.my_recycler_view);
                    recyclerView.setHasFixedSize(true);
                    Log.w("DEBUG", "Setted up recyclerview");

                    layoutManager = new LinearLayoutManager(getActivity());
                    recyclerView.setLayoutManager(layoutManager);
                    Log.w("DEBUG", "Added its layout manager");

                    // specify an adapter (see also next example)
                    mAdapter = new LogsAdapter(myDataset);
                    recyclerView.setAdapter(mAdapter);
                    Log.w("DEBUG", "Setted an adapter");

                } catch (Exception e)
                {
                    Log.w("DEBUG", e.getLocalizedMessage());
                    Toast.makeText(getActivity(), "An error has ocurred!", Toast.LENGTH_LONG).show();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.w("DEBUG", error.toString());
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

        return v;
    }

}
