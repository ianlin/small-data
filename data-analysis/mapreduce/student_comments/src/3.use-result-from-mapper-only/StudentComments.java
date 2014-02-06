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

public class StudentComments extends Configured implements Tool {

    public static class StudentCommentsMapper
        extends Mapper<LongWritable, Text, Text, Text> {

        @Override
        public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

            String[] value_split = value.toString().split("\t");
            String retkey = value_split[0];
            String retvalue = value_split[1];
            context.write(new Text(retkey), new Text(retvalue));
        }
    }

    public static class StudentCommentsReducer
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

    public static void main(String[] args) throws Exception {
        int retCode = ToolRunner.run(new StudentComments(), args);
        System.exit(retCode);
    }

    @Override
    public int run(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: MaxTemperature <input path> <output path>");
            System.exit(-1);
        }

        Job job = new Job(getConf(), "Student Comments");
        job.setJarByClass(getClass());

        job.setMapperClass(StudentCommentsMapper.class);
        job.setReducerClass(StudentCommentsReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }
}
