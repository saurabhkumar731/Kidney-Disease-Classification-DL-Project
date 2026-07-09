from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.model_training import Training
from cnnClassifier import logger

import os
import shutil



STAGE_NAME = "Training"



class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        training_config = config.get_training_config()
        training = Training(config=training_config)
        training.get_base_model()
        training.train_valid_generator()
        training.train()

        source_model="artifacts/training/model.h5"
        destination_dir="model"
        destination_model=os.path.join(destination_dir,"model.h5")
        
        os.makedirs(destination_dir,exist_ok=True)

        if os.path.exists(source_model):
            shutil.copy2(source_model, destination_model)
            logger.info(f"Model copied successfully to {destination_model}")
        else:
            logger.warning(f"Model not found at {source_model}")


if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
        