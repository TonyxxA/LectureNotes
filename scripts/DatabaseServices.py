import os
from dotenv import load_dotenv
import sqlite3


class DatabaseServices:
    """
    A class that provides database services for the notes database.

    Each note has the following attributes:
    - title (str): The title of the note.
    - summary (str): The summary of the note.
    - category (str): The category of the note.
    - recording_path (str): The path to the recording file associated with the note.
    - notes_path (str): The path to the notes file associated with the note.
    - created_at (timestamp): The timestamp when the note was created.
    """

    def __init__(
        self,
        name: str = "notesDatabase.db",
    ) -> None:

        # Load environment variables
        load_dotenv()

        self.database_location = os.getenv("DATABASE_LOCATION")

        # Create database directory if it doesn't exist
        os.makedirs(self.database_location, exist_ok=True)

        self.database_path = os.path.join(self.database_location, name)

        self._init_db()

        pass

    def _init_db(self):
        """
        Initializes the database by creating the 'notes' table if it doesn't exist.

        The 'notes' table has the following columns:
        - id: INTEGER (Primary Key)
        - title: TEXT
        - summary: TEXT
        - category: TEXT
        - recording_path: TEXT
        - notes_path: TEXT
        - created_at: TIMESTAMP (Default: Current Timestamp)
        """

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT,
                summary TEXT,
                category TEXT,
                recording_path TEXT,
                notes_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def save_note_to_db(
        self,
        title: str,
        summary: str,
        category: str,
        recording_path: str,
        notes_path: str,
    ):
        """
        Saves a note to the database.

        Parameters:
        - title (str): The title of the note.
        - summary (str): The summary of the note.
        - category (str): The category of the note.
        - recording_path (str): The path to the recording file associated with the note.
        - notes_path (str): The path to the notes file associated with the note.
        """
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO notes (title, summary, category, recording_path, notes_path)
        VALUES (?, ?, ?, ?, ?)
        """,
            (title, summary, category, recording_path, notes_path),
        )
        conn.commit()
        conn.close()


if __name__ == "__main__":
    pass
