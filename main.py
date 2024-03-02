from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.button import Button  # Corrected import for Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import csv
import re
import webbrowser

class ClickableLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.on_label_press)

    def on_label_press(self, *args):
        webbrowser.open(self.text)

class CsvRowApp(App):
    def build(self):
        self.csv_file = 'data.csv'  # Ensure this is the correct path to your CSV file
        self.csv_data = self.read_csv(self.csv_file)
        self.current_row = 0

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Adjust size and height here for "Correct" and "Incorrect" buttons
        self.buttons_container = BoxLayout(size_hint_y=None, height=100)  # Adjusted container height
        self.correct_button = Button(text="Correct", on_press=self.mark_correct, size_hint_y=2, height=50, font_size='20sp')
        self.incorrect_button = Button(text="Incorrect", on_press=self.mark_incorrect, size_hint_y=2, height=50, font_size='20sp')
        self.next_row_button = Button(text='Next Row', on_press=self.next_row, size_hint_y=2, height=50, font_size='20sp')

        self.buttons_container.add_widget(self.correct_button)
        self.buttons_container.add_widget(self.incorrect_button)

        self.labels_container = BoxLayout(orientation='vertical', size_hint_y=None, padding=(10, 10))
        self.labels_container.bind(minimum_height=self.labels_container.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.8))
        self.scroll_view.add_widget(self.labels_container)

        self.root.add_widget(self.scroll_view)
        self.root.add_widget(self.buttons_container)
        self.root.add_widget(self.next_row_button)

        self.update_labels(self.current_row)

        return self.root

    def read_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data

    def update_csv(self):
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.csv_data)

    def mark_correct(self, instance):
        # Ensure the current row is within the bounds of the CSV data
        if 0 <= self.current_row < len(self.csv_data):
            # Check if the current row has less than 6 columns
            if len(self.csv_data[self.current_row]) < 6:
                # If so, extend the row with empty values up to the 6th column
                self.csv_data[self.current_row].extend([""] * (6 - len(self.csv_data[self.current_row])))
            # Set the 6th column (index 5) to "correct"
            self.csv_data[self.current_row][5] = "correct"
            # Update the CSV file with the modified data
            self.update_csv()

    def mark_incorrect(self, instance):
        # Ensure the current row is within the bounds of the CSV data
        if 0 <= self.current_row < len(self.csv_data):
            # Check if the current row has less than 6 columns
            if len(self.csv_data[self.current_row]) < 6:
                # If so, extend the row with empty values up to the 6th column
                self.csv_data[self.current_row].extend([""] * (6 - len(self.csv_data[self.current_row])))
            # Set the 6th column (index 5) to "incorrect"
            self.csv_data[self.current_row][5] = "incorrect"
            # Update the CSV file with the modified data
            self.update_csv()

    def update_labels(self, row_index):
        self.labels_container.clear_widgets()
        if row_index < len(self.csv_data):
            for item in self.csv_data[row_index]:
                # Check if the item is a hyperlink
                if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\'(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item):
                    label = ClickableLabel(text=item, font_size='20sp', color=(0, 0, 1, 1), size_hint_y=None,
                                           halign='left', valign='top')
                else:
                    label = Label(text=item, font_size='20sp', size_hint_y=None, halign='left', valign='top')
                label_width = self.scroll_view.width - 2 * self.labels_container.padding[0] - 20
                label.text_size = (label_width, None)
                label.bind(texture_size=lambda instance, value: setattr(instance, 'size', (label_width, value[1])))
                self.labels_container.add_widget(label)
        else:
            self.labels_container.add_widget(Label(text='End of file reached!', font_size='20sp'))

    def next_row(self, instance):
        self.current_row += 1
        if self.current_row < len(self.csv_data):
            self.update_labels(self.current_row)
        else:
            self.next_row_button.disabled = True
            # Optionally disable the Correct/Incorrect buttons here as well

if __name__ == '__main__':
    CsvRowApp().run()

