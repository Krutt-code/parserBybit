import matplotlib.pyplot as plt
import json


class CreateSchedule:
    def __init__(self, symbol: str, data: dict, img_name: str = 'graph_image.png') -> None:
        self.symbol = symbol
        self.data = data
        self.img_name = img_name

    def __filtering_data(self):
        data = {}
        for date, prices in self.data.items():
            data[':'.join(date.split()[-3:-1])] = prices[self.symbol]

        return data

    def run(self) -> None:
        filtering_data = self.__filtering_data()

        dates = list(filtering_data.keys())
        prices = list(filtering_data.values())

        plt.style.use('dark_background')

        plt.plot(dates, prices)
        plt.title(self.symbol)
        plt.xlabel('Время')
        plt.ylabel('Цена')
        plt.grid(True)

        plt.savefig(self.img_name)

        plt.close()

if __name__ == '__main__':
    with open('json.json') as file:
        data = json.load(file)

    cs = CreateSchedule(symbol='BTC', data=data)

    cs.run()