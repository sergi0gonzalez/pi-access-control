package com.pi.multiauth_v2;

import android.Manifest;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import com.pi.multiauth_v2.otp.TimeBasedOneTimePasswordGenerator;

import java.nio.charset.Charset;
import java.util.Date;
import java.util.concurrent.TimeUnit;

import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import io.chirp.connect.ChirpConnect;
import io.chirp.connect.models.ChirpError;

public class SoundActivity extends AppCompatActivity {

    ChirpConnect chirp;
    private static final int RESULT_REQUEST_RECORD_AUDIO = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sound);

        chirp = new ChirpConnect(this, "B8a3F4fA4a1Aaf09Afe4ca4f9", "c2FaC2d4FBB83ba735ecED0cF8dAb52C1BB0b3349A7eFCeaB9");
        ChirpError error = chirp.setConfig("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");

        if (error.getCode() == 0) {
            Log.w("DEBUG", "Configured ChirpSDK");
        } else {
            Log.w("DEBUG", error.getMessage());
        }

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case RESULT_REQUEST_RECORD_AUDIO: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    ChirpError error = chirp.start();
                    if (error.getCode() > 0) {
                        Log.e("ChirpError: ", error.getMessage());
                    } else {
                        Log.v("ChirpSDK: ", "Started ChirpSDK");
                    }
                }
                return;
            }
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        Log.w("DEBUG", "GETTING PERMISSIONS");
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.RECORD_AUDIO}, RESULT_REQUEST_RECORD_AUDIO);
        }
        else {
            ChirpError error = chirp.start();
            if (error.getCode() > 0) {
                Log.w("DEBUG", error.getMessage());
            } else {
                Log.w("DEBUG ", "Started ChirpSDK");
            }
        }
    }

    @Override
    public void onPause() {
        super.onPause();
        chirp.stop();
    }

    public void sendSoundCred(View view) {
        SharedPreferences prefs = getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);

        if (prefs.contains("credential")) {
            String message;
            try {

                TimeBasedOneTimePasswordGenerator totp_manager = new TimeBasedOneTimePasswordGenerator(30, TimeUnit.SECONDS, 8, TimeBasedOneTimePasswordGenerator.TOTP_ALGORITHM_HMAC_SHA256);
                String secret_hex = prefs.getString("credential", null);
                byte[] secret = hexStringToByteArray(secret_hex);
                SecretKey secretKey = new SecretKeySpec(secret, 0, secret.length, "SHA256");
                String code = String.valueOf(totp_manager.generateOneTimePassword(secretKey, new Date()));
                String email = prefs.getString("email", "null");
                message = email+":"+code;

                byte[] payload = message.getBytes(Charset.forName("UTF-8"));

                ChirpError error = chirp.send(payload);
                if (error.getCode() > 0) {
                    Log.w("DEBUG", "Chirp:" + error.getMessage());
                } else {
                    Log.w("DEBUG", "Chirp: Sent " + message);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }


    }

    public static byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i+1), 16));
        }
        return data;
    }

}


