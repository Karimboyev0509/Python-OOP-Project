from datetime import date
import json

def vip_discount(my_function):
    def wrapper(customer, room, days):
        price = my_function(customer, room, days)

        if customer.is_vip:
            return price * 0.8 
        
        return price   
    return wrapper



class Room:
    def __init__(self, number, price, amenities, location):
        self.number = number
        self.price = price
        self.amenities = amenities
        self.location = location
        self.booked_days = []

    def is_available(self, start, end):

        for b_start, b_end in self.booked_days:

            if start <= b_end and end >= b_start:
                return False    

        return True
    
    def get_price(self, days):
        return self.price * days
    

class DeluxeRoom(Room):
    def get_price(self, days):
        return self.price * days
    
class VipRoom(Room):
    def get_price(self, days):
        return self.price * days
    

class Customer:
    def __init__(self, name, is_vip= False):
        self.name = name
        self.is_vip =is_vip

class Booking:
    def __init__(self, customer, room, start, end):
        self.customer = customer
        self.room = room
        self.start = start
        self.end = end
        self.total_price = 0

class Hotel:
    def __init__(self):
        self.rooms = []
        self.bookings = []

    def add_room(self, room):
        self.rooms.append(room)

    def book_room(self, customer, room_number, start, end):
        
        for room in self.rooms:
            if room.number == room_number:
                if room.is_available(start, end):
                    days = (end - start).days
                    price = calculate_price(customer, room, days)
                    booking = Booking(customer, room, start, end)
                    booking.total_price += price

                    room.booked_days.append((start, end))
                    self.bookings.append(booking)

                    self.log_booking(customer, room, price)
                    print(f"Booked successfully. Price: {price}")

                    return booking
                
        print("Room not available")


    def log_booking(self, customer, room, price):
        with open("booking.log", "a") as f:
            f.write(f"{customer.name} booked Room {room.number} - {price}\n")

    
    def revenue_report(self):
        total = 0
        for b in self.bookings:
            total += b.total_price

        print("Total Revenue:", total )

@vip_discount
def calculate_price(customer, room , days):
    return room.get_price(days)

hotel = Hotel()
room1 = Room(101, 100, ["WiFi", "AC"], "Tashkent")
hotel.add_room(room1)
        
        
c1 = Customer("Muhammadkarim", is_vip=True)


hotel.book_room(c1, 101, date(2026, 5, 1), date(2026, 5, 5))

hotel.revenue_report()
