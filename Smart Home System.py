from abc import ABC, abstractmethod
import json
from datetime import datetime
import matplotlib.pyplot as plt

class Device(ABC):
    def __init__(self, name, power_per_hour):
        self.name= name
        self.is_on = False
        self.power_per_hour = power_per_hour
        self.total_hours = 0

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} turned on")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} turned off")

    def calculate_energy(self):
        return  self.power_per_hour * self.total_hours
    
    @abstractmethod
    def status_report(self):
        pass


class Light(Device):
    def status_report(self):
        print({
            "device": self.name,
            "type": "Light",
            "status": self.is_on,
            "energy": self.calculate_energy()
        })  
        

class Thermostat(Device):
    def __init__(self, name, power_per_hour):
        super().__init__(name, power_per_hour) #parent classga murojat qilyabmiz

        self.temperature = 25
    def set_temperature(self, value):
        self.temperature = value

    def status_report(self):
        print({
            "device": self.name,
            "type": "Thermostat",
            "temperature": self.temperature,
            "status": self.is_on
        })

class Camera(Device):
    def status_report(self):
        print({
            "device": self.name,
            "type": "Camera",
            "status": self.is_on
        })    

class Alarm(Device):
    def status_report(self):
        print({
            "device": self.name,
            "type": "Alarm",
            "status": self.is_on
        })

class Fan(Device):
    def status_report(self):
        print({
            "device": self.name,
            "type": "Fan",
            "status": self.is_on
        })

class TemperatureObserver:
    def __init__(self, fan):
        self.fan = fan
    
    def update(self, temperature):
        if temperature > 30:
            if not self.fan.is_on:
                self.fan.turn_on()

                print("Fan automatically turned on")

class SmartHomeController:
    def __init__(self):
        self.devices = []
        self.temperature_history = []
        self.observers = []

    def add_device(self, device):
        self.devices.append(device)

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, temperature):
        for observer in self.observers:
            observer.update(temperature)

    def show_all_status(self):
        for device in self.devices:
            device.status_report()

    def save_devices(self):
        data =[]
        for device in self.devices:
            info = {
                "name": device.name,
                "type": device.__class__.__name__,
                "is_on": device.is_on,
                "power_per_hour": device.power_per_hour,
                "total_hours": device.total_hours
            }

            data.append(info)

        with open("devices.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Devices saved")

    def load_devices(self):
        with open("devices.json", "r") as file:
            data = json.load(file)

        for item in data:
            device_type = item["type"]

            if device_type == "Thermostat":
                device = Thermostat(
                    item["name"],
                    item["power_per_hour"])

                device.temperature = item["temperature"]

            elif device_type == "Camera":
                device = Camera(
                    item["name"],
                    item["power_per_hour"])

            elif device_type == "Alarm":
                device = Alarm(
                    item["name"],
                    item["power_per_hour"])

            else:
                device = Fan(
                    item["name"],
                    item["power_per_hour"])

            device.is_on = item["is_on"]
            device.total_hours = item["total_hours"]

            self.devices.append(device)

        print("Devices loaded")
    
    def update_temperature(self, thermostat, temperature):
        thermostat.set_temperature(temperature)
        self.temperature_history.append(temperature)
        self.notify_observers(temperature)

    def plot_temperature_graph(self):
        plt.plot(self.temperature_history)
        plt.xlabel("Time")
        plt.ylabel("Temperature")
        plt.title("Temperature Graph")
        plt.show()

class SmartHomeCLI:

    def __init__(self):

        self.controller = SmartHomeController()

        self.thermostat = Thermostat("Main Thermostat", 2500)

        self.fan = Fan("Cooling Fan", 3000)

        self.controller.add_device(self.thermostat)
        self.controller.add_device(self.fan)

        observer = TemperatureObserver(self.fan)

        self.controller.add_observer(observer)

    def run(self):

        while True:

            print("\n1. Add Light")
            print("2. Show Devices")
            print("3. Update Temperature")
            print("4. Save JSON")
            print("5. Load JSON")
            print("6. Plot Temperature")
            print("7. Exit")

            choice = input("Choose: ")

            if choice == "1":

                name = input("Light name: ")

                light = Light(name, 1)

                self.controller.add_device(light)

            elif choice == "2":

                self.controller.show_all_status()

            elif choice == "3":

                temp = int(input("Temperature: "))

                self.controller.update_temperature(
                    self.thermostat, temp)

            elif choice == "4":

                self.controller.save_devices()

            elif choice == "5":

                self.controller.load_devices()

            elif choice == "6":

                self.controller.plot_temperature_graph()

            elif choice == "7":

                break


cli = SmartHomeCLI()
cli.run()