#!/usr/bin/python
# coding=utf8

import sys


COMPLIMENTS = {
    "不錯": 1,
    "nice": 2,
    "good": 3,
    "very good": 4,
    "很清楚": 5,
    "很好": 6,
    "excellent": 7,
    "讚啦": 8,
    "太讚": 9,
    "brilliant": 10
}

COMPLAINTS = {
    "don't understand": -1,
    "聽不懂": -2,
    "bad": -3,
    "鳥": -4,
    "sucks": -5,
    "爛": -6,
    "hell": -7,
    "無言": -8,
    "bollocks": -9,
    "超爛": -10
}

LECTURERS = (
    "Isabel", "Amy", "Alexis", "Lily", "Kelly",
    "Bob", "Pitt", "Alen", "Aaron", "Brian",
    "Ian", "Henry"
)

def main():
    for line in sys.stdin:
        line = line.strip().split(',')
        student = line[0]
        age = line[1]
        district = line[2]
        comments = line[3]
        lecturer = ''
        score = 0

        for lec in LECTURERS:
            if lec in comments:
                lecturer = lec
                for compliment, compliment_score in COMPLIMENTS.iteritems():
                    if compliment in comments:
                        score = compliment_score
                        break
                if score == 0:
                    for complaint, complaint_score in COMPLAINTS.iteritems():
                        if complaint in comments:
                            score = complaint_score
                            break
                break

        print '\t'.join((lecturer, ','.join((student, age, district, str(score)))))

if __name__ == '__main__':
    main()
