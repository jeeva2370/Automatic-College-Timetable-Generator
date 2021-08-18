import random
import collections



# create a list of subject in string format and Dictonary->this have a no of times a subject in week

class Timetable:
    def __init__(self, course):
        self.course = course
    def timetable(self):
        while True:
            try:
                temp = []
                z = []
                arr = []
                D = {}
                courses = []
                c1 = {}
                d1 = {}
                cols = 7
                for lo, loi in enumerate(self.course):
                    # loi+=1
                    courses.append(self.course[lo]['course'])
                    D[self.course[lo]['course']] = self.course[lo]['contact_hours']
                # print(D)
                # print(courses)

                for i in range(5):
                    col = []
                    for j in range(35):
                        # j+=0
                        rid = random.randrange(len(courses))
                        if courses[rid] not in col:
                            col.append(courses[rid])

                    arr.append(col)
                #     print(col)
                # print(arr)
                courses.clear()
                # counts the no. of times subjects repeated in randomly generated 2d list
                ci = collections.Counter()
                for a in arr:
                    ci.update(a)
                C = dict(ci)
                # print(C)

                # sort the dictonary with keys
                for c in sorted(C):
                    c1[c] = C[c]
                # print(c1)
                for d in sorted(D):
                    d1[d] = D[d]
                # print(d1)

                D.clear()
                I1 = []

                I2 = []
                # create a list of subjects from sorted dictonary
                for w in c1:
                    I2.append(w)
                # print(I2)
                # create list that have the repeatation of subject that wants to delete
                for d, c in zip(d1.values(), c1.values()):
                    if d == c:
                        z.append(0)
                    if d != c:
                        z.append(abs(d - c))
                # print('z')
                # print(z)
                c1.clear()
                d1.clear()
                count = []
                n = None
                # this will delete the subjects form table
                for i, l in zip(I2, z):
                    for s, t1 in enumerate(arr):
                        if i in t1:
                            # print(s,t1.index(i))
                            I1.append([s, t1.index(i)])
                            temp.append([s, t1.index(i)])
                    # print('l'+ str(l))
                    for j in range(l):
                        # print('*----------*')
                        # print(j)
                        rd = random.randrange(len(temp))
                        n = rd
                        # print('n'+str(n))

                        if n in count:
                            # print('true')
                            if (rd + 1) > (len(temp) - 1):
                                rd -= 1

                            else:
                                rd += 1
                        count.append(rd)
                        # print('cont'+str(count))
                        k = temp[rd][1]
                        # print(rd,k)
                        # print(arr[rd][k])
                        del (arr[rd][k])
                        # print('-----------------')
                        n = None
                    count.clear()
                    temp.clear()
                z.clear()

                # print(arr)
                # get the index of subject that exceeds the column size

                g = []

                for u, v in enumerate(arr):
                    # print(u,v)
                    for b in v:
                        # print(b,v.index(b))
                        if v.index(b) >= cols:
                            # print(v.index(b))
                            g.append([u, v.index(b)])
                # print(g)

                # to rearrange the column size
                for u1 in arr:
                    for G, G1 in enumerate(g):

                        # print(len(u1))
                        # print(u1)
                        # print(G1)
                        t = G1[0]
                        t1 = G1[1]
                        if len(u1) < cols:
                            # print(t,t1)
                            u1.append(arr[t][t1])
                            del (arr[t][t1])

                # print(arr)
                g.clear()
                for q, n in enumerate(arr):
                    for e in n:
                        for f in self.course:
                            if e == f["course"]:
                                #    print(e)
                                #    print(n.index(e))
                                arr[q][n.index(e)] = f
                            #    print(f)

                return arr

            except Exception:
                arr.clear()

                continue
            else:
                break

def generate(sem,y1,y2,y3,y4=''):
    if sem=='even':
        year1=Timetable(y1).timetable()
        year2=Timetable(y2).timetable()
        year3=Timetable(y3).timetable()
        return year1,year2,year3
    elif sem == 'odd':
        year1=Timetable(y1).timetable()
        year2=Timetable(y2).timetable()
        year3=Timetable(y3).timetable()
        year4=Timetable(y4).timetable()
        return year1,year2,year3,year4
# Y1=[{'course': 'Technical English', 'contact_hours': 5, 'staff': 'A', 'credits': '4'}, {'course': 'Engineering Mathematics-II', 'contact_hours': 5, 'staff': 'B', 'credits': '4'}, {'course': 'Physics for Information Science', 'contact_hours': 4, 'staff': 'CC', 'credits': '3'}, {'course': 'Basic Electrical,Electronics and Measurement Engineering', 'contact_hours': 4, 'staff': 'G', 'credits': '3'}, {'course': 'Environmental Science and Engineering', 'contact_hours': 4, 'staff': 'D', 'credits': '3'}, {'course': 'Programming in C', 'contact_hours': 5, 'staff': 'H', 'credits': '3'}, {'course': 'Engineering Practices Laboratory', 'contact_hours': 4, 'staff': 'I', 'credits': '2'}, {'course': 'C Programming Laboratory', 'contact_hours': 4, 'staff': 'H', 'credits': '2'}]
# firstsem=Timetable(course=Y1).timetable()
# print('firstyear',firstsem)