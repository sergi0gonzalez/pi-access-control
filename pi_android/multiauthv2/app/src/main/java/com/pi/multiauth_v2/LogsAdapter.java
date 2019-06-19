package com.pi.multiauth_v2;

import android.graphics.Color;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class LogsAdapter extends RecyclerView.Adapter<LogsAdapter.MyViewHolder> {
    private String[] mDataset;

    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder
    public static class MyViewHolder extends RecyclerView.ViewHolder {
        // each data item is just a string in this case
        public TextView timestampText, typeText;
        public MyViewHolder(View v) {
            super(v);

            timestampText = v.findViewById(R.id.timestampText);
            typeText = v.findViewById(R.id.typeText);
        }
    }

    // Provide a suitable constructor (depends on the kind of dataset)
    public LogsAdapter(String[] myDataset) {
        mDataset = myDataset;
    }

    // Create new views (invoked by the layout manager)
    @Override
    public LogsAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent,
                                                       int viewType) {
        // create a new view
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.log_view, parent, false);

        MyViewHolder vh = new MyViewHolder(v);
        return vh;
    }

    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        String s = mDataset[position];
        String date = s.split(":::")[1].split("T")[0];
        String time = s.split(":::")[1].split("T")[1].split("\\.")[0];
        String time_stamp = date + " " + time;
        String type = s.split(":::")[0];

        holder.timestampText.setText(time_stamp);
        holder.typeText.setText(type);

    }

    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.length;
    }
}
