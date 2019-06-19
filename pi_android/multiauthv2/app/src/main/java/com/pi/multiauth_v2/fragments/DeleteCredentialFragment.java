package com.pi.multiauth_v2.fragments;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.DialogFragment;

import com.pi.multiauth_v2.MainActivity;
import com.pi.multiauth_v2.R;

public class DeleteCredentialFragment extends DialogFragment {
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        // Use the Builder class for convenient dialog construction
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        builder.setMessage("Remove credential from device?")
                .setPositiveButton("Erase", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        final SharedPreferences prefs = getActivity().getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);
                        SharedPreferences.Editor editor = prefs.edit();
                        editor.remove("credential");
                        editor.remove("credUpdateDate");
                        editor.commit();

                        MainActivity ma = (MainActivity)getActivity();
                        CredentialsFragment cf = (CredentialsFragment)ma.fragment;
                        cf.updateCredentialStatusText();
                    }
                })
                .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // User cancelled the dialog
                    }
                })
                .setIcon(R.drawable.ic_delete)
                .setMessage("You will need an internet connection to recover the credential!");
        // Create the AlertDialog object and return it
        return builder.create();
    }
}
