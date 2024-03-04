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
                if self.csv_data[i][7] == 'isEvent' or self.csv_data[i][7] == 'isNotEvent':
                    self.current_row = i
            except:
                pass



        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.action_buttons_container = BoxLayout(size_hint_y=None, height=80)  # Adjusted height for more buttons

        # Define new buttons
        self.invites_button = Button(text="Inv", on_press=self.mark_invites, size_hint_y=None, height=80,
                                     font_size='20sp')
        self.date_button = Button(text="Dat", on_press=self.mark_date, size_hint_y=None, height=80, font_size='20sp')
        self.location_button = Button(text="Loc", on_press=self.mark_location, size_hint_y=None, height=80,
                                      font_size='20sp')
        self.loose_button = Button(text="Tun", on_press=self.mark_loose, size_hint_y=None, height=80,
                                   font_size='20sp')
        self.future_button = Button(text="Fut", on_press=self.mark_future, size_hint_y=None, height=80,
                                    font_size='20sp')

        # Add new buttons to the container
        for button in [self.invites_button, self.date_button, self.location_button, self.loose_button,
                       self.future_button]:
            self.action_buttons_container.add_widget(button)




        self.no_action_buttons_container = BoxLayout(size_hint_y=None, height=80)  # Adjusted height for more buttons

        # Define new buttons
        self.no_invites_button = Button(text="NoInv", on_press=self.no_mark_invites, size_hint_y=None, height=80,
                                     font_size='20sp')
        self.no_date_button = Button(text="NoDat", on_press=self.no_mark_date, size_hint_y=None, height=80, font_size='20sp')
        self.no_location_button = Button(text="NoLoc", on_press=self.no_mark_location, size_hint_y=None, height=80,
                                      font_size='20sp')
        self.no_loose_button = Button(text="NoTun", on_press=self.no_mark_loose, size_hint_y=None, height=80,
                                   font_size='20sp')
        self.no_future_button = Button(text="NoFut", on_press=self.no_mark_future, size_hint_y=None, height=80,
                                    font_size='20sp')

        # Add new buttons to the container
        for button in [self.no_invites_button, self.no_date_button, self.no_location_button, self.no_loose_button,
                       self.no_future_button]:
            self.no_action_buttons_container.add_widget(button)

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
        self.root.add_widget(self.no_action_buttons_container)
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

    def mark_invites(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 5:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (5 - len(self.csv_data[self.current_row])))
        self.csv_data[self.current_row][4] = "invites"
        self.update_csv()
        self.update_labels(self.current_row)

    def mark_date(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 6:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (6 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][5] = "date"
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_location(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 7:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (7 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][6] = "location"
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_loose(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 8:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (8 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][7] = "stay tuned"
            self.update_csv()
            self.update_labels(self.current_row)

    def mark_future(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 9:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (9 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][8] = "future"
            self.update_csv()
            self.update_labels(self.current_row)


    def no_mark_invites(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 5:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (5 - len(self.csv_data[self.current_row])))
        self.csv_data[self.current_row][4] = "no invites"
        self.update_csv()
        self.update_labels(self.current_row)

    def no_mark_date(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 6:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (6 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][5] = "no date"
            self.update_csv()
            self.update_labels(self.current_row)

    def no_mark_location(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 7:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (7 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][6] = "no location"
            self.update_csv()
            self.update_labels(self.current_row)

    def no_mark_loose(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 8:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (8 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][7] = "no stay tuned"
            self.update_csv()
            self.update_labels(self.current_row)

    def no_mark_future(self, instance):
        if 0 <= self.current_row < len(self.csv_data):
            if len(self.csv_data[self.current_row]) < 9:
                # If so, extend the row with empty values up to the 8th column
                self.csv_data[self.current_row].extend([""] * (9 - len(self.csv_data[self.current_row])))
            self.csv_data[self.current_row][8] = "no future"
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


