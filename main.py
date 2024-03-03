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
        for i in range(len(self.csv_data)):
            try:
                if self.csv_data[i][7] == 'isEvent' or self.csv_data[i][7] == 'isNotEvent':
                    self.current_row = i
            except:
                pass



        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Adjusted the container height to accommodate larger buttons
        self.action_buttons_container = BoxLayout(size_hint_y=None, height=210)
        # Increased button height and font size
        self.isEvent_button = Button(text="isEvent", on_press=self.mark_isEvent, size_hint_y=None, height=200, font_size='32sp')
        self.isNotEvent_button = Button(text="isNotEvent", on_press=self.mark_isNotEvent, size_hint_y=None, height=200, font_size='32sp')
        self.action_buttons_container.add_widget(self.isEvent_button)
        self.action_buttons_container.add_widget(self.isNotEvent_button)

        self.row_buttons_container = BoxLayout(size_hint_y=None, height=210)
        # Increased button height and font size
        self.previous_row_button = Button(text="Previous", on_press=self.previous_row, size_hint_y=None, height=200, font_size='32sp')
        self.next_row_button = Button(text='Next', on_press=self.next_row, size_hint_y=None, height=200, font_size='32sp')
        self.row_buttons_container.add_widget(self.previous_row_button)
        self.row_buttons_container.add_widget(self.next_row_button)

        self.labels_container = BoxLayout(orientation='vertical', size_hint_y=None, padding=(10, 10))
        self.labels_container.bind(minimum_height=self.labels_container.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height * 0.8))
        self.scroll_view.add_widget(self.labels_container)

        self.root.add_widget(self.scroll_view)
        self.root.add_widget(self.action_buttons_container)
        self.root.add_widget(self.row_buttons_container)

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

    def mark_isEvent(self, instance):
        # Ensure the current row is within the bounds of the CSV data
        if 0 <= self.current_row < len(self.csv_data):
            # Check if the current row has less than 6 columns
            if len(self.csv_data[self.current_row]) < 8:
                # If so, extend the row with empty values up to the 6th column
                self.csv_data[self.current_row].extend([""] * (8 - len(self.csv_data[self.current_row])))
            # Set the 6th column (index 5) to "correct"
            self.csv_data[self.current_row][7] = "isEvent"
            # Update the CSV file with the modified data
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_isNotEvent(self, instance):
        # Ensure the current row is within the bounds of the CSV data
        if 0 <= self.current_row < len(self.csv_data):
            # Check if the current row has less than 6 columns
            if len(self.csv_data[self.current_row]) < 8:
                # If so, extend the row with empty values up to the 6th column
                self.csv_data[self.current_row].extend([""] * (8 - len(self.csv_data[self.current_row])))
            # Set the 6th column (index 5) to "incorrect"
            self.csv_data[self.current_row][7] = "isNotEvent"
            # Update the CSV file with the modified data
            self.update_csv()
            self.update_labels(self.current_row)

    def update_labels(self, row_index):
        self.labels_container.clear_widgets()
        if row_index < len(self.csv_data):
            for i, item in enumerate(self.csv_data[row_index]):
                # Check if the item is a hyperlink
                if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\'(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item):
                    label = ClickableLabel(text=item, font_size='20sp', color=(0, 0, 1, 1), size_hint_y=None,
                                           halign='left', valign='top')
                elif i == 4:
                    label = Label(text=item, font_size='20sp', size_hint_y=None, halign='left', valign='top')
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
            self.current_row = len(self.csv_data) - 1  # Prevent going beyond the last row
            self.next_row_button.disabled = True
        self.previous_row_button.disabled = False

    def previous_row(self, instance):
        if self.current_row > 0:
            self.current_row -= 1
            self.update_labels(self.current_row)
            self.next_row_button.disabled = False

if __name__ == '__main__':
    CsvRowApp().run()


