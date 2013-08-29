import csv


FIRST_CHOICE = 10
SECOND_CHOICE = 1
INFINITY = -100000000000000

MAX_NUM_PER_LAB = 5
MAX_NUM_PER_DISC = 1
MAX_NUM_PER_OH = 3

class LabAssistant(object):

    def __init__(self, first_choices, second_choices, cant_make, preferred_tas, num_labs, num_discussions, num_office_hours):
        self.first_choices = first_choices
        self.second_choices = second_choices
        self.cant_make = cant_make
        self.preferred_tas = preferred_tas
        self.num_labs = num_labs
        self.num_discussions = num_discussions
        self.num_office_hours = num_office_hours
        self.labs = []
        self.office_hours = []
        self.discussions = []

    @property
    def wants_labs(self):
        return self.num_labs != 0

    @property
    def wants_discussions(self):
        return self.num_discussions != 0

    @property
    def wants_office_hours(self):
        return self.num_office_hours != 0

    @property
    def happiness(self):
        total = 0
        total += self.happiness_of(self.labs)
        total += self.happiness_of(self.discussions)
        total += self.happiness_of(self.office_hours)
        return total

    def happiness_of(self, items):
        total = 0
        for item in items:
            if item in self.first_choices:
                total += FIRST_CHOICE
            elif item in self.second_choices:
                total += SECOND_CHOICE
            else:
                total += INFINITY
        return total

def parsed(line):
    timestamp, name, email, num_unit, num_discussions, num_oh, first_labs, second_labs, cant_labs, first_discs, second_discs, cant_discs, oh_times, preferred_tas, _, num_labs = line

    first_choices = str(first_labs + ', ' + first_discs).split(', ')
    second_choices = str(second_labs + ', ' + second_discs).split(', ')
    cant_make = str(cant_labs + ', ' + cant_discs).split(', ')
    preferred_tas = preferred_tas.split(', ')

    first_labs = first_labs.split(', ')
    second_labs = second_labs.split(', ')

    first_discs = first_discs.split(', ')
    second_discs = second_discs.split(', ')
    ohs = oh_times.split(', ')

    return [first_choices, second_choices, cant_make, preferred_tas, int(num_labs), int(num_discussions), int(num_oh)], [first_labs + second_labs, first_discs + second_discs, ohs]

def read_file(filename):
    la = []
    labs = set()
    discs = set()
    office_hours = set()
    with open(filename, 'rb') as filename:
        output = csv.reader(filename, delimiter=',')
        num = 0
        for line in output:
            if num == 0:
                num += 1
                continue
            if num > 2:
                break
            per_line = parsed(line)
            labs.update(set(per_line[1][0]))
            discs.update(set(per_line[1][1]))
            office_hours.update(set(per_line[1][2]))
            print per_line
            la.append(LabAssistant(*per_line[0]))
            num += 1
    return la, list(map(list, (labs, discs, office_hours)))

def maximize(lab_assistants, labs, discs, ohs):
    

    total_happy = 0
    for la in lab_assistants:
        total_happy += la.happiness
    return total_happy

if __name__ == '__main__':
    la, (labs, discs, ohs) = read_file('responses.csv')
    print maximize(la, labs, discs, ohs)
