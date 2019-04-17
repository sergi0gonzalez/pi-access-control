package pi.multi_auth;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.BlurMaskFilter;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;


public class CommFragment extends Fragment
{
    public CommFragment() {
        // Required empty public constructor
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

        if (comm_method.equals("NFC"))
        {
            toCheck = v.findViewById(R.id.nfcRadio);
            toCheck.setChecked(true);
        } else if (comm_method.equals("QR"))
        {
            toCheck = v.findViewById(R.id.qrRadio);
            toCheck.setChecked(true);
        } else if (comm_method.equals("SOUND"))
        {
            toCheck = v.findViewById(R.id.soundRadio);
            toCheck.setChecked(true);
        }


        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener()
        {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId)
            {
                switch(checkedId){
                    case R.id.nfcRadio:
                        prefs.edit().putString("pi.multi_auth.comm_method", "NFC").apply();
                        break;
                    case R.id.qrRadio:
                        prefs.edit().putString("pi.multi_auth.comm_method", "QR").apply();
                        break;
                    case R.id.soundRadio:
                        prefs.edit().putString("pi.multi_auth.comm_method", "SOUND").apply();
                        break;
                }
            }
        });
        return v;
    }
}
