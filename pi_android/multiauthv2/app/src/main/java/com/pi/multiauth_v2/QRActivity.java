package com.pi.multiauth_v2;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.util.TypedValue;
import android.widget.ImageView;
import android.widget.Toast;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.MultiFormatWriter;
import com.google.zxing.WriterException;
import com.google.zxing.common.BitMatrix;
import com.pi.multiauth_v2.background.QRIntentService;

public class QRActivity extends AppCompatActivity  {

    BroadcastReceiver updateUiReceiver;
    public static int white = 0xFFFFFFFF;
    public static int black = 0xFF000000;
    public static int WIDTH;
    private ImageView qrimageview;
    public static String broadcastAction = "com.pi.multiauth_v2.qr_receiver";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_qr);
        qrimageview = findViewById(R.id.qr_placeholder);
        Resources r = getResources();
        float dip = 400f;
        WIDTH = (int)Math.floor(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dip, r.getDisplayMetrics()));

    }

    @Override
    public void onResume(){
        super.onResume();

        IntentFilter filter = new IntentFilter();
        filter.addAction(QRActivity.broadcastAction);

        updateUiReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String message = intent.getStringExtra("message");
                Log.w("DEBUG" , "received broadcast in qrqactivity - " + message);
                try {
                    Bitmap qr_bitmap = encodeAsBitmap(message);
                    qrimageview.setImageBitmap(qr_bitmap);
                } catch (WriterException we)
                {
                    Toast.makeText(context, "QR Zxing library exception", Toast.LENGTH_LONG).show();
                }
            }
        };
        registerReceiver(updateUiReceiver, filter);
        Intent intent = new Intent(this, QRIntentService.class);
        startService(intent);

    }

    Bitmap encodeAsBitmap(String str) throws WriterException {
        BitMatrix result;
        try {
            result = new MultiFormatWriter().encode(str, BarcodeFormat.QR_CODE, WIDTH, WIDTH, null);
        } catch (IllegalArgumentException iae) {
            // Unsupported format
            return null;
        }
        int w = result.getWidth();
        int h = result.getHeight();
        int[] pixels = new int[w * h];
        for (int y = 0; y < h; y++) {
            int offset = y * w;
            for (int x = 0; x < w; x++) {
                pixels[offset + x] = result.get(x, y) ? black : white;
            }
        }
        Bitmap bitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
        bitmap.setPixels(pixels, 0, WIDTH, 0, 0, w, h);
        return bitmap;
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(updateUiReceiver);
        Intent intent = new Intent(this, QRIntentService.class);
        stopService(intent);
    }

}
