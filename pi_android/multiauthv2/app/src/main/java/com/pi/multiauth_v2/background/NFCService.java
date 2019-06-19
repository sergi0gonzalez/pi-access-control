package com.pi.multiauth_v2.background;

import android.content.Context;
import android.content.SharedPreferences;
import android.nfc.cardemulation.HostApduService;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.util.Log;
import android.widget.Toast;

import com.pi.multiauth_v2.otp.TimeBasedOneTimePasswordGenerator;

import java.util.Date;
import java.util.concurrent.TimeUnit;

import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;


public class NFCService extends HostApduService {
    @Override
    public byte[] processCommandApdu(byte[] apdu, Bundle extras) {
        Log.w("NFCDEBUG", "RECEIVED COMMAND APDU");

        String response;
        final SharedPreferences prefs = getSharedPreferences("pi.multi_auth_v2", Context.MODE_PRIVATE);
        if (prefs.contains("credential"))
        {

            TimeBasedOneTimePasswordGenerator totp_manager = null;
            try {
                totp_manager = new TimeBasedOneTimePasswordGenerator(30, TimeUnit.SECONDS, 8, TimeBasedOneTimePasswordGenerator.TOTP_ALGORITHM_HMAC_SHA256);
            } catch(Exception e)
            {
                Log.w("NFCDEBUG","TOTP Generation Error!");
            }

            String secret_hex = prefs.getString("credential", null);
            byte[] secret = null;
            try {
                secret = hexStringToByteArray(secret_hex);
            } catch(Exception e)
            {
                Log.w("NFCDEBUG","Credential Loading Error");
            }

            SecretKey secretKey = new SecretKeySpec(secret, 0, secret.length, "SHA256");
            String code = null;
            try{
                code = String.valueOf(totp_manager.generateOneTimePassword(secretKey, new Date()));
            } catch(Exception e)
            {
                Log.w("NFCDEBUG","Secret key generation error");
            }

            String email = prefs.getString("email", "null");
            final String message = email+":"+code;

            response = bytesToHex(message.getBytes());

        } else
        {
            response = "0";
        }

        String respApdu = response + "9000";
        Log.w("DEBUG", respApdu);
        return hexStringToByteArray(respApdu);
    }
    @Override
    public void onDeactivated(int reason) {

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

    public static String bytesToHex(byte[] bytes) {
        final char[] hexArray = "0123456789ABCDEF".toCharArray();
        char[] hexChars = new char[bytes.length * 2];
        for ( int j = 0; j < bytes.length; j++ ) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = hexArray[v >>> 4];
            hexChars[j * 2 + 1] = hexArray[v & 0x0F];
        }
        return new String(hexChars);
    }
}


