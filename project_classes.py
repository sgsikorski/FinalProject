"""CSC 161 Milestone IV: Extra Credit

Scott Sikorski
Spring 2020
Stats method is implented within this file
Project milestone III rewritten using OOD
"""


class StockMarket:
    def __init__(self, file):
        # Constructors
        self.file = file
        self.funds = 0
        self.stocks = 0
        # Used for stats method
        self.ran = False
        self.mine = False

    def transact(self, funds, stocks, qty, price, buy=False, sell=False):
        total = qty * price

        # Buying transact method
        if(buy is True):
            if(self.funds < total):
                if(self.mine is True):
                    print("Insufficient funds. Transaction wasn't processed")
                return self.funds, self.stocks
            self.remFunds = self.funds - total
            self.nowStocks = self.stocks + qty
            return self.remFunds, self.nowStocks

        elif(sell is True):
            if(self.stocks < qty):
                if(self.mine is True):
                    print("Insufficient stocks. Transaction wasn't processed")
                return self.funds, self.stocks
            self.remFunds = self.funds + total
            self.nowStocks = self.stocks - qty
            return self.remFunds, self.nowStocks

        else:
            print("Ambigious transaction. Can't determine wheter to buy or"
                  "sell. No actions performed")
            return self.funds, self.stocks

    def alg_moving_average(self):
        self.mine = False
        file = open(self.file, "r")
        f = file.readlines()
        topLine = f[0].split(",")
        self.funds = 1000
        self.stocks = 100
        avgTotal = 0

        for i in range(len(f) - 20):
            for j in range(20):
                stockValues = f[i + j + 1].split(",")
                stockVal = float(stockValues[1])  # Uses open value
                avgTotal = avgTotal + stockVal
            average = float(avgTotal / 20)

            if((stockVal - average) / (average) * 100 > 5):
                self.funds, self.stocks = self.transact(self.funds,
                                                        self.stocks,
                                                        10, stockVal,
                                                        sell=True)

            elif((stockVal - average) / (average) * 100 < -5):
                self.funds, self.stocks = self.transact(self.funds,
                                                        self.stocks,
                                                        10, stockVal,
                                                        buy=True)

        self.funds, self.stocks = self.transact(self.funds, self.stocks,
                                                self.stocks, stockVal,
                                                sell=True)

        return self.funds, self.stocks

    def alg_mine(self):
        self.mine = True
        if(self.ran is True):
            return self.funds, self.stocks

        # Initialize variables
        file = open(self.file, "r")
        f = file.readlines()
        topLine = f[0].split(",")
        self.funds = 1000
        self.stocks = 100

        print("This algorithm takes the daily change percent and decides "
              "whether to sell or buy based on your preferences")

        # For testing the AAPL.csv, 12.5 as a buying point creates 3 responses
        # 10 as a selling point creates 5 responses

        # Asking the user for their daily change preferences
        selling = float(input("What day change percent do you want to sell"
                              " at? "))
        buying = float(input("What day change percent do you want to buy"
                             " at? "))
        dailyStocks = int(input("How many stocks would you want to buy"
                                " or sell at? "))

        # This algorithm takes the open and close values and calculates the
        # day change percent and determines to sell or buy a user inputed
        # amount of stocks based on the user preferences for the day change
        # percent
        for i in range(len(f)):
            if(i == 0):
                continue
            stockValues = f[i].split(",")
            openValue = float(stockValues[1])
            closeValue = float(stockValues[4])
            dayChange = openValue - closeValue
            dailyPercent = (dayChange / openValue) * 100

            if(dailyPercent > selling):
                self.funds, self.stocks = self.transact(self.funds,
                                                        self.stocks,
                                                        dailyStocks,
                                                        closeValue,
                                                        sell=True)

            if(dailyPercent < buying * -1):
                self.funds, self.stocks = self.transact(self.funds,
                                                        self.stocks,
                                                        dailyStocks,
                                                        closeValue, buy=True)

        self.funds, self.stocks = self.transact(self.funds, self.stocks,
                                                self.stocks, closeValue,
                                                sell=True)
        self.ran = True

        return self.funds, self.stocks

    # Extra credit statistics method
    def stats(self):
        # Based on returned funds values, creates the difference between them
        m = list(self.alg_mine())
        mA = list(self.alg_moving_average())
        diff = mA[0] - m[0]

        # Describes which one is better by which method makes the most money
        if(diff > 0):
            s = "The moving average algorithm is better because \
the difference is ${0}".format(diff)
        elif(diff < 0):
            s = "The daily change algorithm is better because \
the difference is ${0}".format(diff * -1)

        return s

    def __repr__(self):
        s1 = "Current Stocks: {0} \nCurrent Balance: \
${1}".format(self.stocks, self.funds)
        return s1


def main():
    file = input("What file do you want to use? ")
    trading = StockMarket(file)
    print(trading)
    alg_1 = list(trading.alg_moving_average())
    print("The finishing balance is ${0}".format(alg_1[0]))
    alg_2 = list(trading.alg_mine())
    print("The finshing balance is ${0}".format(alg_2[0]))
    print(trading.stats())


if(__name__ == "__main__"):
    main()
