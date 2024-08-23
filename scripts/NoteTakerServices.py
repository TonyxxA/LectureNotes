import os
from dotenv import load_dotenv

# Anthropic
import anthropic
from anthropic.types.message import Message as AnthropicChatCompletion

# OpenAI
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion

from .NoteTakerPrompts import PROMPTS, ANTHROPIC_PROMPTS

from .prices import ANTHROPIC_INPUT_TOKEN_PRICE, ANTHROPIC_OUTPUT_TOKEN_PRICE

from .prices import (
    OPENAI_GPT40MINI_INPUT_TOKEN_PRICE,
    OPENAI_GPT40MINI_OUTPUT_TOKEN_PRICE,
)


class NoteTakerAnthropicService:
    # MODEL_NAME = "claude-3-5-sonnet-20240620"
    MODEL_NAME = "claude-3-haiku-20240307"

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)

        self.input_token_price = ANTHROPIC_INPUT_TOKEN_PRICE
        self.output_token_price = ANTHROPIC_OUTPUT_TOKEN_PRICE

        self.input_tokens = 0
        self.output_tokens = 0
        self.total_cost = 0

    def _calculate_conversation_cost(
        self, input_tokens: int, output_tokens: int
    ) -> float:
        return round(
            (
                input_tokens * self.input_token_price
                + output_tokens * self.output_token_price
            )
            / 1.0e6,
            4,
        )

    def _update_tracking_stats(self, message: AnthropicChatCompletion):
        self.input_tokens += message.usage.input_tokens
        self.output_tokens += message.usage.output_tokens
        self.total_cost += self._calculate_conversation_cost(
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )

    def _prompt_api(
        self, prompt_type: str, transcript: str, max_tokens: int
    ) -> AnthropicChatCompletion:

        prompt = ANTHROPIC_PROMPTS[prompt_type]

        conversation_report = self.client.messages.create(
            model=self.MODEL_NAME,
            system=prompt["system"],
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt["user"].format(transcript=transcript),
                },
                {"role": "assistant", "content": prompt["assistant"]},
            ],
            temperature=prompt["temperature"],
            stream=False,
        )

        # adding the assistant prompt to the conversation report text
        conversation_report.content[0].text = (
            prompt["assistant"] + conversation_report.content[0].text
        )
        return conversation_report

    def _prompt_key_points_and_action_items(
        self, transcript: str
    ) -> AnthropicChatCompletion:
        return self._prompt_api("key_points", transcript, 1000)

    def _prompt_detailed_notes(self, transcript: str) -> AnthropicChatCompletion:
        return self._prompt_api("detailed_notes", transcript, 4096)

    def _prompt_executive_summary(self, transcript: str) -> AnthropicChatCompletion:
        return self._prompt_api("executive_summary", transcript, 2000)

    def _prompt_study_guide(self, transcript: str) -> AnthropicChatCompletion:
        return self._prompt_api("study_guide", transcript, 4096)

    def take_notes(self, transcript: str) -> tuple[str, str, str, float, int, int]:
        conversation_report = self._prompt_key_points_and_action_items(
            transcript=transcript
        )
        self._update_tracking_stats(conversation_report)
        key_points_and_actions = conversation_report.content[0].text

        conversation_report = self._prompt_detailed_notes(transcript=transcript)
        self._update_tracking_stats(conversation_report)
        detailed_notes = conversation_report.content[0].text

        conversation_report = self._prompt_executive_summary(transcript=transcript)
        self._update_tracking_stats(conversation_report)
        executive_summary = conversation_report.content[0].text

        conversation_report = self._prompt_study_guide(transcript=transcript)
        self._update_tracking_stats(conversation_report)
        study_guide = conversation_report.content[0].text

        return (
            executive_summary,
            detailed_notes,
            key_points_and_actions,
            study_guide,
            self.total_cost,
            self.input_tokens,
            self.output_tokens,
        )


class NoteTakerOpenAIService:
    MODEL_NAME = "gpt-4o-mini"

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

        self.input_token_price = OPENAI_GPT40MINI_INPUT_TOKEN_PRICE
        self.output_token_price = OPENAI_GPT40MINI_OUTPUT_TOKEN_PRICE

        self.input_tokens = 0
        self.output_tokens = 0
        self.total_cost = 0

    def _calculate_conversation_cost(
        self, input_tokens: int, output_tokens: int
    ) -> float:
        return round(
            (
                input_tokens * self.input_token_price
                + output_tokens * self.output_token_price
            )
            / 1.0e6,
            4,
        )

    def _update_tracking_stats(self, message: OpenAIChatCompletion):
        self.input_tokens += message.usage.prompt_tokens
        self.output_tokens += message.usage.completion_tokens

        self.total_cost += self._calculate_conversation_cost(
            input_tokens=message.usage.prompt_tokens,
            output_tokens=message.usage.completion_tokens,
        )

    def _prompt_api(
        self, prompt_type: str, transcript: str, max_tokens: int
    ) -> OpenAIChatCompletion:

        prompt = ANTHROPIC_PROMPTS[prompt_type]

        conversation_report = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": prompt["system"],
                },
                {
                    "role": "user",
                    "content": prompt["user"].format(transcript=transcript),
                },
                {"role": "assistant", "content": prompt["assistant"]},
            ],
            max_tokens=max_tokens,
            temperature=prompt["temperature"],
        )

        # adding the assistant prompt to the conversation report text
        conversation_report.choices[0].message.content = (
            prompt["assistant"] + conversation_report.choices[0].message.content
        )
        return conversation_report

    def _prompt_key_points_and_action_items(
        self, transcript: str
    ) -> OpenAIChatCompletion:
        return self._prompt_api("key_points", transcript, 1000)

    def _prompt_detailed_notes(self, transcript: str) -> OpenAIChatCompletion:
        return self._prompt_api("detailed_notes", transcript, 16384)

    def _prompt_executive_summary(self, transcript: str) -> OpenAIChatCompletion:
        return self._prompt_api("executive_summary", transcript, 2000)

    def _prompt_study_guide(self, transcript: str) -> OpenAIChatCompletion:
        return self._prompt_api("study_guide", transcript, 16384)

    def take_notes(self, transcript: str) -> tuple[str, str, str, float, int, int]:
        conversation_report = self._prompt_key_points_and_action_items(
            transcript=transcript
        )
        self._update_tracking_stats(conversation_report)
        key_points_and_actions = conversation_report.choices[0].message.content

        conversation_report = self._prompt_detailed_notes(transcript=transcript)
        self._update_tracking_stats(conversation_report)
        detailed_notes = conversation_report.choices[0].message.content

        conversation_report = self._prompt_executive_summary(transcript=transcript)
        self._update_tracking_stats(conversation_report)
        executive_summary = conversation_report.choices[0].message.content

        conversation_report = self._prompt_study_guide(transcript=transcript)
        self._update_tracking_stats(conversation_report)
        study_guide = conversation_report.choices[0].message.content

        return (
            executive_summary,
            detailed_notes,
            key_points_and_actions,
            study_guide,
            self.total_cost,
            self.input_tokens,
            self.output_tokens,
        )


if __name__ == "__main__":
    from NotesTextGeneratorServices import NotesTextGeneratorService
    from DocumentParserServices import HTMLToWordParser, HTMLToPDFParser

    title = "Test Lecture Notes"
    word_doc_path = "Samples/" + title + ".docx"
    pdf_doc_path = "Samples/" + title + ".pdf"
    made_up_duration = 3613.2

    with open("Samples/sample_transcript.txt", "r") as file:
        transcript = file.read()

    # note_taker = NoteTakerAnthropicService()
    note_taker = NoteTakerOpenAIService()

    (
        executive_summary,
        detailed_notes,
        key_points_and_actions,
        study_guide,
        total_cost,
        input_tokens,
        output_tokens,
    ) = note_taker.take_notes(transcript=transcript)

    HTML_notes_generator = NotesTextGeneratorService()
    HTML_notes = HTML_notes_generator.generate_content_HTML_text(
        title,
        [executive_summary, detailed_notes, key_points_and_actions, study_guide],
        lecture_duration_sec=made_up_duration,
        LLM_input_tokens=input_tokens,
        LLM_output_tokens=output_tokens,
        notes_cost=total_cost,
        appendix=[{"Subtitle": "Transcript", "Content": transcript}],
    )

    document_parser = HTMLToWordParser()
    document_parser.convert_html_to_word(html_text=HTML_notes, word_file=word_doc_path)

    document_parser = HTMLToPDFParser()
    document_parser.convert_html_to_pdf(html_text=HTML_notes, pdf_file=pdf_doc_path)

    print("Done!")
