import numpy
import matplotlib.pyplot as plt
import sqlite3
import database_manager

def main():
    db = database_manager.DatabaseManager()
    db.connect()
    x = db.avg_histogram()
    plt.hist(x, bins=30, alpha=0.5)
    plt.title("Photo-average")
    plt.xlabel("Average")
    plt.ylabel("Number of photos")
    plt.show()
    db.close()


if __name__ == "__main__":
        main()