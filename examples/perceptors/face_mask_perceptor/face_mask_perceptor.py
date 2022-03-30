#Add libraries we need
import os
import pathlib
from typing import Any

#Add Darcy AI libraries we need, particularly the ImageClassificationPerceptor base class and the Config and ConfigRegistry classes
from darcyai.perceptor.coral.image_classification_perceptor import ImageClassificationPerceptor
from darcyai.config import Config
from darcyai.config_registry import ConfigRegistry
from darcyai.utils import validate_not_none, validate_type, validate

#Add our FaceMaskDetectionModel class for POM-compatible output
from face_mask_detection_model import FaceMaskDetectionModel


#Define our custom Perceptor class called "FaceMaskPerceptor"
class FaceMaskPerceptor(ImageClassificationPerceptor):
    """
    This class is a subclass of ImageClassificationPerceptor.
    It is used to detect face mask in an image.
    """

    #Define our "init" method
    def __init__(self, threshold:float=0.95):
        #Get the directory of the code file and find the AI model file
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, "face_mask_detection.tflite")

        #Set up our own text labels for AI output so we don't need a labels.txt file
        labels = {
            0: "No Mask",
            1: "Mask",
        }

        #Validate input parameters
        validate_not_none(threshold, "threshold is required")
        validate_type(threshold, (float, int), "threshold must be a number")
        validate(0 <= threshold <= 1, "threshold must be a number between 0 and 1")

        #Call "init" on the parent class and pass our AI model information
        super().__init__(model_path=model_file,
                         threshold=0,
                         top_k=2,
                         labels=labels)

        #Add a configuration item to the list, in this case a threshold setting that is a floating point value
        #This will show up in the configuration REST API
        self.config_schema = [
            Config("threshold", "float", threshold, "Threshold"),
        ]


    #Define our "run" method
    def run(self, input_data:Any, config:ConfigRegistry=None) -> FaceMaskDetectionModel:
        """
        This function is used to run the face mask detection.

        Arguments:
            input_data (Any): RGB array of the face.
            config (ConfigRegistry): The configuration.

        Returns:
            FaceMaskDetectionModel: The face mask detection model.
        """
        #Get the AI model result by calling "run" on the parent class where we have already passed our AI model
        perception_result = super().run(input_data=input_data, config=config)

        #Check the output to see if the mask detection crosses the configured threshold
        if len(perception_result[1]) == 0:
            has_mask = False
        else:
            idx = perception_result[1].index("Mask")
            has_mask = perception_result[0][idx][1] >= self.get_config_value("threshold")

        #Wrap the result in the POM-compatible class and send it out
        return FaceMaskDetectionModel(has_mask)
