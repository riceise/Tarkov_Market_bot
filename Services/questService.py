import os
import json
parsed_detailed_info_dir = 'parsed_detailed_info'
parsed_main_info_dir = 'parsed_main_info'
# class QuestService:
#     def get_quests_for_trader(self, trader_name):
#         """
#         Получить список квестов для заданного торговца.
#         :param trader_name: имя торговца
#         :return: список квестов
#         """
#         filepath = os.path.join(f'parsing_service/parsed_main_info/{trader_name}.json')
#         print(f"Looking for main quests file at: {filepath}")  # Diagnostic message
#
#         if not os.path.exists(filepath):
#             print("Main quests file not found.")  # Diagnostic message
#             return None
#
#         with open(filepath, 'r', encoding='utf-8') as file:
#             data = json.load(file)
#         return data.get('Квесты', [])
#
#     def get_quest_details(self, trader_name, quest_name):
#         """
#         Получить подробную информацию о квесте.
#         :param trader_name: имя торговца
#         :param quest_name: название квеста
#         :return: информация о квесте
#         """
#         filepath = os.path.join(f'parsing_service/parsed_detailed_info/{trader_name}/{quest_name}.json')
#         print(f"Looking for detailed quest file at: {filepath}")  # Diagnostic message
#
#         if not os.path.exists(filepath):
#             print("Detailed quest file not found.")  # Diagnostic message
#             return None
#
#         with open(filepath, 'r', encoding='utf-8') as file:
#             quest_data = json.load(file)
#         return quest_data
class QuestService:
    def get_quests_for_trader(self, trader_name):
        filepath = os.path.join(f'parsing_service/parsed_main_info/{trader_name}.json')
        print(f"Looking for main quests file at: {filepath}")  # Diagnostic message

        if not os.path.exists(filepath):
            print("Main quests file not found.")  # Diagnostic message
            return None

        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get('Квесты', [])

    def get_quest_details(self, trader_name, quest_name):
        filepath = os.path.join(f'parsing_service/parsed_detailed_info/{trader_name}/{quest_name}.json')
        print(f"Looking for detailed quest file at: {filepath}")  # Diagnostic message

        if not os.path.exists(filepath):
            print("Detailed quest file not found.")  # Diagnostic message
            return None

        with open(filepath, 'r', encoding='utf-8') as file:
            quest_data = json.load(file)
        return quest_data