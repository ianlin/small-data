import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

public class PublicToilet extends Configured implements Tool {

    public static class PublicToiletMapper
        extends Mapper<LongWritable, Text, Text, Text> {

        private Text retkey = new Text();
        private Text retvalue = new Text();

        @Override
        public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

            if (value.charAt(0) != '#') {
                String[] line_split = value.toString().split(",");
                if (line_split[7].trim().equals("1")) {
                    retkey.set(line_split[1]);
                    retvalue.set(line_split[8]);
                    context.write(retkey, retvalue);
                }
            }
        }
    }

    /*
    public static class PublicToiletReducer
        extends Reducer<Text, Text, Text, IntWritable> {

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {

            int sum = 0;
            for (Text v : values) {
                String[] v_split = v.toString().split(",");
                sum += Integer.parseInt(v_split[v_split.length - 1]);
            }
            context.write(key, new IntWritable(sum));
        }
    }
    */

    public static void main(String[] args) throws Exception {
        int retCode = ToolRunner.run(new PublicToilet(), args);
        System.exit(retCode);
    }

    @Override
    public int run(String[] args) throws Exception {
        /*
        if (args.length != 2) {
            System.err.println("Usage: MaxTemperature <input path> <output path>");
            System.exit(-1);
        }
        */

        Job job = new Job(getConf(), "Public Toilet");
        job.setJarByClass(getClass());

        job.setMapperClass(PublicToiletMapper.class);
        //job.setReducerClass(PublicToiletReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }
}
