package my_pig_java_udfs;
import java.io.IOException;
import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;
//import org.apache.hadoop.io.WritableComparable;

public class ScoreMap extends EvalFunc<String>
{
	public String exec(Tuple input) throws IOException {
		if (input == null || input.size() == 0) {
			return "0";
		}
		try {
			Integer score = (Integer)input.get(0);
			if (score == 1) {
				return "100";
			} else if (score == 2) {
				return "90";
			} else if (score == 3) {
				return "80";
			} else if (score == 4) {
				return "70";
			} else if (score == 5) {
				return "60";
			} else if (score <= 10) {
				return "50";
			} else if (score <= 20) {
				return "40";
			} else if (score <= 30) {
				return "30";
			} else if (score <= 40) {
				return "20";
			} else if (score <= 50) {
				return "10";
			} else if (score <= 100) {
				return "5";
			} else {
				return "0";
			}
		} catch (Exception e) {
			return "0";
			//throw new IOException("Caught exception processing input row ", e);
		}
	}
}
