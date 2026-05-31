from abc import ABC, abstractmethod
import json

#Abstract class 
class Vehicle(ABC):
    def __init__(self, name, price_per_day):      
        self.name = name
        self.price_per_day =price_per_day

        self.available = True
        self.rent_count = 0

    def rent(self):
        if self.available:
            self.available = False
            self.rent_count += 1

            self.write_log(f"{self.name} rented")

            print(f"{self.name} rented successfully")

        else:
            print(f"{self.name} is not available")

    def return_vehicle(self):
        self.available = True

    def write_log(self, message):

        with open("rental.log", "a") as file:
            file.write(message + "\n")

    @abstractmethod
    def calculate_rent(self, days):
        pass


#Car Class
class Car(Vehicle):
    def calculate_rent(self, days):
        
        total = self.price_per_day * days
    #discount
        if self.rent_count > 3:
            total *= 0.9

        return total
#truck class
class Truck(Vehicle):
    def calculate_rent(self, days):
        
        total = self.price_per_day * days

        if self.rent_count > 3:
            total *= 0.85

        return total
    
#Bike class
class Bike(Vehicle):
    def calculate_rent(self, days):
        
        total = self.price_per_day * days

        if self.rent_count > 3:
            total *= 0.95

        return total
    
#Fleet Manager
class FleetManager: 
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def show_all_vehicles(self):
        for vehicle in self.vehicles:
            print({
                "name": vehicle.name,
                "type": vehicle.__class__.__name__,
                "available": vehicle.available,
                "rent_count": vehicle.rent_count    
            })

 #Search by name
    def search_by_name(self, name):

        for vehicle in self.vehicles:
            if vehicle.name.lower() == name.lower():
                return vehicle
            
        return None
 #Search by type
    def search_by_type(self,vehicle_type):
        result = []

        for vehicle in self.vehicles:
            if vehicle.__class__.__name__.lower() == vehicle_type.lower():
                result.append(vehicle)

        return result
 #Search by Price
    def search_by_price(self, max_price):
        result = []

        for vehicle in self.vehicles:
            if vehicle.price_per_day <= max_price:
                result.append(vehicle)

        return result
    
    def load_from_json(self):

        with open("vehicles.json", "r") as file:
            data = json.load(file)

        for item in data:
            vehicle_type = item["type"]

            if vehicle_type == "Car":
                vehicle = Car(
                    item["name"],
                    item["price_per_day"])
            
            elif vehicle_type == "Truck":
                vehicle = Truck(
                    item["name"],
                    item["price_per_day"])
            
            else:
                vehicle = Bike(
                    item["name"],
                    item["price_per_day"])
            
            vehicle.available = item["available"]
            vehicle.rent_count = item["rent_count"]

            self.vehicles.append(vehicle)
        
        print("Data loaded from Json")

    

manager = FleetManager()
car1 = Car("BMW", 100)

manager.add_vehicle(car1)

manager.show_all_vehicles()