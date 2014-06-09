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

        private Text retkey = new Text();
        private Text retvalue = new Text();

        private Map<String, Integer> COMPLIMENTS = new HashMap<String, Integer>();
        private Map<String, Integer> COMPLAINTS = new HashMap<String, Integer>();
        private List<String> LECTURERS = new ArrayList<String>();

        public void addCompliments() {
            COMPLIMENTS.put("不錯", new Integer(1));
            COMPLIMENTS.put("nice", new Integer(2));
            COMPLIMENTS.put("good", new Integer(3));
            COMPLIMENTS.put("very good", new Integer(4));
            COMPLIMENTS.put("很清楚", new Integer(5));
            COMPLIMENTS.put("很好", new Integer(6));
            COMPLIMENTS.put("excellent", new Integer(7));
            COMPLIMENTS.put("讚啦", new Integer(8));
            COMPLIMENTS.put("太讚", new Integer(9));
            COMPLIMENTS.put("brilliant", new Integer(10));
        }

        public void addComplaints() {
            COMPLAINTS.put("don't understand", new Integer(-1));
            COMPLAINTS.put("聽不懂", new Integer(-2));
            COMPLAINTS.put("bad", new Integer(-3));
            COMPLAINTS.put("鳥", new Integer(-4));
            COMPLAINTS.put("sucks", new Integer(-5));
            COMPLAINTS.put("爛", new Integer(-6));
            COMPLAINTS.put("hell", new Integer(-7));
            COMPLAINTS.put("無言", new Integer(-8));
            COMPLAINTS.put("bollocks", new Integer(-9));
            COMPLAINTS.put("超爛", new Integer(-10));
        }

        public void addLecturers() {
            LECTURERS.add("Isabel");
            LECTURERS.add("Amy");
            LECTURERS.add("Alexis");
            LECTURERS.add("Lily");
            LECTURERS.add("Kelly");
            LECTURERS.add("Bob");
            LECTURERS.add("Pitt");
            LECTURERS.add("Alen");
            LECTURERS.add("Aaron");
            LECTURERS.add("Brian");
            LECTURERS.add("Ian");
            LECTURERS.add("Henry");
        }

        @Override
        public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

            addLecturers();
            addCompliments();
            addComplaints();

            String lecturer = "";
            String[] line_split = value.toString().split(",");
            String student = line_split[0];
            String age = line_split[1];
            String district = line_split[2];
            String comments = line_split[3];
            Integer score = new Integer(0);

            for (String lec : LECTURERS) {
                if (comments.contains(lec)) {
                    lecturer = lec;
                    for (Map.Entry<String, Integer> entry : COMPLIMENTS.entrySet()) {
                        if (comments.contains(entry.getKey())) {
                            score = entry.getValue();
                            break;
                        }
                    }
                    if (score == 0) {
                        for (Map.Entry<String, Integer> entry : COMPLAINTS.entrySet()) {
                            if (comments.contains(entry.getKey())) {
                                score = entry.getValue();
                                break;
                            }
                        }
                    }
                    break;
                }
            }

            retkey.set(lecturer);
            retvalue.set(student + "," + age + "," + district + "," + score.toString() + ",");
            context.write(retkey, retvalue);
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
