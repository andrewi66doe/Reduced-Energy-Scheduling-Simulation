from graphics import *
from main import load_tasks, schedule, task_set_interval
from math import ceil


def plot_tasks(tasks):
    schedule = []
    elapsed = 0

    for task in tasks:
        if task.a > elapsed:
            schedule.append((task, task.a, task.r, 1))
            elapsed += (task.a - elapsed)
        else:
            schedule.append((task, elapsed, task.r, 1))
            elapsed += task.r + task.a

    plotter = SchedulePlotter(schedule)
    plotter.draw_schedule()


class SchedulePlotter:
    def __init__(self, schedule, max_x=100, max_y=100):
        self.schedule = schedule
        self.max_x = max_x
        self.max_y = max_y
        self._get_schedule_interval()
        self.window = GraphWin(width=800, height=600)
        self.window.setCoords(0, 0, self.max_x, self.max_y)
        self.margin = 4

    def _get_schedule_interval(self):
        self.schedule.sort(key=lambda x: x.task.b)
        max_time = self.schedule[-1].start + self.schedule[-1].duration

        min_time = self.schedule[0].start
        self.schedule_start = min_time
        self.schedule_end = max_time

    def draw_schedule(self):
        x_axis = Line(Point(self.margin, self.margin), Point(self.max_x - self.margin, self.margin))
        y_axis = Line(Point(self.margin, self.margin), Point(self.margin, self.max_y- self.margin))

        interval = (self.max_x - 2*self.margin) / self.schedule_end
        spacing = self.max_x / len(self.schedule)

        for z in range(0, ceil(self.schedule_end) + 1, 5000):
            pa = Point((z * interval) + self.margin, self.margin-1.5)
            tick_label = Text(pa, str(z))
            tick_label.draw(self.window)

        for i, sb in enumerate(sorted(self.schedule, key=lambda x: x.task.name, reverse=True)):
            deadline = sb.task.b
            release = sb.task.a
            dla = Point((deadline * interval) + self.margin, i * spacing + self.margin)
            dlb = Point((deadline * interval) + self.margin, (i * spacing) + (spacing / self.margin) + self.margin)
            ra = Point((release * interval) + self.margin, i * spacing + self.margin)
            rb = Point((release * interval) + self.margin, (i * spacing) + (spacing / self.margin) + self.margin)

            release_l = Line(ra, rb)
            release_l.setFill('green')
            release_l.setArrow('last')
            release_l.draw(self.window)
            deadline_l = Line(dla, dlb)
            deadline_l.setFill('red')
            deadline_l.setArrow('first')
            deadline_l.draw(self.window)

            label = Text(Point(self.margin-2, (i * spacing) + (spacing / self.margin) + 4) , sb.task.name)
            label.draw(self.window)
            bl = Point(self.margin + (sb.start * interval), i * spacing + self.margin)
            ur = Point(self.margin + ((sb.start * interval) + (sb.duration * interval)), (i * spacing) + (spacing / self.margin) + self.margin)
            rect = Rectangle(bl, ur)
            rect.draw(self.window)
            l = Line(Point(self.margin, i * spacing + self.margin), Point(self.max_x - 1, i * spacing + self.margin))
            l.draw(self.window)
        x_axis.draw(self.window)
        y_axis.draw(self.window)
        self.window.getMouse()


if __name__ == "__main__":
    tasks = load_tasks("input.txt")
    a, b = task_set_interval(tasks)

    s = schedule(tasks)
    for t in s:
        print("Schedule task {0} at time {1:.2f} for {2:.2f}"
              " time units with {3:.2f}% processing speed".format(t.task.name,
                                                                  t.start,
                                                                  t.duration,
                                                                  t.execution_speed * 100))
    plotter = SchedulePlotter(s)
    plotter.draw_schedule()
