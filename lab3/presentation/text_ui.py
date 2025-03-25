from sqlalchemy.engine import Row

from service.weather_service import WeatherService

from config import CSV_PATH


class TextUI:
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    @staticmethod
    def print_waring(msg: str):
        print(f'\t(!) {msg}')

    @staticmethod
    def print_info(msg: str):
        print(f'\t(i) {msg}')

    @staticmethod
    def print_weather_short(row: Row):
        string = (
            f'\tid = {row.Weather.id: <5} {row.Weather.country: <30}{str(row.Weather.last_updated)}'
            f'\t|\tweather: wind = {row.Weather.wind_kph: >4} kph'
        )

        air_quality = row.Weather.air_quality

        if air_quality:
            string += (
                f'\t|\tair_quality: US EPA = {air_quality.air_quality_us_epa_index: >2}'
            )

        analytics = row.Weather.analytics

        if analytics:
            string += (
                f'\t|\tanalytics: should go outside = {analytics.should_go_outside}'
            )

        print(string)

    def main_menu(self):
        actions = (
            ('Load from CSV', self.load_from_csv_menu),
            # ('Insert', None),
            ('View all', lambda: self.view_all_menu(0)),
            ('Delete all', self.delete_all_menu),
            ('Delete by ID', self.delete_by_id_menu),
            ('Quit', quit),
        )

        print('\n\n=== MAIN MENU ===')
        print('Actions:')
        for i, (action_name, _) in enumerate(actions):
            print(f'\t{i+1}. {action_name}')

        while True:
            try:
                action_i = int(input('Please, enter an action number: ')) - 1
            except ValueError:
                self.print_waring('This is not a number')
                continue

            if not 0 <= action_i < len(actions):
                self.print_waring('No action corresponds to this number')
                continue

            action_func = actions[action_i][1]
            break

        action_func()

    # === CREATE ============================================================================
    def load_from_csv_menu(self):
        print('\n\n=== LOAD FROM CSV ===')
        print('All the entries will be deleted and replaced with data from this file:')
        print(f'\t{CSV_PATH}')

        command = input('Continue? (y/n) ')
        if command.lower() == 'y':
            self.weather_service.load_from_csv()
            self.print_info('Done')
        else:
            self.print_info('Canceled')

        self.main_menu()

    # === READ ==============================================================================
    def view_all_menu(self, page):
        actions = (
            ('Previous page', lambda: self.view_all_menu(max(0, page - 1))),
            ('Next page', lambda: self.view_all_menu(page + 1)),
            ('Exit', self.main_menu),
        )

        print('\n\n=== VIEW ALL ===')
        print('Shows a short representation of the weather data')
        print('Actions:')
        for i, (action_name, _) in enumerate(actions):
            print(f'\t{i + 1}. {action_name}')

        print(f'Page {page+1}:')
        for row in self.weather_service.view_all(page, 20):
            self.print_weather_short(row)

        while True:
            try:
                action_i = int(input('Please, enter an action number: ')) - 1
            except ValueError:
                self.print_waring('This is not a number')
                continue

            if not 0 <= action_i < len(actions):
                self.print_waring('No action corresponds to this number')
                continue

            action_func = actions[action_i][1]
            break

        action_func()

    # === DELETE ============================================================================
    def delete_all_menu(self):
        print('\n\n=== DELETE ALL ===')
        print('All the entries will be deleted')

        command = input('Continue? (y/n) ')
        if command.lower() == 'y':
            self.weather_service.delete_all()
            self.print_info('Done')
        else:
            self.print_info('Canceled')

        self.main_menu()

    def delete_by_id_menu(self):
        print('\n\n=== DELETE BY ID ===')

        while True:
            command = input('Enter ID of the entry you want to delete or leave empty to cancel: ')

            if command == '':
                self.print_info('Canceled')
                break

            try:
                obj_id = int(command)
            except ValueError:
                self.print_waring('This is not a number')
                continue

            num_rows_deleted = self.weather_service.delete_by_id(obj_id)

            if num_rows_deleted == 0:
                self.print_waring('There is no rows with this ID')
                continue

            self.print_info('Done')
            break

        self.main_menu()
