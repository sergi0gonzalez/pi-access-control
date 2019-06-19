package com.pi.multiauth_v2.background;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;

import com.pi.multiauth_v2.QRActivity;
import com.pi.multiauth_v2.otp.TimeBasedOneTimePasswordGenerator;

import java.util.Date;
import java.util.concurrent.TimeUnit;

import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class QRIntentService extends IntentService {

    boolean running;
    int integ;
    private SharedPreferences prefs;

    public QRIntentService() {
        super("QRIntentService");
        running = true;
        integ = 1;

    }

    @Override
    protected void onHandleIntent(Intent intent) {
        prefs = getApplicationContext().getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);
        while (running)
        {
            try
            {

                if (prefs.contains("credential"))
                {
                    Intent broadCastIntent = new Intent();
                    broadCastIntent.setAction(QRActivity.broadcastAction);

                    try {
                        TimeBasedOneTimePasswordGenerator totp_manager = new TimeBasedOneTimePasswordGenerator(30, TimeUnit.SECONDS, 8, TimeBasedOneTimePasswordGenerator.TOTP_ALGORITHM_HMAC_SHA256);
                        String secret_hex = prefs.getString("credential", null);
                        byte[] secret = hexStringToByteArray(secret_hex);
                        SecretKey secretKey = new SecretKeySpec(secret, 0, secret.length, "SHA256");
                        String code = String.valueOf(totp_manager.generateOneTimePassword(secretKey, new Date()));
                        String email = prefs.getString("email", "null");
                        broadCastIntent.putExtra("message", email+":"+code);
                    } catch(Exception e)
                    {
                        e.printStackTrace();
                    }

                    int seconds_to_sleep = 1;
                    Thread.sleep(seconds_to_sleep * 1000);
                    sendBroadcast(broadCastIntent);
                }

            }
            catch (Exception ex)
            {
                ex.printStackTrace();
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

    @Override
    public void onDestroy() {
        super.onDestroy();
        running = false;
    }


}
