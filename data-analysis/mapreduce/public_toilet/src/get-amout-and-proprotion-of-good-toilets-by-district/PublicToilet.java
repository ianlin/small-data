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
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

public class PublicToilet extends Configured implements Tool {

    public static class PublicToiletMapper
        extends Mapper<LongWritable, Text, Text, IntWritable> {

        public boolean isGoodToilet(float total, float first, float second) {
            return (first + second) / total >= 0.75 ? true : false;
        }

        @Override
        public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

            if (value.charAt(0) != '#') {
                String[] line_split = value.toString().split(",");
                String address = line_split[8].trim();
                String total_toilet = line_split[2].trim();
                //Pattern p = regex.Pattern.compile("^\u81fa\u5317\u5e02([^\u5340\u5e02]+\u5340).*");
                Pattern p = Pattern.compile("^臺北市([^市區]+區).*");
                Matcher m = p.matcher(address);
                if (m.matches()) {
                    IntWritable good_toilet = new IntWritable(0);
                    String district = m.group(1);
                    String handicapped = line_split[7].trim();
                    
                    if (handicapped.equals("1") && ! total_toilet.equals("0")) {
                        float total = Integer.parseInt(total_toilet);
                        float first = Integer.parseInt(line_split[3]);
                        float second = Integer.parseInt(line_split[4]);
                        if (isGoodToilet(total, first, second)) {
                            good_toilet.set(1);
                        }
                    }
                    context.write(new Text(district), good_toilet);
                }
            }
        }
    }

    public static class PublicToiletReducer
        extends Reducer<Text, IntWritable, Text, Text> {

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {

            Float total_toilet = new Float(0);
            Float good_toilet = new Float(0);
            Float proportion = new Float(0);
            String retvalue = "";

            for (IntWritable v : values) {
                total_toilet += 1;
                good_toilet += v.get();
            }

            proportion = (Float) good_toilet / total_toilet;

            retvalue = total_toilet.toString() + "\t" + good_toilet.toString() + "\t" + proportion.toString();

            context.write(key, new Text(retvalue));
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

        Job job = new Job(getConf(), "Public Toilet");
        job.setJarByClass(getClass());

        job.setMapperClass(PublicToiletMapper.class);
        job.setReducerClass(PublicToiletReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }
}
