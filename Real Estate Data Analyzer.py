import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from abc import ABC, abstractmethod




class Property(ABC):

    def __init__(self, property_id, district, area, price, rooms, sold):
        self.property_id = property_id
        self.district = district
        self.area = area
        self.price = price
        self.rooms = rooms
        self.sold = sold

    def calculate_price_per_m2(self):
      return self.price / self.area

    @abstractmethod
    def property_type(self):
        pass


class Apartment(Property):
    def property_type(self):
        return "Apartment"


class House(Property):
    def property_type(self):
        return "House"


class FilterStrategy(ABC):
    @abstractmethod
    def filter_data(self, df):
        pass


class PriceFilter(FilterStrategy):
    def __init__(self, max_price):
        self.max_price = max_price
    def filter_data(self, df):
        return df[df["price"] <= self.max_price]



class AreaFilter(FilterStrategy):
    def __init__(self, min_area):
        self.min_area = min_area
    def filter_data(self, df):
        return df[df["area"] >= self.min_area]


class DistrictFilter(FilterStrategy):
    def __init__(self, district):
        self.district = district
    def filter_data(self, df):
        return df[df["district"] == self.district]



class RoomFilter(FilterStrategy):
    def __init__(self, rooms):
        self.rooms = rooms
    def filter_data(self, df):
        return df[df["rooms"] == self.rooms]



class RealEstateAnalyzer:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)


    def show_statistics(self):
        print("\nAverage Price:")
        print(self.df["price"].mean())

        print("\nMost Expensive District:")
        print(self.df.groupby("district")["price"].mean().idxmax())

        print("\nSold Properties:")
        print(self.df[self.df["sold"] == True].shape[0]) #rows soni

    def apply_filter(self, strategy):

        filtered = strategy.filter_data(self.df)
        return filtered


    def export_excel(self, data):
        data.to_excel("data.xlsx", index=False)
        print("Excel exported")


    def visualize(self):

        sns.histplot(self.df["price"])
        plt.title("Price Distribution")
        plt.show()

        sns.barplot( x="district", y="price", data=self.df)
        plt.title("District Prices")
        plt.show()




class RealEstateCLI:

    def __init__(self):

        self.analyzer = RealEstateAnalyzer(
            "properties.csv")

    def run(self):
        while True:
            print("\n1. Show Statistics")
            print("2. Filter By Price")
            print("3. Filter By Area")
            print("4. Filter By District")
            print("5. Filter By Rooms")
            print("6. Visualize")
            print("7. Exit")
            

            choice = input("Choose: ")

  
            if choice == "1":
                self.analyzer.show_statistics()

            elif choice == "2":

                max_price = float(
                    input("Max price: "))

                strategy = PriceFilter(max_price)

                result = self.analyzer.apply_filter(
                    strategy)

                print(result)


            elif choice == "3":
                min_area = float(
                    input("Min area: "))

                strategy = AreaFilter(min_area)
                result = self.analyzer.apply_filter(strategy)

                print(result)


            elif choice == "4":
                district = input("District: ")

                strategy = DistrictFilter(district)

                result = self.analyzer.apply_filter(strategy)
                print(result)

            elif choice == "5":

                rooms = int(
                    input("Rooms: "))

                strategy = RoomFilter(rooms)

                result = self.analyzer.apply_filter(strategy)
                print(result)

     
            elif choice == "6":
                self.analyzer.visualize()

            elif choice == "7":
                break


cli = RealEstateCLI()
cli.run()