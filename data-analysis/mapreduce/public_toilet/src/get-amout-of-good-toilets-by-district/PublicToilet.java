import java.util.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

public class PublicToilet extends Configured implements Tool {

    public static class PublicToiletMapper
        extends Mapper<LongWritable, Text, Text, IntWritable> {

        private Text retkey = new Text();

        public boolean isGoodToilet(float total, float first, float second) {
            return (first + second) / total >= 0.75 ? true : false;
        }

        @Override
        public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

            if (value.charAt(0) != '#') {
                String[] line_split = value.toString().split(",");
                if (line_split[7].trim().equals("1") && ! line_split[2].trim().equals("0")) {
                    float total = Integer.parseInt(line_split[2]);
                    float first = Integer.parseInt(line_split[3]);
                    float second = Integer.parseInt(line_split[4]);
                    if (isGoodToilet(total, first, second)) {
                        //regex.Pattern p = regex.Pattern.compile("^\u81fa\u5317\u5e02([^\u5340\u5e02]+\u5340).*");
                        Pattern p = Pattern.compile("^臺北市([^市區]+區).*");
                        Matcher m = p.matcher(line_split[8]);
                        if (m.matches()) {
                            String district = m.group(1);
                            retkey.set(district);
                            context.write(retkey, new IntWritable(1));
                        }
                    }
                }
            }
        }
    }

    public static class PublicToiletReducer
        extends Reducer<Text, IntWritable, Text, IntWritable> {

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {

            int sum = 0;
            for (IntWritable v : values) {
                sum += v.get();
            }
            context.write(key, new IntWritable(sum));
        }
    }

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

        Configuration conf = new Configuration();

        Job job = new Job(conf, "Public Toilet");
        job.setJarByClass(PublicToilet.class);

        job.setMapperClass(PublicToiletMapper.class);
        job.setReducerClass(PublicToiletReducer.class);

        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }
}
