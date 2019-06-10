package pi.multi_auth;

import android.annotation.SuppressLint;
import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.BlurMaskFilter;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


public class CommFragment extends Fragment
{
    private String token;
    public CommFragment() {
        // Required empty public constructor
    }

    @SuppressLint("ValidFragment")
    public CommFragment(String token)
    {
        this.token = token;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_comm, container, false);
        RadioGroup radioGroup = v.findViewById(R.id.radioGroup);

        final SharedPreferences prefs = getActivity().getSharedPreferences("pi.multi_auth", Context.MODE_PRIVATE);
        String comm_method = prefs.getString("pi.multi_auth.comm_method", "NFC");
        RadioButton toCheck;

        if (comm_method.equals("QR"))
        {
            toCheck = v.findViewById(R.id.qrRadio);
            toCheck.setChecked(true);
        } else if (comm_method.equals("SOUND"))
        {
            toCheck = v.findViewById(R.id.soundRadio);
            toCheck.setChecked(true);
        } else if (comm_method.equals("BLUETOOTH"))
        {
            toCheck = v.findViewById(R.id.bluetoothRadio);
            toCheck.setChecked(true);
        }


        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener()
        {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId)
            {
                switch(checkedId){
                    case R.id.qrRadio:
                        prefs.edit().putString("pi.multi_auth.comm_method", "QR").apply();
                        break;
                    case R.id.soundRadio:
                        prefs.edit().putString("pi.multi_auth.comm_method", "SOUND").apply();
                        break;
                    case R.id.bluetoothRadio:
                        prefs.edit().putString("pi.multi_auth.comm_method", "BLUETOOTH").apply();
                        break;
                }
            }
        });

        CheckBox nfcCheckbox = v.findViewById(R.id.nfcCheckbox);

        boolean running = false;
        ActivityManager manager = (ActivityManager) getActivity().getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (NFCService.class.getName().equals(service.service.getClassName())) {
                running = true;
            }
        }

        if (running) nfcCheckbox.setChecked(true);
        nfcCheckbox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
           @Override
           public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

               if (isChecked)
               {
                   Intent intent = new Intent(getActivity(), NFCService.class);
                   Log.w("NFCDEBUG", "Starting service...");
                   getActivity().startService(intent);
                   Toast.makeText(getActivity(), "NFC Service activated!", Toast.LENGTH_LONG).show();
               } else
               {
                   Intent intent = new Intent(getActivity(), NFCService.class);
                   Log.w("NFCDEBUG", "Stopping service...");
                   Toast.makeText(getActivity(), "NFC Service deactivated!", Toast.LENGTH_LONG).show();
                   getActivity().stopService(intent);
               }

           }
       });



        Button fetchbutton = v.findViewById(R.id.pull);
        Button deletebutton = v.findViewById(R.id.delete);
        final TextView tv = v.findViewById(R.id.cred_status);

        fetchbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                RequestQueue queue = Volley.newRequestQueue(getActivity());
                String url = "http://192.168.1.220:8080/api/get_credential/";

                StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try
                        {
                            JSONObject result = new JSONObject(response);
                            String credential = result.getString("credential");

                            SharedPreferences.Editor editor = prefs.edit();
                            editor.putString("credential", credential);
                            editor.commit();
                            Toast.makeText(getActivity(), "Successfully fetched credential!", Toast.LENGTH_LONG).show();
                            updateCredentialStatusText(tv);

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

        deletebutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SharedPreferences.Editor editor = prefs.edit();
                editor.remove("credential");
                editor.commit();

                updateCredentialStatusText(tv);
                Toast.makeText(getActivity(), "Successfully deleted credential!", Toast.LENGTH_LONG).show();
            }
        });

        updateCredentialStatusText(tv);

        return v;
    }

    public void updateCredentialStatusText(TextView tv){

        SharedPreferences sharedPref = getActivity().getSharedPreferences("pi.multi_auth", Context.MODE_PRIVATE);
        if (!sharedPref.contains("credential"))
        {
            tv.setText("Status: unavailable");
            tv.setTextColor(Color.RED);
        } else {
            tv.setText("Status: available");
            tv.setTextColor(Color.GREEN);
        }

    }
}
