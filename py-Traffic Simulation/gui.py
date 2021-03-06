import tkinter as tk
import constants

import random
import math

def frac(n, total):
    return 360 * n / total if n < total else 359.9


class ConsoleGUI():
    def __init__(self):
        super(ConsoleGUI, self).__init__()

    def update_car(self, car):
        print("X {} - Y {}".format(car.x, car.y))


class TkinterGUI():
    def __init__(self, city, processor):
        self.city = city
        self.processor = processor
        self.frame = MainFrame(city, self)
        self.cars_map = {}
        self.fading_accident_list = []

        self.refresh()

    def update(self, cars, delta_t):
        for car in cars:
            self.frame.update_car(car, self.cars_map)
        self.frame.update_accidents(delta_t)
        self.frame.menu_frame.update_arrival_label()
        self.frame.menu_frame.update_delta_t_label(delta_t)
        self.frame.menu_frame.update_total_label(
            self.processor.simulation_time)

        cars = len(self.processor.agents)

        self.frame.menu_frame.update_cars_label(cars)
        self.frame.menu_frame.update_pie_chart(cars, self.city.arrivals,
                                               self.city.accidents)
        self.refresh()

    def refresh(self):
        self.frame.update_idletasks()
        self.frame.update()

    def start(self):
        self.frame.draw_city()

    def remove_agent(self, agent):
        spot = self.cars_map.get(agent.id)
        if spot:
            self.frame.delete_agent(spot)


class MenuFrame(tk.Frame):
    def __init__(self, parent, city):
        tk.Frame.__init__(self, parent)
        self.city = city

        self.custom_amount = tk.StringVar()
        self.custom_amount.set('0')

        # To avoid movement of this frame. It's like a width parameter
        self.label = tk.Label(self, text='Traffic-Sym', font=(None, 40), fg='red')
        self.label.pack(side=tk.TOP)

        self.init_stats_menu()
        self.init_pie_chart()
        self.init_controls_menu()

    def init_stats_menu(self):
        self.stats_label = tk.Label(self, text='Status', font=(None, 40))
        self.stats_label.pack(side=tk.TOP)

        self.accident_label = tk.Label(
            self,
            text='Accidents: {}'.format(self.city.accidents),
            font=(None, 20))
        self.accident_label.pack(pady=5)

        self.arrival_label = tk.Label(
            self,
            text='Safe Arrivals: {}'.format(self.city.accidents),
            font=(None, 20))
        self.arrival_label.pack(pady=5)

        self.delta_t_label = tk.Label(self, text='FPS: ', font=(None, 20))
        self.delta_t_label.pack(pady=5)

        self.total_label = tk.Label(self, text='Simulation Time: ', font=(None, 20))
        self.total_label.pack(pady=5)

        self.cars_label = tk.Label(self, text='Cars: ', font=(None, 20))
        self.cars_label.pack(pady=5)

    def init_controls_menu(self):
        self.label = tk.Label(self, text='Menu', font=(None, 40))
        self.label.pack(side=tk.TOP)

        self.pause_button = tk.Button(
            self, text='STOP', command=self.pause_pressed)
        self.pause_button.pack(pady=5)

        self.add_button = tk.Button(
            self, text='Add Car', command=self.city.add_random_agent)
        self.add_button.pack(pady=5)

        self.add_boost_button = tk.Button(
            self,
            text='Run {} Cars'.format(
                int(self.city.vertical_roads_count +
                    self.city.horizontal_roads_count)),
            command=self.city.add_multiple_agents)
        self.add_boost_button.pack(pady=5)

        self.add_super_boost_button = tk.Button(
            self,
            text='Run {} Cars'.format(
                int(self.city.vertical_roads_count +
                    self.city.horizontal_roads_count) * 5),
            command=self.city.add_times_multiple_agents)
        self.add_super_boost_button.pack(pady=5)

        container = tk.Frame(self, height=2)
        container.pack(pady=5)

        tk.Entry(
            container, textvariable=self.custom_amount).grid(
                row=0, column=0)

        self.add_custom_button = tk.Button(
            container,
            text='Simulate'.format(
                int(self.city.vertical_roads_count +
                    self.city.horizontal_roads_count) * 5),
            command=self.add_custom_agents)
        self.add_custom_button.grid(row=0, column=1)

    def add_custom_agents(self):
        try:
            value = int(self.custom_amount.get())
            if value > 0:
                self.city.add_custom_agents(value)
        except ValueError as e:
            pass
        self.custom_amount.set('0')

    def init_pie_chart(self):
        container = tk.Frame(self, height=2)
        container.pack(pady=10)

        self.pie_chart = tk.Canvas(container, width=100, height=100)
        xy = 10, 10, 100, 100
        self.pie_chart.grid(rowspan=4, columnspan=6)

        self.accidents_portion = self.pie_chart.create_arc(xy, fill="#860000")
        self.arrived_portion = self.pie_chart.create_arc(xy, fill="#008D17")
        self.remain_portion = self.pie_chart.create_arc(
            xy, fill="#002486", start=0, extent=359.9)

        self.travelling_portion_label = tk.Label(
            container,
            text='Travelling 100.00%',
            font=(None, 12, 'bold'),
            fg="#002486")
        self.travelling_portion_label.grid(row=1, column=6)
        self.accidents_portion_label = tk.Label(
            container,
            text='Accidents 0.00%',
            font=(None, 12, 'bold'),
            fg="#860000")
        self.accidents_portion_label.grid(row=2, column=6)
        self.arrived_portion_label = tk.Label(
            container,
            text='Arrivals 0.00%',
            font=(None, 12, 'bold'),
            fg="#008D17")
        self.arrived_portion_label.grid(row=3, column=6)

    def pause_pressed(self):
        self.city.pause()
        self.pause_button.config(text='Resume'
                                 if self.pause_button.cget("text") == 'Pause'
                                 else "Pause")

    def update_accidents_label(self):
        self.accident_label.config(
            text='Accidents: {}'.format(self.city.accidents))

    def update_arrival_label(self):
        self.arrival_label.config(
            text='Safe Arrivals: {}'.format(self.city.arrivals))

    def update_delta_t_label(self, delta_t):
        self.delta_t_label.config(text='FPS: {:.3f}'.format(delta_t))

    def update_total_label(self, s_time):
        self.total_label.config(text='Time: {:.1f}s'.format(s_time))

    def update_cars_label(self, quantity):
        self.cars_label.config(text='Cars: {}'.format(quantity))

    def update_pie_chart(self, cars, arrivals, accidents):
        total = cars + arrivals + accidents
        if total > 0:
            self.pie_chart.itemconfig(
                self.arrived_portion,
                start=frac(0, total),
                extent=frac(arrivals, total))
            self.arrived_portion_label.config(text="Arrivals {:.2f}%".format(
                100 * arrivals / total))

            self.pie_chart.itemconfig(
                self.accidents_portion,
                start=frac(arrivals, total),
                extent=frac(accidents, total))
            self.accidents_portion_label.config(
                text="Accidents {:.2f}%".format(100 * accidents / total))

            self.pie_chart.itemconfig(
                self.remain_portion,
                start=frac(accidents + arrivals, total),
                extent=frac(cars, total))
            self.travelling_portion_label.config(
                text="Travelling {:.2f}%".format(100 * cars / total))


class CityFrame(tk.Frame):
    def __init__(self, parent, city, manager):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.city = city
        self.manager = manager

        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def draw_city(self):
        self.w = self.canvas.winfo_width()
        self.h = self.canvas.winfo_height()

        self.margin_w = self.w * constants.MARGIN / 2
        self.margin_h = self.h * constants.MARGIN / 2

        self.w *= (1 - constants.MARGIN)
        self.h *= (1 - constants.MARGIN)

        self.rel_x = self.w / self.city.width
        self.rel_y = self.h / self.city.height

        for i in range(self.city.horizontal_roads_count):
            pos = (i * self.city.block_height_size * self.rel_y
                   ) + self.margin_h
            self.canvas.create_rectangle(
                self.margin_w - constants.ROAD_WIDTH / 2,
                pos - constants.ROAD_WIDTH / 2,
                self.w + self.margin_w + constants.ROAD_WIDTH / 2,
                pos + constants.ROAD_WIDTH / 2,
                fill="gray",
                outline='grey')

        for i in range(self.city.vertical_roads_count):
            pos = (i * self.city.block_width_size * self.rel_x) + self.margin_w
            self.canvas.create_rectangle(
                pos - constants.ROAD_WIDTH / 2,
                self.margin_h,
                pos + constants.ROAD_WIDTH / 2,
                self.h + self.margin_h,
                fill="gray",
                outline='grey')

    def get_drawing_position_car(self, car):
        return self.get_drawing_position(car.navigation_manager.x,
                                         car.navigation_manager.y)

    def get_drawing_position(self, x, y):
        mapped_x = x * self.rel_x + self.margin_w
        mapped_y = y * self.rel_y + self.margin_h
        return (mapped_x, mapped_y)

    def update_car(self, car, cars_map):
        spot = cars_map.get(car.id)
        if spot:
            self.canvas.delete(spot[0])
        color = self.get_speed_color(car)
        pos = self.get_drawing_position_car(car)
        #points = [150, 100, 200, 120, 240, 180, 210, 200, 150, 150, 100, 200]
        #id_ = self.canvas.create_polygon(points, outline='#f11', fill='#1f1', width=2)
        id_ = self.canvas.create_rectangle(
            pos[0] - constants.CAR_RADIUS,
            pos[1] - constants.CAR_RADIUS,
            pos[0] + constants.CAR_RADIUS,
            pos[1] + constants.CAR_RADIUS,
            fill=color,outline='#f11')
        cars_map[car.id] = (id_, color)

    def update_accidents(self, delta_t):
        self.parent.menu_frame.update_accidents_label()
        for each in self.city.accidents_list[:]:
            (c1, c2) = self.city.accidents_list.pop()
            x, y = self.get_drawing_position(
                (c1.navigation_manager.x + c2.navigation_manager.x) / 2,
                (c1.navigation_manager.y + c2.navigation_manager.y) / 2)
            r = 3 * constants.CAR_RADIUS
            id_ = self.canvas.create_oval(
                x - r, y - r, x + r, y + r, fill='red')
            self.manager.fading_accident_list.append([id_, (x, y), r])
        self.draw_fading_accidents(delta_t)

    def draw_fading_accidents(self, delta_t):
        for each in self.manager.fading_accident_list[:]:
            self.canvas.delete(each[0])
            x, y = each[1]
            r = each[2]
            each[2] = each[2] - 10 * delta_t
            if each[2] < 0:
                self.canvas.delete(each[0])
                self.manager.fading_accident_list.remove(each)
            else:
                id_ = self.canvas.create_oval(
                    x - r, y - r, x + r, y + r, fill='red')
                each[0] = id_

    def delete_agent(self, spot):
        self.canvas.delete(spot[0])

    def get_speed_color(self, car):
        speed = math.sqrt(car.navigation_manager.speed_x**2 +
                          car.navigation_manager.speed_y**2)
        speed = speed / self.city.get_max_speed()
        if speed > 1:
            speed = 1
        base_FF_speed = int(speed * 255)
        invert_FF_speed = int(255 - base_FF_speed)
        return "#00" + "{:02x}".format(base_FF_speed) + "{:02x}".format(
            invert_FF_speed)


class MainFrame(tk.Frame):
    def __init__(self, environment, manager):
        tk.Frame.__init__(self)
        self.city = environment
        self.manager = manager

        self.init_main_frame()

        self.city_frame = CityFrame(self, self.city, self.manager)
        self.menu_frame = MenuFrame(self, self.city)

        self.city_frame.pack(fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)
        self.menu_frame.pack(fill=tk.BOTH, expand=tk.NO, side=tk.RIGHT)

    def init_main_frame(self):
        self.master.title("AUTO - Self Driving-Cars")

        # Full Windows Size
        self.master.geometry("{0}x{1}+0+0".format(
            self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def draw_city(self):
        self.city_frame.draw_city()

    def delete_agent(self, spot):
        self.city_frame.delete_agent(spot)

    def update_car(self, car, car_map):
        self.city_frame.update_car(car, car_map)

    def update_accidents(self, delta_t):
        self.city_frame.update_accidents(delta_t)
