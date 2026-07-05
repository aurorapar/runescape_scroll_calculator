from datetime import datetime

from .jobs.handle_data import handle_data
from .spreadsheeting.create_scroll_chances import create_scroll_spreadsheet

def main():
    handle_data()
    create_scroll_spreadsheet()

if __name__ == "__main__":
    main()