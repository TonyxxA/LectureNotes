import os
from datetime import timedelta

from flask import Flask, request, render_template, send_file, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

from scripts.DatabaseServices import DatabaseServices
from scripts.SecurityServices import SecurityServices
from scripts.AudioTranscriberServices import LocalAudioTranscriberService
from scripts.NoteTakerServices import NoteTakerAnthropicService, NoteTakerOpenAIService
from scripts.NotesTextGeneratorServices import NotesTextGeneratorService
from scripts.DocumentParserServices import HTMLToWordParser, HTMLToPDFParser

app = Flask(__name__)

limiter = Limiter(
    get_remote_address, app=app, default_limits=["200 per day", "50 per hour"]
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/authenticate", methods=["POST"])
@limiter.limit("5 per minute")
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    security_service = SecurityServices()
    if not security_service.check_auth(username, password):
        return jsonify({"success": False, "message": "Authentication failed"}), 401

    if not security_service.check_ip(request.remote_addr):
        return jsonify({"success": False, "message": "Access denied"}), 403

    session["authenticated"] = True
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

    return jsonify({"success": True})


@app.route("/upload", methods=["POST"])
@limiter.limit("5 per minute")
def upload():
    if not session.get("authenticated"):
        return jsonify({"message": "Not authenticated"}), 401

    os.makedirs("Uploads", exist_ok=True)

    file = request.files["file"]
    filename = file.filename
    file_path = os.path.join("Uploads", filename)
    file.save(file_path)

    audio_transcriber = LocalAudioTranscriberService(TRANSCRIBTION_MODEL)
    transcript, duration = audio_transcriber.transcribe_audio(file_path)

    note_taker = NoteTakerOpenAIService()
    (
        executive_summary,
        detailed_notes,
        key_points_and_actions,
        study_guide,
        notes_total_cost,
        input_tokens,
        output_tokens,
    ) = note_taker.take_notes(transcript=transcript["text"])

    os.makedirs("Notes", exist_ok=True)
    title = filename.split(".")[0]
    word_doc_path = os.path.join("Notes", f"{title}.docx")
    pdf_path = os.path.join("Notes", f"{title}.pdf")

    word_doc_notes_generator = NotesTextGeneratorService()
    notes_text = word_doc_notes_generator.generate_content_HTML_text(
        title,
        [executive_summary, detailed_notes, key_points_and_actions, study_guide],
        lecture_duration_sec=duration,
        LLM_input_tokens=input_tokens,
        LLM_output_tokens=output_tokens,
        notes_cost=notes_total_cost,
        appendix=[{"Subtitle": "Transcript", "Content": transcript["text"]}],
    )

    document_parser = HTMLToWordParser()
    document_parser.convert_html_to_word(notes_text, word_doc_path)

    # Generate PDF
    pdf_parser = HTMLToPDFParser()
    pdf_parser.convert_html_to_pdf(notes_text, pdf_path)

    db_service.save_note_to_db(
        filename, executive_summary, "Lecture", file_path, word_doc_path
    )

    # Return both Word and PDF files
    return jsonify(
        {"word_doc": f"/download/word/{title}", "pdf": f"/download/pdf/{title}"}
    )


@app.route("/download/word/<title>")
def download_word(title):
    word_doc_path = os.path.join("Notes", f"{title}.docx")
    return send_file(word_doc_path, as_attachment=True, download_name=f"{title}.docx")


@app.route("/download/pdf/<title>")
def download_pdf(title):
    pdf_path = os.path.join("Notes", f"{title}.pdf")
    return send_file(pdf_path, as_attachment=True, download_name=f"{title}.pdf")


if __name__ == "__main__":
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY")

    TRANSCRIBTION_MODEL = "tiny.en"

    DATABASE_NAME = "notesDatabase.db"
    db_service = DatabaseServices(DATABASE_NAME)

    app.run(host="0.0.0.0", port=5002)
