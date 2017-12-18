import pandas as pd

if __name__ == "__main__":
    etutor = pd.read_csv("../data/etutor_db.csv")
    ps = pd.read_csv("../data/ps10.csv")

    grades = ps.copy()
    vals = grades.get_values()

    l = []
    for val in vals:
        last = val[0].split(',')[0]
        q = etutor.query('Last == "{}"'.format(last))
        if len(q) > 0:
            v = q.get_values()[0, 4]
            print v
            l.append(str(v))
        else:
            print "No id"
            l.append("")
    ps["id"] = l
    ps.to_csv('../data/ps10_withid.csv')
