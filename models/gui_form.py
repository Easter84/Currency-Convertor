"""
This module contains the GUI and manages all interactions with it.
"""
from business import get_currency_names, get_exchange_rates
import concurrent.futures
from logs import get_logger
from services import check_dollar_amount, convert_amount
import sys
import tkinter as tk
from tkinter import ttk


logger = get_logger(__name__)


class ExchangeForm():
    """
    This class handles the creation and interaction with a gui window for the user.
    """
    def __init__(self, root):
        self.root = root
        self.root.title('Foreign Currency Exchange Form')
        # Declaring class level variables and fields
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.country_list = []
        self.rates_dict = {}
        # Declaring All GUI widgets and Labels
        self.currency_box_label = ttk.Label(root, text='Select Currency')
        self.currency_combo_box = ttk.Combobox(root, values=self.country_list)
        self.currency_label = ttk.Label(root, text='Enter Amount of US Dollars')
        self.us_currency_entry_text = ttk.Entry(root)
        self.results_label = ttk.Label(root, text='Currency Conversion Results')
        self.results_text_box = tk.Text(root, height=5, width=45)
        self.calculate_results_button = ttk.Button(root, text='Calculate', command=self.calculate_conversion)
        self.cancel_button = ttk.Button(root, text='Close', command=self.close_app)
        # Placing all labels and widgets on the screen
        self.currency_label.grid(column=0, row=1)
        self.us_currency_entry_text.grid(column=0, row=2)
        self.currency_box_label.grid(column=0, row=3)
        self.currency_combo_box.grid(column=0, row=4)
        self.results_label.grid(column=3, row=0)
        self.results_text_box.grid(column=3, row=2, rowspan=4)
        self.calculate_results_button.grid(column=0, row=6)
        self.cancel_button.grid(column=3, row=6)
        # Populating the lists, dicts and combo box
        self.populate_fields()
        self.get_rates()

    def populate_fields(self):
        """
        This function multi-threads the get_currency_update to fill the combo box
        :return: Nothing
        """
        self.root.after(0, self.update_gui_currency("Getting Currency"))
        self.executor.submit(self.get_currency_update)

    def get_currency_update(self):
        """
        This functions calls the business layer to get the needed data from the api
        :return: Nothing
        """
        get_currency_names(self.currency_callback_success, self.currency_callback_error)
        self.update_gui_currency("Finished Getting Currency")

    def update_gui_currency(self, message):
        """
        This clears the results box and then updates it with the message passed to it.
        :param message: string
        :return: nothing
        """
        self.clear_results()
        self.results_text_box.insert(tk.END, message)

    def get_rates(self):
        """
        Multi-threads the get_exchange_rate function
        :return: Nothing
        """
        self.root.after(0, self.update_gui_currency('Getting Rates'))
        self.executor.submit(get_exchange_rates, self.rates_callback_success, self.rates_callback_error)

    def calculate_conversion(self):
        """
        This function takes the information from the gui and calculates the conversion from US
        Dollars to whatever currency the user selected and displays it in the results box.
        :return: Nothing
        """
        self.clear_results()
        selected_currency = self.currency_combo_box.get()
        amount_usd = self.us_currency_entry_text.get()

        def process_conversion():
            """
            This inner function is used to do the actual conversion and display work.
            :return: nothing
            """
            if check_dollar_amount(amount_usd):
                if selected_currency in self.rates_dict:
                    exchange_rate = self.rates_dict[selected_currency]['exchange_rate']
                    converted_amount = convert_amount(amount_usd, exchange_rate)
                    self.display_conversion_result(amount_usd, converted_amount, selected_currency)
                else:
                    self.update_gui_currency('Selected currency is not available in the exchange rates.')
            else:
                self.update_gui_currency('Please enter a valid amount')
        if not self.rates_dict:
            self.get_rates()
            self.root.after(0, process_conversion)
        else:
            process_conversion()

    def display_conversion_result(self, amount_in_usd, converted_amount, selected_currency):
        """
        This function displays a formatted result for the user to see.
        :param amount_in_usd: Gotten from the GUI
        :param converted_amount: New Amount based off calculation
        :param selected_currency: Gotten from drop down combo box
        :return: Nothing
        """
        result_text = f'${amount_in_usd} USD is worth {converted_amount} {selected_currency}'
        self.results_text_box.delete(1.0, tk.END)
        self.results_text_box.insert(1.0, result_text)

    def bind_combo_box(self):
        """
        This function is used to link/wire the combobox with the calculate_conversion method
        :return: Nothing
        """
        self.currency_combo_box.bind("<<ComboboxSelected>>", self.calculate_conversion)

    def clear_results(self):
        """
        This function clears the result box.
        :return: Nothing
        """
        self.results_text_box.delete(1.0, tk.END)

    def currency_callback_success(self, data):
        """
        This function is called when the get_currency_update method is successfully and is used
        to parse the data.
        :param data: json from the api call
        :return: a list of currency
        """
        currency_list = []
        items_json = data.json()
        for item in items_json['data']:
            currency = item.get('currency')
            if currency not in currency_list:
                currency_list.append(currency)
        self.currency_combo_box['values'] = currency_list
        self.clear_results()
        self.results_text_box.insert(tk.END, 'Getting Currency')

    def currency_callback_error(self, error):
        """
        This function is called when the get_currency_update method fails
        :param error: Failed api call
        :return: Nothing
        """
        self.update_gui_currency(f'Error :{error}')

    def rates_callback_success(self, data):
        """
        This function handles what to do when get_rates is successful
        :param data: json from the get_rates
        :return: Dictionary
        """
        rates_dict = {}
        items_json = data.json()
        for item in items_json['data']:
            currency = item.get('currency')
            record_date = item.get('record_date')
            exchange_rate = item.get('exchange_rate')
            if currency in rates_dict:
                if record_date > rates_dict[currency]['record_date']:
                    rates_dict[currency] = {'record_date': record_date, 'exchange_rate': exchange_rate}
            else:
                rates_dict[currency] = {'record_date': record_date, 'exchange_rate': exchange_rate}
        self.rates_dict = rates_dict

    def rates_callback_error(self, error):
        """
        This function is called when the get_rates has failed
        :param error:The issue that caused the failure
        :return:Nothing
        """
        error_message = f'API Error: {error}'
        self.results_text_box.insert(1.0, error_message)

    def close_app(self):
        """
        This function closes the application
        :return: Nothing
        """
        self.executor.shutdown()
        sys.exit()
