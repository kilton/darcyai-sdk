#Add libraries we need
import os
import pathlib
from typing import Any

#Add Darcy AI libraries we need, particularly the ObjectDetectionPerceptor base class and the Config and ConfigRegistry classes
from darcyai.perceptor.coral.object_detection_perceptor import ObjectDetectionPerceptor
from darcyai.config import Config
from darcyai.config_registry import ConfigRegistry
from darcyai.utils import validate_not_none, validate_type, validate


#Define our custom Perceptor class called "FaceDetector"
class FaceDetector(ObjectDetectionPerceptor):
    """
    Detect faces in an image.
    """

    #Define our "init" method
    def __init__(self, threshold:float=0.95):
        #Get the directory of the code file and find the AI model file
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, "ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite")

        #Validate input parameters
        validate_not_none(threshold, "threshold is required")
        validate_type(threshold, (float, int), "threshold must be a number")
        validate(0 <= threshold <= 1, "threshold must be a number between 0 and 1")

        #Call "init" on the parent class and pass our AI model information
        super().__init__(model_path=model_file,
                         threshold=0)

        #Add a configuration item to the list, in this case a threshold setting that is a floating point value
        #This will show up in the configuration REST API
        self.config_schema = [
            Config("threshold", "float", threshold, "Threshold"),
        ]


    #Define our "run" method
    def run(self, input_data:Any, config:ConfigRegistry=None) -> Any:
        """
        This function is used to run the face detection.

        Arguments:
            input_data (Any): RGB array of the image.
            config (ConfigRegistry): The configuration.

        Returns:
            Any: The face detection result.
        """
        #Get the AI model result by calling "run" on the parent class where we have already passed our AI model
        perception_result = super().run(input_data=input_data, config=config)

        #Create an empty result array and then fill it by checking all results against the configured threshold
        result = []
        if len(perception_result) and len(perception_result[0]) > 0:
            for detection in perception_result[0]:
                if detection.id == 0 and detection.score >= config.threshold:
                    result.append(detection)

        #Send out our filtered results
        return result
