from .parser import ParserBybit, JsonHandler
from datetime import datetime, timedelta

from os import path

import logging

logger = logging.getLogger('parser')

class DataM:
    def __init__(self, config, time) -> None:
        self.config = config
        self.data_path = self.config.data.data_file_name
        self.time = time

    def __get_time(self):
        date = datetime.now() + timedelta(hours=3)
        return date.strftime('%Y %m %d %H %M %S')

    def __update_data_prices(self):
        
        JsonHandler(self.data_path).write_to_json(
            {
            self.time: ParserBybit().run()
            }
        )
    
    def __calculate_time_difference_minutes(self, start_time, end_time):
        time_diff = datetime(*map(int, end_time.split())) - datetime(*map(int, start_time.split()))
        return time_diff.total_seconds() / 60
    
    def __read_data(self):
        try: 
            return JsonHandler(self.data_path).read_json()
        except Exception as e:
            logger.error(e)

    def __change_check(self, data):
        time1, time2 = data[0][0], data[1][0]
        prices1, prices2 = data[0][1], data[1][1]
        difference = {}

        for name, price in prices1.items():
            if name in prices2:
                if price - prices2[name] != 0:
                    if self.config.data.negative_change:
                        if (abs(price - prices2[name]) / price) * 100  > self.config.data.height:
                            difference[name] = {
                                time2: prices2[name],
                                time1: price
                            }
                    else:
                        if price - prices2[name] > 0:
                            if ((price - prices2[name]) / price) * 100  > self.config.data.height:
                                difference[name] = {
                                    time2: prices2[name],
                                    time1: price
                                }
            
        return difference
    
    def __remove_old_data(self, data: dict) -> dict:
        new_data = {}
        time_now = self.__get_time()

        for time, item in data.items():
            if ((datetime(*map(int, time_now.split())) - datetime(*map(int, time.split()))).total_seconds() // 60) <= (self.config.data.period_time*4 + 1):
                new_data[time] = item

        if len(data.items()) != len(new_data.items()):
            JsonHandler(self.data_path).write_json(new_data)

        return new_data


    def __time_validation(self) -> dict:
        data = {
            '🔴': {},
            '🟠': {},
            '🟡': {} 
        }
        if not self.__read_data():
            JsonHandler(self.data_path).write_json({})

        self.__update_data_prices()

        try:
            new_data = self.__remove_old_data(self.__read_data())
        except Exception as e:
            logger.error(e)

        if len(new_data.items()) > 1:
            items = list(new_data.items())[::-1]
            for item in items[1:]:
                time_difference = self.__calculate_time_difference_minutes(
                    start_time=item[0],
                    end_time  =items[0][0]
                ) + 0.5

                if time_difference >= self.config.data.period_time*4:
                    if not data['🟡']:
                        data['🟡'] = self.__change_check([items[0], item])
                        return data

                elif time_difference >= self.config.data.period_time*2:
                    if not data['🟠']:
                        data['🟠'] = self.__change_check([items[0], item])
                        continue

                elif time_difference >= self.config.data.period_time:
                    if not data['🔴']:
                        data['🔴'] = self.__change_check([items[0], item])
                        continue
                
                else:
                    continue
                    
            return data
        
        return data


    def run(self):
        return self.__time_validation()