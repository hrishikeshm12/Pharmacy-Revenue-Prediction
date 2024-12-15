
import hex.genmodel.easy.EasyPredictModelWrapper;
import hex.genmodel.MojoModel;
import hex.genmodel.easy.RowData;
import hex.genmodel.easy.prediction.RegressionModelPrediction;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;

@SpringBootApplication
@RestController
@ComponentScan(basePackages = "com.hrishikesh")

public class MOJOModelServer {

    private EasyPredictModelWrapper predictor;

    public static void main(String[] args) {
        SpringApplication.run(MOJOModelServer.class, args);
    }

    @PostMapping("/predict")
    public double predict(@RequestBody String inputData) throws Exception {
        // Parse the input data (simple CSV format key:value)
        String[] inputs = inputData.split(",");
        RowData rowData = new RowData();
        for (String input : inputs) {
            String[] keyValue = input.split(":");
            rowData.put(keyValue[0], keyValue[1]);
        }

        // Make prediction
        RegressionModelPrediction prediction = predictor.predictRegression(rowData);
        return prediction.value;
    }

    @PostConstruct
    public void init() throws Exception {
        // Load the MOJO model
        MojoModel mojoModel = MojoModel.load("./models/GBM_5_AutoML_1_20241031_73853.zip");
        EasyPredictModelWrapper.Config config = new EasyPredictModelWrapper.Config();
        config.setModel(mojoModel);
        predictor = new EasyPredictModelWrapper(config);
    }
}
