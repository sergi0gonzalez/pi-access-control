package com.pi.multiauth_v2.fragments;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.widget.CardView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.pi.multiauth_v2.BluetoothActivity;
import com.pi.multiauth_v2.NFCActivity;
import com.pi.multiauth_v2.QRActivity;
import com.pi.multiauth_v2.R;
import com.pi.multiauth_v2.SoundActivity;


public class AuthenticateFragment extends Fragment {

    public AuthenticateFragment() {

    }
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View v =  inflater.inflate(R.layout.fragment_authenticate, container, false);

        CardView card = v.findViewById(R.id.cardViewQR);

        card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), QRActivity.class);
                startActivity(intent);
            }
        });

        card = v.findViewById(R.id.cardViewSound);

        card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), SoundActivity.class);
                startActivity(intent);
            }
        });

        card = v.findViewById(R.id.cardViewBT);

        card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), BluetoothActivity.class);
                startActivity(intent);
            }
        });

        card = v.findViewById(R.id.cardViewNFC);

        card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), NFCActivity.class);
                startActivity(intent);
            }
        });


        return v;
    }


}
