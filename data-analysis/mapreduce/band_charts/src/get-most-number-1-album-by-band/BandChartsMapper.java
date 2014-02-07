import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.LongWritable;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonElement;

public class BandChartsMapper
    extends Mapper<LongWritable, Text, Text, Text> {

    private Text retkey = new Text();
    private Text retvalue = new Text();

    @Override
    public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        String line = value.toString();
        JsonParser jsonparser = new JsonParser();
        JsonObject jsonobj = (JsonObject) jsonparser.parse(line);
        for (Map.Entry<String,JsonElement> entry : jsonobj.entrySet()) {
            JsonObject entryobj = entry.getValue().getAsJsonObject();
            for (Map.Entry<String,JsonElement> subentry : entryobj.entrySet()) {
                if (subentry.getValue().getAsInt() == 1) {
                    retkey.set(entry.getKey());
                    retvalue.set(subentry.getKey());
                    context.write(retkey, retvalue);
                }
            }
        }
    }
}
