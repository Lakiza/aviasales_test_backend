import json
import utils

class DashboardData:
    def __init__(self, data):
        self._data = {}
        self._average = {}

        jsonData = json.loads(data)
        errors = self._parseDataByPeriods(jsonData)
        statistic = self._parseDataByPeriods(jsonData['data'][0])
        self._data = self._normalize(errors, statistic)

        self._average['errors'] = self._calculateAverageOf('statistic.errors', self._data)
        self._average['zeroes'] = self._calculateAverageOf('statistic.zeroes', self._data)
        self._average['timeout'] = self._calculateAverageOf('statistic.timeout', self._data)

    def _parseDataByPeriods(self, data):
        _data = {
            'lastHour': {},
            'today': {},
            'yesterday': {},
            '3days': {}
        }

        # Devide all data by periods
        for key, value in data.items():
            if key.find('_last_hour') != -1:
                newKey = key.replace('_last_hour', '')
                _data['lastHour'][newKey] = value
            elif key.find('_today') != -1:
                newKey = key.replace('_today', '')
                _data['today'][newKey] = value
            elif key.find('_yesterday') != -1:
                newKey = key.replace('_yesterday', '')
                _data['yesterday'][newKey] = value
            elif key.find('_last_3days') != -1:
                newKey = key.replace('_last_3days', '')
                _data['3days'][newKey] = value

        return _data

    def _calculateAverageOf(self, path, data):
        summary = 0
        elements = 0

        for period in data.keys():
            if not data[period]:
                continue

            value = utils.getDictValueByPath(data[period], path)
            if value is not None:
                summary += value
                elements += 1

        return summary / elements if elements else 0


    def _normalize(self, errors, statistic):
        if not errors or not statistic:
            raise TypeError('Invalid')

        # Transform to frontend-friendly format 
        data = {}
        for period in errors.keys():
            if not errors[period] and not statistic[period]: 
                data[period] = {}
                continue

            data[period] = {
                'errors': errors[period].get('errors', []),
                'statistic': {
                    'errors': statistic[period].get('errors', 0),
                    'zeroes': statistic[period].get('zeroes', 0),
                    'timeout': statistic[period].get('timeout', 0),
                    'searches': {
                        'current': statistic[period].get('searches_current', 0),
                        'previous': statistic[period].get('searches_previous', 0)
                    },
                    'clicks': {
                        'current': statistic[period].get('clicks_current', 0),
                        'previous': statistic[period].get('clicks_previous', 0)
                    },
                    'bookings': {
                        'current': statistic[period].get('bookings_current', 0),
                        'previous': statistic[period].get('bookings_previous', 0)
                    },
                    'ctr': statistic[period].get('ctr', 0),
                    'str': statistic[period].get('str', 0),
                    'avgcheck': statistic[period].get('avg_price', 0),
                }
            }

        return data
            
    def getDataForPeriod(self, period):
        if period in self._data:
            return self._data[period]
        else: 
            return None

    def getStatisticAverage(self):
        return self._average
        