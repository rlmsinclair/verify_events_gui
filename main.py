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

PATH_TO_CSV = '1000data.csv'  # Path to the csv file
ONLY_SHOW_ISEVENT = False  # This will only show instagram captions that at least one of the AIs thinks is an event

class ClickableLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.on_label_press)

    def on_label_press(self, *args):
        webbrowser.open(self.text)

class CsvRowApp(App):
    def build(self):
        self.csv_file = PATH_TO_CSV  # Ensure this is the correct path to your CSV file
        self.csv_data = self.read_csv(self.csv_file)
        self.current_row = 0
        for i in range(len(self.csv_data)):
            try:
                if self.csv_data[i][4] == 'event' or self.csv_data[i][4] == 'no_event':
                    self.current_row = i
            except:
                pass



        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.action_buttons_container_top = BoxLayout(size_hint_y=None, height=100)  # Adjusted height for more buttons
        self.action_buttons_container_bottom = BoxLayout(size_hint_y=None, height=100)  # Adjusted height for more buttons


        # Define new buttons

        self.is_event_button = Button(text="Event", on_press=self.mark_is_event, size_hint_y=None, height=100,
                                     font_size='20sp')
        self.invites_button = Button(text="Invites", on_press=self.mark_invites, size_hint_y=None, height=100,
                                     font_size='20sp')
        self.date_button = Button(text="Date", on_press=self.mark_date, size_hint_y=None, height=100, font_size='20sp')
        self.time_button = Button(text="Time", on_press=self.mark_time, size_hint_y=None, height=100, font_size='20sp')

        self.location_button = Button(text="Location", on_press=self.mark_location, size_hint_y=None, height=100,
                                      font_size='20sp')
        self.future_button = Button(text="Future", on_press=self.mark_future, size_hint_y=None, height=100,
                                    font_size='20sp')

        # Add new buttons to the container
        for button in [self.is_event_button, self.invites_button, self.date_button]:
            self.action_buttons_container_top.add_widget(button)
        for button in [self.time_button, self.location_button, self.future_button]:
            self.action_buttons_container_bottom.add_widget(button)


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
        self.root.add_widget(self.action_buttons_container_top)
        self.root.add_widget(self.action_buttons_container_bottom)
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

    def mark_is_event(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 5:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (5 - len(self.csv_data[self.current_row])))
        if self.csv_data[self.current_row][4] == "event":
            self.csv_data[self.current_row][4] = "no_event"
        else:
            self.csv_data[self.current_row][4] = "event"
        self.update_csv()
        self.update_labels(self.current_row)

    def mark_invites(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 6:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (6 - len(self.csv_data[self.current_row])))
            if self.csv_data[self.current_row][5] == "invites":
                self.csv_data[self.current_row][5] = "no_invites"
            else:
                self.csv_data[self.current_row][5] = "invites"
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_date(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 7:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (7 - len(self.csv_data[self.current_row])))
            if self.csv_data[self.current_row][6] == "date":
                self.csv_data[self.current_row][6] = "no_date"
            else:
                self.csv_data[self.current_row][6] = "date"
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_time(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 8:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (8 - len(self.csv_data[self.current_row])))
            if self.csv_data[self.current_row][7] == "time":
                self.csv_data[self.current_row][7] = "no_time"
            else:
                self.csv_data[self.current_row][7] = "time"
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_location(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 9:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (9 - len(self.csv_data[self.current_row])))
            if self.csv_data[self.current_row][8] == "location":
                self.csv_data[self.current_row][8] = "no_location"
            else:
                self.csv_data[self.current_row][8] = "location"
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_future(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 10:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (10 - len(self.csv_data[self.current_row])))
            if self.csv_data[self.current_row][9] == "future":
                self.csv_data[self.current_row][9] = "no_future"
            else:
                self.csv_data[self.current_row][9] = "future"
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
                # elif i == 4:
                #     label = Label(text=item, font_size='20sp', size_hint_y=None, halign='left', valign='top')
                else:
                    label = Label(text=item, font_size='20sp', size_hint_y=None, halign='left', valign='top')
                label_width = self.scroll_view.width - 2 * self.labels_container.padding[0] - 20
                label.text_size = (label_width, None)
                label.bind(texture_size=lambda instance, value: setattr(instance, 'size', (label_width, value[1])))
                self.labels_container.add_widget(label)
        else:
            self.labels_container.add_widget(Label(text='End of file reached!', font_size='20sp'))

    def next_row(self, instance):
        if ONLY_SHOW_ISEVENT:
            for i in range(self.current_row + 1, len(self.csv_data)):
                if 'isEvent' in self.csv_data[i][4] or 'isEvent' in self.csv_data[i][5] or 'isEvent' in self.csv_data[6]:
                    self.current_row = i
                    if self.current_row < len(self.csv_data):
                        self.update_labels(self.current_row)
                    else:
                        self.current_row = len(self.csv_data) - 1  # Prevent going beyond the last row
                        self.next_row_button.disabled = True
                    self.previous_row_button.disabled = False
                    break
        else:
            self.current_row += 1
            if self.current_row < len(self.csv_data):
                self.update_labels(self.current_row)
            else:
                self.current_row = len(self.csv_data) - 1  # Prevent going beyond the last row
                self.next_row_button.disabled = True
            self.previous_row_button.disabled = False

    def previous_row(self, instance):
        if ONLY_SHOW_ISEVENT:
            for i in range(self.current_row - 1, -1, -1):
                if 'isEvent' in self.csv_data[i][4] or 'isEvent' in self.csv_data[i][5] or 'isEvent' in self.csv_data[6]:
                    self.current_row = i
                    if self.current_row < len(self.csv_data):
                        self.update_labels(self.current_row)
                    else:
                        self.current_row = len(self.csv_data) - 1  # Prevent going beyond the last row
                        self.next_row_button.disabled = True
                    self.previous_row_button.disabled = False
                    break
        else:
            if self.current_row > 0:
                self.current_row -= 1
                self.update_labels(self.current_row)
                self.next_row_button.disabled = False

if __name__ == '__main__':
    CsvRowApp().run()


