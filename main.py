import re
from math import floor, ceil


class Task:
    def __init__(self, name, a, b, r):
        self.name = name
        self.a = int(a)
        self.b = int(b)
        self.r = int(r)

    def interval(self):
        return self.a, self.b

    def interval_len(self):
        return self.b - self.a

    def __repr__(self):
        return "<{} ({}, {}, {})>".format(self.name,
                                          self.a,
                                          self.b,
                                          self.r)


class SchedulingBlock:
    def __init__(self, task, start, duration, execution_speed):
        self.task = task
        self.start = start
        self.duration = duration
        self.execution_speed = execution_speed


def load_tasks(filename):
    tasks = []
    file = open(filename, "r")
    lines = file.readlines()
    num_tasks = int(lines[0].strip())

    for line in lines[1:]:
        if re.match('.*\s*\(\d*,\s*\d*,\s\d*\)', line):
            name, a, b, r = (line.replace("(", " ").replace(")", " ").replace(",", " ")).split()
            task = Task(name, a, b, r)
            tasks.append(task)
        else:
            print("Parse Error: {}".format(line))
    return tasks, num_tasks


def task_set_interval(task_set):
    a_values = [x.a for x in task_set]
    b_values = [x.b for x in task_set]

    return min(a_values), max(b_values)


def tasks_in_interval(a, b, tasks):
    in_interval = set()

    for task in tasks:
        if task.a >= a and task.b <= b:
            in_interval.add(task)
    return in_interval


# O(n^2) algorithm for finding critical group
def find_critical_group(task_set, time):
    isets = []

    a_vals = [ti.a for ti in task_set]
    b_vals = [ti.b for ti in task_set]

    a_vals.sort()
    b_vals.sort()
    max_idx = 0
    max_g = 0
    i = 0

    for a in a_vals:
        for b in filter(lambda x: x > a, b_vals):
            iset = tasks_in_interval(a, b, task_set)
            if iset:
                iset_interval = b - a
                g_val = sum(task.r for task in iset) / iset_interval
                if max_g <= g_val <= 1:
                    max_g = g_val
                    max_idx = i
                # print("{0} \t{1} \t{2:.2f}".format(a, b, g_val), end=" ")
                # print(iset)
                i += 1
                isets.append(iset)
    return max_g, set(isets[max_idx])


def get_ready_at_time(task_set, t):
    return set(filter(lambda x: x.a <= t, task_set))


def get_earliest_deadline(task_set):
    return min(task_set, key=lambda x: x.b)


def edf(task_set, g):
    f_schedule = []
    task_set = set(list(task_set))

    # Modify run time of each task to run for the allotted speed
    for task in task_set:
        task.r /= g
        task.r = floor(task.r)

    elapsed = 0

    while task_set:
        ready_tasks = get_ready_at_time(task_set, elapsed)

        if ready_tasks:
            scheduled_task = get_earliest_deadline(ready_tasks)
            scheduled_task.r -= 1
            if scheduled_task.r == 0:
                task_set -= {scheduled_task}
            f_schedule.append(SchedulingBlock(scheduled_task, elapsed, 1, g))
        elapsed += 1

    return f_schedule


def schedule(initial_task_set):

    f_schedule = []
    time = 0

    total = 0
    task_set = set(initial_task_set)

    # While the original task set still has members
    while task_set:
        # Find the critical group of tasks
        g, critical_group = find_critical_group(task_set, time)
        a, b = task_set_interval(critical_group)
        print("#" * 20)
        print("Critical Group {} \t{}\n".format(g, critical_group))
        #total += sum(task.r/g for task in critical_group)

        # Remove the critical group from the original set
        task_set -= critical_group

        sched = edf(critical_group, g)
        f_schedule += sched
        # Revise deadlines and arrival times for remaining tasks
        for t in task_set:
            if a <= t.b <= b:
                t.b = a
            elif t.b > b:
                 t.a = b
            if a <= t.a <= b:
                t.a = b
            elif t.a > b:
                 t.a -= (b-a)


        print(task_set)
    return f_schedule


if __name__ == "__main__":
    taskset = load_tasks("cheng.txt")
    schedule = schedule(taskset)
    for t in schedule:
        task, start, duration, g = t
        print("Schedule task {0} at time {1:.2f} for {2:.2f} time units with {3:.2f}% processing speed".format(task.name, start, duration, g*100))
