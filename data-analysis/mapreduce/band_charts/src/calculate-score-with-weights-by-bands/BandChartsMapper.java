import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonElement;

public class BandChartsMapper
    extends Mapper<LongWritable, Text, Text, IntWritable> {

    private Text retkey = new Text();
    private IntWritable retvalue = new IntWritable();

    @Override
    public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        String line = value.toString();
        int score = 0;
        JsonParser jsonparser = new JsonParser();
        JsonObject jsonobj = (JsonObject) jsonparser.parse(line);
        for (Map.Entry<String,JsonElement> entry : jsonobj.entrySet()) {
            JsonObject entryobj = entry.getValue().getAsJsonObject();
            for (Map.Entry<String,JsonElement> subentry : entryobj.entrySet()) {
                int rank = subentry.getValue().getAsInt();
                if (rank == 1) {
                    score = 100;
                } else if (rank == 2) {
                    score = 90;
                } else if (rank == 3) {
                    score = 80;
                } else if (rank == 4) {
                    score = 70;
                } else if (rank == 5) {
                    score = 60;
                } else if (rank >= 6 && rank <= 10) {
                    score = 50;
                } else if (rank >= 11 && rank <= 20) {
                    score = 40;
                } else if (rank >= 21 && rank <= 30) {
                    score = 30;
                } else if (rank >= 31 && rank <= 40) {
                    score = 20;
                } else if (rank >= 41 && rank <= 50) {
                    score = 10;
                } else if (rank >= 51 && rank <= 100) {
                    score = 5;
                } else {
                    score = 0;
                }
                retkey.set(entry.getKey());
                retvalue.set(score);
                context.write(retkey, retvalue);
            }
        }
    }
}
