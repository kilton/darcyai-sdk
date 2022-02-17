import audioop
import math
import numpy as np
import pyaudio

from darcyai.input.input_stream import InputStream
from darcyai.stream_data import StreamData
from darcyai.utils import timestamp, validate_type, validate_not_none, validate

class AudioInputStream(InputStream):
    """
    AudioInputStream is an input stream that reads audio data from a microphone.

    # Arguments
    chunk_size: The size of the audio data chunk.
        Defaults to 1024.
    format: The format of the audio data.
        Defaults to pyaudio.paFloat32.
    sample_len_sec: The length of the audio sample in seconds.
        Defaults to 5.
    """
    def __init__(self,
                 chunk_size: int = 1024,
                 format: str = pyaudio.paFloat32,
                 sample_len_sec: int = 5):

        validate_not_none(chunk_size, "chunk_size must be provided")
        validate_type(chunk_size, int, "chunk_size must be an integer")
        validate(chunk_size > 0, "chunk_size must be greater than 0")
        self.__chunk_size = chunk_size

        validate_not_none(format, "format must be provided")
        validate_type(format, int, "format must be an integer")
        self.__format = format

        validate_not_none(sample_len_sec, "sample_len_sec must be provided")
        validate_type(sample_len_sec, int, "sample_len_sec must be an integer")
        validate(sample_len_sec > 0, "sample_len_sec must be greater than 0")
        self.__sample_len_sec = sample_len_sec
        
        self.__audio_stream = None
        self.__stopped = True
        self.__threshold = 30000

        self.__pyaudio = pyaudio.PyAudio()
        self.__input_device_index = self.__pyaudio.get_default_input_device_info()["index"]
        self.__channels = self.__pyaudio.get_default_input_device_info()["maxInputChannels"]
        self.__rate = int(self.__pyaudio.get_device_info_by_index(self.__input_device_index)["defaultSampleRate"])


    def stop(self):
        """
        Stops the audio stream.
        """
        self.__stopped = True
        if self.__audio_stream is not None:
            self.__audio_stream.stop_stream()
            self.__audio_stream.close()


    def stream(self):
        """
        Starts the audio stream.
        """
        self.__audio_stream = self.__pyaudio.open(
                                     format=self.__format,
                                     channels=self.__channels,
                                     rate=self.__rate,
                                     input=True,
                                     output=False,
                                     frames_per_buffer=self.__chunk_size,
                                     input_device_index=self.__input_device_index)
        self.__stopped = False

        while not self.__stopped:
            frames = []
            for i in range(0, int(self.__rate / self.__chunk_size * self.__sample_len_sec)):
                data = self.__audio_stream.read(self.__chunk_size, exception_on_overflow=False)
                frames.append(data)

            data = b"".join(frames)
            avg = math.sqrt(abs(audioop.avg(data, 4)))
            if avg < self.__threshold:
                yield StreamData(data, timestamp())
            else:
                print("Silence detected")

    def get_sample_rate(self):
        """
        Returns the sample rate of the audio stream.

        # Returns
        The sample rate of the audio stream.
        """
        return self.__rate
