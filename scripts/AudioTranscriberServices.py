from pydub import AudioSegment
import whisper
import torch


class LocalAudioTranscriberService:
    def __init__(self, model_name: str = "tiny.en"):
        self.model_name = model_name
        pass

    def get_audio_duration(self, audio_file_path: str):
        """
        Get the duration of an audio file in seconds.

        Parameters:
        audio_file_path (str): The path to the audio file.

        Returns:
        float: The duration of the audio file in seconds.
        """
        audio = AudioSegment.from_file(audio_file_path)
        return audio.duration_seconds

    def transcribe_audio(self, audio_file_path: str) -> tuple[str, float]:
        """
        Transcribes the audio file located at the given file path.

        Args:
            audio_file_path (str): The file path of the
            audio file to transcribe.
        """

        duration = self.get_audio_duration(audio_file_path)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = whisper.load_model(self.model_name, device=device)

        audio = whisper.load_audio(audio_file_path)
        result = model.transcribe(audio)

        return result, duration


if __name__ == "__main__":
    pass
