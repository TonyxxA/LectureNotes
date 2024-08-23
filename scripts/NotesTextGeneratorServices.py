from datetime import datetime
import re


class NotesTextGeneratorService:
    def __init__(self):
        pass

    def remove_thinking(self, text):
        # Function to extract and print thinking content
        def print_thinking(match):
            print("Thinking content:")
            print(match.group(1).strip())
            print()  # Add a blank line after each thinking content
            return ""  # Remove the thinking tag from the text

        # Remove thinking tags and print their content
        processed_text = re.sub(
            r"<thinking>(.*?)</thinking>", print_thinking, text, flags=re.DOTALL
        )

        return processed_text

    def generate_content_HTML_text(
        self, title: str, main_content: list[str], **kwargs
    ) -> str:

        # Parse Keyword Arguments for Nerd Info
        nerd_info = []
        if "lecture_duration_sec" in kwargs:
            lecture_duration_sec = kwargs["lecture_duration_sec"]
            nerd_info.append(
                f"<li>Lecture Duration: {lecture_duration_sec // 60} min {round(lecture_duration_sec % 60, 1)} sec</li>"
            )

        if "LLM_input_tokens" in kwargs:
            LLM_input_tokens = kwargs["LLM_input_tokens"]
            nerd_info.append(f"<li>LLM Input Tokens: {LLM_input_tokens}</li>")

        if "LLM_output_tokens" in kwargs:
            LLM_output_tokens = kwargs["LLM_output_tokens"]
            nerd_info.append(f"<li>LLM Output Tokens: {LLM_output_tokens}</li>")

        if "transcription_cost" in kwargs:
            transcription_cost = kwargs["transcription_cost"]
            nerd_info.append(f"<li>Transcription Cost: ${transcription_cost}</li>")

        total_cost = 0
        for key, value in kwargs.items():
            if "cost" in key and (type(value) == float or type(value) == int):
                total_cost += value

        if total_cost:
            nerd_info.append(f"<li>Total Cost: ${total_cost}</li>")

        if nerd_info:
            nerd_info.insert(
                0,
                f"<li>Generated on: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}</li>",
            )

        # Parse keyword arguments for Appendix
        appendix = []
        if "appendix" in kwargs:
            appendix_items = kwargs["appendix"]
            for section in appendix_items:
                appendix.append(
                    f"<h2>{section['Subtitle']}</h2><p>{section['Content']}</p>"
                )

        ## Construct content text

        content_text = f"""<!DOCTYPE html>\n<html lang="en">\n\n<head>\n\t<meta charset="UTF-8">\n\t<title>{title}</title>\n</head>\n\n"""

        content_text += "<body>\n"
        if nerd_info:
            content_text += (
                "<h1>Nerd Info</h1>\n"
                + "<ul>\n\t"
                + "\n\t".join(nerd_info)
                + "\n</ul>\n"
            )

        content_text += "".join(main_content)

        if appendix:
            content_text += "\n<h1>Appendix</h1>\n" + "\n".join(appendix)

        content_text += "\n</body>\n</html>"

        # Remove thinking tags and print their content
        content_text = self.remove_thinking(content_text)

        return content_text


if __name__ == "__main__":

    pass
