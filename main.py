from database import Database
from analysis import analysis

DATABASE_NAME = "sehaj1104/student-productivity-and-digital-distraction-dataset"

if __name__ == "__main__":
    db = Database(DATABASE_NAME)
    db.download()
    db.read()

    analysis(db.get_dataset())
