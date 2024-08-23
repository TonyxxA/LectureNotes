import pypandoc


class HTMLToWordParser:

    REFERENCE_STYLE = "Samples/custom-reference.docx"

    def __init__(self) -> None:
        pass

    def convert_html_to_word(self, html_text: str, word_file: str) -> None:
        """
        Convert an HTML file to a Word document.

        Args:
            html_file (str): The path to the HTML file.
            word_file (str): The path to save the Word document.

        Returns:
            None
        """

        # Configure the options for pandoc
        options = [
            "--pdf-engine=xelatex",
            "--mathjax",
            "-V",
            "geometry:margin=1in",
            "--standalone",
            "--from",
            "html+tex_math_dollars",
            "--extract-media=.",
            f"--reference-doc={self.REFERENCE_STYLE}",
        ]

        # Convert HTML to DOCX
        pypandoc.convert_text(
            html_text,
            "docx",
            format="html",
            outputfile=word_file,
            extra_args=options,
        )


class HTMLToPDFParser:

    def __init__(self) -> None:
        pass

    def convert_html_to_pdf(self, html_text: str, pdf_file: str) -> None:
        """
        Convert an HTML file to a PDF document.

        Args:
            html_file (str): The path to the HTML file.
            pdf_file (str): The path to save the PDF document.

        Returns:
            None
        """

        # Configure the options for pandoc
        options = [
            "--pdf-engine=xelatex",
            "--mathjax",
            "-V",
            "geometry:margin=1in",
            "--standalone",
            "--from",
            "html+tex_math_dollars",
            "--top-level-division=chapter",
        ]

        # Convert HTML to PDF
        pypandoc.convert_text(
            html_text,
            "pdf",
            format="html",
            outputfile=pdf_file,
            extra_args=options,
        )


if __name__ == "__main__":

    title = "Test Lecture Notes2"
    word_doc_path = "Samples/" + title + ".docx"
    pdf_doc_path = "Samples/" + title + ".pdf"
    made_up_duration = 3613.2

    with open("Samples/sample_HTML_notes_text.txt", "r") as file:
        transcript = file.read()

    document_parser = HTMLToWordParser()
    document_parser.convert_html_to_word(transcript, word_doc_path)

    document_parser = HTMLToPDFParser()
    document_parser.convert_html_to_pdf(transcript, pdf_doc_path)
