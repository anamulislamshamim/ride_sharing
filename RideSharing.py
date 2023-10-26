from abc import ABC, abstractclassmethod
from datetime import datetime


class Ride_Sharing:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
        self.drivers = []
        self.riders = []
        self.rides = []
    
    def add_rider(self, rider):
        self.riders.append(rider)
    
    def add_drivers(self, driver):
        self.drivers.append(driver)
    
    def __repr__(self) -> str:
        return f"Name: {self.company_name}\nDrivers: {len(self.drivers)}\nRiders: {len(self.riders)}"


class User(ABC):
    def __init__(self, name, email, nid) -> None:
        self.name = name
        self.email = email 
        # TODO: set user id dynamically
        self.__id = 0
        self.__nid = nid 
        self.wallet = 0
    
    @abstractclassmethod
    def display_profile(self):
        raise NotImplemented
   

class Rider(User):
    def __init__(self, name, email, nid, current_location, initial_amount) -> None:
        super().__init__(name, email, nid)
        self.wallet = initial_amount
        self.current_ride = None 
        self.current_location = current_location
        self.end_location = None
    
    def display_profile(self):
        print(f"Rider: {self.name}\nEmail: {self.email}\nBalance: {self.wallet}")
    
    def load_cash(self, amount):
        self.wallet += amount 
    
    @property
    def show_current_ride(self):
        return f"Current Ride: {self.current_location} to {self.end_location}"
    
    def update_location(self, current_location):
        self.current_location = current_location
    
    def ride_request(self, ride_company, destination: str) -> None:
        if self.current_ride is None:
            # Todo: set ride properly
            # Todo: set current ride via ride match
            self.end_location = destination
            ride_request = Ride_Request(self, destination) 
            ride_matcher = Ride_Matching(ride_company)
            self.current_ride = ride_matcher.find_driver(ride_request) 
    
    def load_cash(self, amount):
        if amount > 0:
            self.wallet -= amount


class Driver(User):
    def __init__(self, name, email, nid, current_location) -> None:
        super().__init__(name, email, nid)
        self.current_location = current_location
    
    def display_profile(self):
        print(f"Rider: {self.name}\nEmail: {self.email}\nBalance: {self.wallet}")

    def accept_ride(self, ride):
        ride.set_driver(self)

    def load_cash(self, amount):
        if amount > 0:
            self.wallet += amount 
    

class Ride:
    def __init__(self, start_location, end_location) -> None:
        self.start_location = start_location
        self.end_location = end_location
        self.driver = None 
        self.rider = None
        self.start_time = None 
        self.end_time = None 
        self.estimated_fare = None 
    
    def set_driver(self, driver):
        self.driver = driver 
    
    def start_ride(self):
        self.start_time = datetime.now()
    
    def end_ride(self, rider, amount):
        self.end_time = datetime.now()
        self.rider.wallet -= amount 
        self.driver.wallet += amount 
    

class Ride_Request:
    def __init__(self, rider, end_location) -> None:
        self.rider = rider 
        self.end_location = end_location


class Ride_Matching:
    def __init__(self, ride_company) -> None:
        self.available_drivers = ride_company.drivers
    
    def find_driver(self, ride_request):
        if len(self.available_drivers) > 0:
            # TODO: find the closest driver of the rider 
            driver = self.available_drivers[0]
            ride = Ride(ride_request.rider.current_location, ride_request.rider.end_location)
            driver.accept_ride(ride)
            return ride 

class Vehicle(ABC):
    speed = {
        'car': 50,
        'bike': 60,
        'cng': 15
    }

    def __init__(self, vehicle_type, license_plate, rate, driver) -> None:
        super().__init__()
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
        self.rate = rate 
        self.driver = driver 
    
    @abstractclassmethod
    def start_drive(self):
        pass 


class Car(Vehicle):
    def __init__(self, vehicle_type, license_plate, rate, driver) -> None:
        super().__init__(vehicle_type, license_plate, rate, driver)
        self.status = 'available'
    
    def start_drive(self):
        self.status = 'unavailable'
    


# Drivers code:
niye_jao = Ride_Sharing('Niye Jao')
sakib = Rider("Sakib Khan", 'sakib@khan.com', 12345678, 'mohakhali', 1200)
niye_jao.add_rider(sakib)
kala_pakhi = Driver('Kala Pakhi', 'kala@sada.com', 563849389, 'gulshan 1')
niye_jao.add_drivers(kala_pakhi)
print(niye_jao)
# book a ride
sakib.ride_request(niye_jao, "uttra")
print(sakib.show_current_ride)
