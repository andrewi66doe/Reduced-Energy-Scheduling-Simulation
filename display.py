import argparse
from graphics import *
from scheduler import load_tasks, schedule, task_set_interval
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
    def __init__(self, schedule, num_tasks, max_x=100, max_y=100):
        self.schedule = schedule
        self.max_x = max_x
        self.max_y = max_y
        self._get_schedule_interval()
        self.window = GraphWin(width=800, height=600)
        self.window.setCoords(0, 0, self.max_x, self.max_y)
        self.margin = 4
        self.num_tasks = num_tasks

    def _get_schedule_interval(self):
        self.schedule.sort(key=lambda x: x.start)
        max_time = self.schedule[-1].task.b
        min_time = self.schedule[0].start
        self.schedule_start = min_time
        self.schedule_end = max_time

    def draw_schedule(self):
        x_axis = Line(Point(self.margin, self.margin), Point(self.max_x - self.margin, self.margin))
        y_axis = Line(Point(self.margin, self.margin), Point(self.margin, self.max_y - self.margin))

        interval = (self.max_x - 2*self.margin) / self.schedule_end
        spacing = self.max_x / self.num_tasks

        step = int(self.schedule_end / 5)

        for z in range(0, int(ceil(self.schedule_end)) + 1, step):
            pa = Point((z * interval) + self.margin, self.margin-1.5)
            tick_label = Text(pa, str(z))
            tick_label.draw(self.window)

        i = 0
        self.schedule.sort(key=lambda x: x.task.name, reverse=True)
        last_block = self.schedule[0].task.name

        for sb in self.schedule:
            if sb.task.name != last_block:
                i += 1
                last_block = sb.task.name
            deadline = sb.task.b
            release = sb.task.a
            dla = Point((deadline * interval) + self.margin, i * spacing + self.margin)
            dlb = Point((deadline * interval) + self.margin, (i * spacing) + (spacing / self.margin) + self.margin)
            ra = Point((release * interval) + self.margin, i * spacing + self.margin)
            rb = Point((release * interval) + self.margin, (i * spacing) + (spacing / self.margin) + self.margin)

            release_l = Line(ra, rb)
            color_rgb(0, 0, 255)
            release_l.setFill('green')
            release_l.setArrow('last')
            release_l.draw(self.window)
            deadline_l = Line(dla, dlb)
            deadline_l.setFill('black')
            deadline_l.setArrow('first')
            deadline_l.draw(self.window)

            label = Text(Point(self.margin-2, (i * spacing) + (spacing / self.margin) + 4) , sb.task.name)
            label.draw(self.window)
            bl = Point(self.margin + (sb.start * interval), i * spacing + self.margin)
            ur = Point(self.margin + ((sb.start * interval) + (sb.duration * interval)), (i * spacing) + (spacing / self.margin) + self.margin)
            rect = Rectangle(bl, ur)
            rect_color = color_rgb(int(255 * sb.execution_speed), int(255 * (1 - sb.execution_speed)), 0)
            rect.setFill(rect_color)
            rect.draw(self.window)
            l = Line(Point(self.margin, i * spacing + self.margin), Point(self.max_x - 1, i * spacing + self.margin))
            l.draw(self.window)
        x_axis.draw(self.window)
        y_axis.draw(self.window)
        self.window.getMouse()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulation of a low power scheduling algorithm.")
    parser.add_argument('filename', type=str, help='Name of input file')
    args = parser.parse_args()
    tasks, num_tasks = load_tasks(args.filename)
    a, b = task_set_interval(tasks)

    s = schedule(tasks)
    for t in s:
        print("Schedule task {0} at time {1:.2f} for {2:.2f}"
              " time units with {3:.2f}% processing speed".format(t.task.name,
                                                                  t.start,
                                                                  t.duration,
                                                                  t.execution_speed * 100))
    plotter = SchedulePlotter(s, num_tasks)
    plotter.draw_schedule()
