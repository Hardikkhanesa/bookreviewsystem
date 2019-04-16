import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine('postgres://nysqtbkbaoexhh:04dccd0f6c64186ca6b9d49f288b49b85930ea913d560828c79aa5fe4fd1e256@ec2-54-221-201-212.compute-1.amazonaws.com:5432/d6v3stt6deu3s5');

db = scoped_session(sessionmaker(bind=engine))


def main():
    f=open("books.csv")
    reader = csv.reader(f);
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",{"isbn":isbn,"title":title,"author":author,"year":year})
        print(f"Added Books of {title} ");
    db.commit()

if __name__=="__main__":
    main()

#def main():
#   f = open("flights.csv")
#    reader = csv.reader(f)
#   for origin, destination, duration in reader:
#        db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
#                    {"origin": origin, "destination": destination, "duration": duration})
#        print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
#    db.commit()