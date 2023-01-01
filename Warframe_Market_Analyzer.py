
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import json
import csv
from enum import Enum, auto

class ITEM_TYPE(Enum):
    RELICS = auto()
    SETS = auto()
    ARCANES = auto()
    BLUEPRINTS = auto()
    NEUROPTICS = auto()
    SYSTEMS = auto()
    CHASSIS = auto()
    BARRELS = auto()
    STOCKS = auto()
    RECEIVERS = auto()
    HANDLES = auto()
    BLADES = auto()
    HILTS = auto()
    SCENES = auto()
    EMOTES = auto()
    IMPRINTS = auto()
    MODS = auto()


class Market:

    def __init__(self):
        self.FilePath = ""
        self.marketurl = "https://api.warframe.market/v1/"
        self.items = {}
        
        Market.__CreateMainFilePath__(self)
        Market.__SetItemsFile__(self)

    def __CreateDir__(self, path):
        """Helper method that creates a directory if the directory does not exist."""
        if os.path.isdir(path) == False:
            os.mkdir(path)

    def __CreateMainFilePath__(self):
        """Creates the file path to the directory."""

        path = "C:/Users/" + os.getlogin() + "/Documents/WarframeMarketAnalyzer"

        # C:\Users\{user}\Documents\WarframeMarketAnalyzer

        Market.__CreateDir__(self, path)         # Checks if the directory, "WarframeMarketAnalyzer" exists

        self.FilePath = path

    def __SetItemsFile__(self):
        """Sets ItemList file."""
        path = self.GetItemFilePath()

        if not os.path.exists(path) == True:
            Market.__CreateItemList__(self)

    def __CreateItemList__(self):
        """Creates a json file of items."""

        def SortItem(self, item):
            """Helper methood that sorts the item into their respective key"""
            if "_relic" in item:
                self.items[ITEM_TYPE.RELICS.name].append(item)
            
            elif "_set" in item:
                self.items[ITEM_TYPE.SETS.name].append(item)
            
            elif "arcane_" in item:
                self.items[ITEM_TYPE.ARCANES.name].append(item)
            
            elif "_blueprint" in item:
                self.items[ITEM_TYPE.BLUEPRINTS.name].append(item)

            elif "_neuroptics" in item:
                self.items[ITEM_TYPE.NEUROPTICS.name].append(item)
            
            elif "_prime_systems" in item:
                self.items[ITEM_TYPE.SYSTEMS.name].append(item)
            
            elif "_chassis" in item:
                self.items[ITEM_TYPE.CHASSIS.name].append(item)
            
            elif "_barrel" in item:
                self.items[ITEM_TYPE.BARRELS.name].append(item)
            
            elif "_stock" in item:
                self.items[ITEM_TYPE.STOCKS.name].append(item)
            
            elif "_receiver" in item:
                self.items[ITEM_TYPE.RECEIVERS.name].append(item)

            elif "_handle" in item:
                self.items[ITEM_TYPE.HANDLES.name].append(item)

            elif "_blade" in item:
                self.items[ITEM_TYPE.BLADES.name].append(item)

            elif "_hilt" in item:
                self.items[ITEM_TYPE.HILTS.name].append(item)
            
            elif "_scene" in item:
                self.items[ITEM_TYPE.SCENES.name].append(item)
            
            elif "_emote" in item:
                self.items[ITEM_TYPE.EMOTES.name].append(item)
            
            elif "_imprint" in item:
                self.items[ITEM_TYPE.IMPRINTS.name].append(item)
            
            else:
                self.items[ITEM_TYPE.MODS.name].append(item)
            exit

        self.items = {
            ITEM_TYPE.RELICS.name: [], 
            ITEM_TYPE.SETS.name: [], 
            ITEM_TYPE.ARCANES.name: [], 
            ITEM_TYPE.BLUEPRINTS.name: [], 
            ITEM_TYPE.NEUROPTICS.name: [], 
            ITEM_TYPE.SYSTEMS.name: [], 
            ITEM_TYPE.CHASSIS.name: [], 
            ITEM_TYPE.BARRELS.name: [],
            ITEM_TYPE.STOCKS.name: [],
            ITEM_TYPE.RECEIVERS.name: [],
            ITEM_TYPE.HANDLES.name: [],
            ITEM_TYPE.BLADES.name: [],
            ITEM_TYPE.HILTS.name: [],
            ITEM_TYPE.SCENES.name: [],
            ITEM_TYPE.EMOTES.name: [],
            ITEM_TYPE.IMPRINTS.name: [],
            ITEM_TYPE.MODS.name: []
        }

        path = self.GetItemFilePath()

        rawitems = self.__GetRawItems__()

        for item in rawitems["payload"]["items"]:
            SortItem(self, item["url_name"])   

        with open(path,'w') as jsonFile:
            json.dump(self.items, jsonFile)

    def __GetRawItems__(self):
        """Helper Methood to get all items on the market"""
        return requests.get(self.marketurl+"/items").json()

    def __CreateCsvFile__(self, data, name):
        """Creates the csv file."""
        path = self.FilePath + "/ItemOrderData"

        self.__CreateDir__(path)

        data.to_csv(f'{path}/{name}.csv', index=False)

    def __PrintCsvFile__(self, name):
        """Prints entire csv file."""
        data = self.__GetOrdersFile__(name)
        print(data)

    def __GetSellOrdersFile__(self, name):
        """Gets only Order_Type "Sell" from csv file."""
        path = f'{self.FilePath}/ItemOrderData/{name}.csv'

        data = pd.read_csv(path)

        data = data.drop(data[data.Order_Type != "Sell"].index)

        data = data.sort_values(by = 'Platinum')

        return data

    def __GetBuyOrdersFile__(self, name):
        """Gets only Order_Type "Buy" from csv file."""
        path = f'{self.FilePath}/ItemOrderData/{name}.csv'

        data = pd.read_csv(path)

        data = data.drop(data[data.Order_Type != "Buy"].index)

        data = data.sort_values(by = 'Platinum')

        return data

    def __GetOrdersFile__(self, name):
        """Returns entire csv file."""
        
        path = f'{self.FilePath}/ItemOrderData/{name}.csv'

        data = pd.read_csv(path)

        return data

    def __DisplayData__(self, data):
        """Prints data."""
        print(data)

    def PlotData(self, data):
        """Plots data and shows the plot."""
        data.plot(x="Platinum", y="Quantity", kind="bar")

        plt.show()

    def GetItemFilePath(self):
        """Helper methood to set path to ItemList.json"""
        return self.FilePath + "/ItemList.json"

    def GetItemOrderInfo(self, url_name: str):
        """Helper methood that returns a list of all orders for the specified url name."""
        return requests.get(self.marketurl+"/items/"+url_name+"/orders").json()["payload"]["orders"]

    def UpdateItemList(self):
        """Updates ItemList.json"""
        path = self.GetItemFilePath(self)
        self.__CreateItemList__(self, path)

    def SetItems(self, itype = None):
        """Gets ItemList.json and loads into self.items."""
        path = self.GetItemFilePath()
        with open(path) as jsonFile:
            self.items = json.load(jsonFile)
        
        if itype != None:
            self.items = self.items[itype.name]
        
    def RawDisplay(self, itype = None):
        """Prints entire dictionary unless specific item"""

        self.SetItems(itype)

        print(self.items)

    def ItemOrderInfo(self, url_name: str):
        """Creates csv file to be used."""

        # Add mod rank


        ItemOrders = self.GetItemOrderInfo(url_name)

        def GenerateHashMap(ItemOrders):

            hashmap = {}

            for index, item in enumerate(ItemOrders):
                if f'{item["platinum"]}{item["order_type"]}' in hashmap:
                    hashmap[f'{item["platinum"]}{item["order_type"]}'] += item["quantity"]
                else:
                    hashmap[f'{item["platinum"]}{item["order_type"]}'] = item["quantity"]
            
            return hashmap


        hashmap = GenerateHashMap(ItemOrders)

        data = {"Quantity": [], "Platinum": [], "Order_Type": []}

        for index, item in enumerate(hashmap):
            if "sell" in item:
                data["Order_Type"].append("Sell")
                data["Platinum"].append(int(item[:-4]))
                data["Quantity"].append(hashmap[item])
            else:
                data["Order_Type"].append("Buy")
                data["Platinum"].append(int(item[:-3]))
                data["Quantity"].append(hashmap[item])
        
        data = pd.DataFrame(data=data)

        self.__CreateCsvFile__(data, url_name)

    def DisplayFile(self, name: str, *, OrderType: str):
        """Displays and plots an existing csv file of the specified item/name of file."""
        
        if OrderType == 'Sell':
           data = self.__GetSellOrdersFile__(name)
           self.PlotData(data)
        elif OrderType == 'Buy':
            data = self.__GetBuyOrdersFile__(name)
            self.PlotData(data)
        else:
            data = self.__GetOrdersFile__(name)
        
        self.__DisplayData__(data)

def main():
    # Main functions include: RawDisplay(ITEM_TYPE._), ItemOrderInfo(url_name), DisplayFile(url_name)
    WarframeMarket = Market()
    WarframeMarket.RawDisplay(ITEM_TYPE.SETS)
    WarframeMarket.ItemOrderInfo("phantasma_prime_set")
    WarframeMarket.DisplayFile("phantasma_prime_set", OrderType="Sell")


if __name__ == "__main__":
    main()
