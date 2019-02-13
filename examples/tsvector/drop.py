from .model import Company
from ..common import Database


if __name__ == "__main__":
    db = Database(echo=True)
    db.drop_table(Company)
