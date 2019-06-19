package com.pi.multiauth_v2;

import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.Toast;

import com.pi.multiauth_v2.background.NFCService;

public class NFCActivity extends AppCompatActivity {

    final Context context = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nfc);

        CheckBox nfcCheckbox = findViewById(R.id.checkBox);

        boolean running = false;
        ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
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
                    Intent intent = new Intent(context, NFCService.class);
                    Log.w("NFCDEBUG", "Starting service...");
                    startService(intent);
                    Toast.makeText(context, "NFC Service activated!", Toast.LENGTH_LONG).show();
                } else
                {
                    Intent intent = new Intent(context, NFCService.class);
                    Log.w("NFCDEBUG", "Stopping service...");
                    Toast.makeText(context, "NFC Service deactivated!", Toast.LENGTH_LONG).show();
                    stopService(intent);
                }

            }
        });

    }
}
