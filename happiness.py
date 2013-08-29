from collections import defaultdict
import csv


FIRST_CHOICE = 10
SECOND_CHOICE = 1
INFINITY = -100000000000000

MAX_NUM_PER_LAB = 5
MAX_NUM_PER_DISC = 1
MAX_NUM_PER_OH = 3

class Section(object):

    def __init__(self, name, num_allowed, ta):
        self.name = name
        self.num_allowed = num_allowed
        self.ta = ta
        self.las = []


class LabAssistant(object):

    def __init__(self, name, first_choices, second_choices, cant_make, preferred_tas, num_labs, num_discussions, num_office_hours):
        self.name = name
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
    def wants_more_labs(self):
        return len(self.labs) < self.num_labs

    @property
    def wants_more_discs(self):
        return len(self.discussions) < self.num_discussions

    @property
    def wants_more_office_hours(self):
        return len(self.office_hours) < self.num_office_hours

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

    def wants_lab(self, lab):
        return lab not in self.labs and lab.name in self.first_choices

    def wants_disc(self, disc):
        return disc not in self.discussions and disc.name in self.first_choices

    def wants_oh(self, oh):
        return oh not in self.office_hours and oh.name in self.first_choices

    def add_labs(self, labs):
        for lab in labs:
            if self.wants_more_labs and self.wants_lab(lab):
                self.labs.append(lab)

    def add_discs(self, discs):
        for disc in discs:
            if self.wants_more_discs and self.wants_disc(disc):
                self.discussions.append(disc)

    def add_ohs(self, ohs):
        for oh in ohs:
            if self.wants_more_office_hours and self.wants_oh(oh):
                self.office_hours.append(oh)

def int_or_zero(num):
    if num == '':
        return 0
    return int(num)

def parsed(line):
    timestamp, name, email, num_unit, num_discussions, num_oh, first_labs, second_labs, cant_labs, first_discs, second_discs, cant_discs, oh_times, preferred_tas, _, num_labs = line

    first_choices = str(first_labs + ', ' + first_discs + ', ' + oh_times).split(', ')
    second_choices = str(second_labs + ', ' + second_discs).split(', ')
    cant_make = str(cant_labs + ', ' + cant_discs).split(', ')
    preferred_tas = preferred_tas.split(', ')

    first_labs = first_labs.split(', ')
    second_labs = second_labs.split(', ')

    first_discs = first_discs.split(', ')
    second_discs = second_discs.split(', ')
    ohs = oh_times.split(', ')

    return [name, first_choices, second_choices, cant_make, preferred_tas, int_or_zero(num_labs), int_or_zero(num_discussions), int_or_zero(num_oh)], [first_labs + second_labs, first_discs + second_discs, ohs]

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
#            if num > 2:
 #               break
            per_line = parsed(line)
            labs.update(set(per_line[1][0]))
            discs.update(set(per_line[1][1]))
            office_hours.update(set(per_line[1][2]))
            la.append(LabAssistant(*per_line[0]))
            num += 1
    return la, list(map(list, (labs, discs, office_hours)))

def maximize(lab_assistants, labs, discs, ohs):
    for la in lab_assistants:
        la.add_labs(labs)
        la.add_discs(discs)
        la.add_ohs(ohs)

    labs = defaultdict(list)
    discs = defaultdict(list)
    ohs = defaultdict(list)

    total_happy = 0
    for la in lab_assistants:
        total_happy += la.happiness

        for lab in la.labs:
            labs[lab].append(la.name)

        for disc in la.discussions:
            discs[disc].append(la.name)

        for oh in la.office_hours:
            ohs[oh].append(la.name)

    return total_happy, labs, discs, ohs

def make_labs(lab):
    sections = []
    for ta in lab_to_ta[lab]:
        sections.append(Section(lab, 5, ta))
    return sections

def make_discs(disc):
    discussions = []
    for ta in disc_to_ta[disc]:
        discussions.append(Section(disc, 2, ta))
    return discussions

def make_ohs(oh):
    ohs = []
    for ta in oh_to_ta[oh]:
        ohs.append(Section(oh, 4, ta))
    return ohs

def map_tas(filename):
    mappings = defaultdict(lambda: defaultdict(list))
    with open(filename, 'rU') as filename:
        output = csv.reader(filename, delimiter=',')
        for line in output:
            type_of_section, ta, section_time = line
            mappings[type_of_section][section_time].append(ta)
    return mappings['lab'], mappings['disc'], mappings['oh']

def flatten(unflattened):
    items = []
    for item in unflattened:
        if isinstance(item, list):
            items.extend(flatten(item))
        else:
            items.append(item)
    return items

if __name__ == '__main__':
    lab_to_ta, disc_to_ta, oh_to_ta = map_tas('sections.csv')


    la, (labs, discs, ohs) = read_file('responses.csv')
    labs = flatten(list(map(make_labs, labs)))
    discs = flatten(list(map(make_discs, discs)))
    ohs = flatten(list(map(make_ohs, ohs)))
    total_happy, labs, discs, ohs = maximize(la, labs, discs, ohs)

    for lab, las in labs.iteritems():
        print lab.name, las
        print ''

