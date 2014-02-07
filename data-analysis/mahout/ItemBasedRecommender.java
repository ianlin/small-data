import java.util.*;
import java.io.*;
import java.io.IOException;

import org.apache.mahout.cf.taste.impl.model.file.*;
import org.apache.mahout.cf.taste.impl.recommender.*;
import org.apache.mahout.cf.taste.impl.similarity.*;
import org.apache.mahout.cf.taste.model.*;
import org.apache.mahout.cf.taste.recommender.*;
import org.apache.mahout.cf.taste.similarity.*;

public class ItemBasedRecommender {

    public static void main(String[] args) throws Exception {
        DataModel model = new FileDataModel(new File("/home/cloudera/small-data/data-analysis/mahout/mydata"));
        ItemSimilarity similarity = new PearsonCorrelationSimilarity(model);

        Recommender recommender = new GenericItemBasedRecommender(model, similarity);

        List<RecommendedItem> recommendations = recommender.recommend(4, 10);

        for (RecommendedItem recommendation : recommendations) {
            System.out.println(recommendation);
        }
    }
}
