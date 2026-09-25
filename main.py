from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Window.clearcolor = (0.10, 0.11, 0.15, 1)

CATEGORIES = {
    "طول": {
        "متر": 1.0,
        "سانتی‌متر": 0.01,
        "میلی‌متر": 0.001,
        "کیلومتر": 1000.0,
        "اینچ": 0.0254,
        "فوت": 0.3048,
        "یارد": 0.9144,
        "مایل": 1609.344,
    },
    "وزن": {
        "کیلوگرم": 1.0,
        "گرم": 0.001,
        "میلی‌گرم": 0.000001,
        "تن": 1000.0,
        "پوند": 0.45359237,
        "اونس": 0.028349523125,
    },
    "دما": {
        "سلسیوس": "C",
        "فارنهایت": "F",
        "کلوین": "K",
    },
    "زمان": {
        "ثانیه": 1.0,
        "دقیقه": 60.0,
        "ساعت": 3600.0,
        "روز": 86400.0,
        "هفته": 604800.0,
    },
    "مساحت": {
        "متر مربع": 1.0,
        "سانتی‌متر مربع": 0.0001,
        "کیلومتر مربع": 1000000.0,
        "هکتار": 10000.0,
        "فوت مربع": 0.09290304,
    },
    "حجم": {
        "لیتر": 1.0,
        "میلی‌لیتر": 0.001,
        "متر مکعب": 1000.0,
        "گالن (آمریکا)": 3.785411784,
    },
    "سرعت": {
        "متر بر ثانیه": 1.0,
        "کیلومتر بر ساعت": 0.2777777778,
        "مایل بر ساعت": 0.44704,
    },
}


def convert(category, value, from_unit, to_unit):
    if category == "دما":
        if from_unit == "سلسیوس":
            c = value
        elif from_unit == "فارنهایت":
            c = (value - 32) * 5 / 9
        else:
            c = value - 273.15

        if to_unit == "سلسیوس":
            return c
        elif to_unit == "فارنهایت":
            return c * 9 / 5 + 32
        else:
            return c + 273.15
    else:
        base = value * CATEGORIES[category][from_unit]
        return base / CATEGORIES[category][to_unit]


class UnitConverter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        title = Label(
            text="[b]مبدل واحد[/b]",
            markup=True,
            font_size="28sp",
            size_hint_y=None,
            height=60,
            color=(0.4, 0.8, 1, 1),
        )
        self.add_widget(title)

        self.category_spinner = Spinner(
            text="طول",
            values=list(CATEGORIES.keys()),
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.4, 0.7, 1),
        )
        self.category_spinner.bind(text=self.on_category_change)
        self.add_widget(self.category_spinner)

        self.input_value = TextInput(
            text="1",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=50,
            font_size="20sp",
            halign="center",
        )
        self.add_widget(self.input_value)

        units_row = GridLayout(cols=2, spacing=10, size_hint_y=None, height=50)

        self.from_spinner = Spinner(
            text="متر",
            values=list(CATEGORIES["طول"].keys()),
            background_color=(0.2, 0.6, 0.4, 1),
        )
        self.to_spinner = Spinner(
            text="سانتی‌متر",
            values=list(CATEGORIES["طول"].keys()),
            background_color=(0.6, 0.4, 0.2, 1),
        )
        units_row.add_widget(self.from_spinner)
        units_row.add_widget(self.to_spinner)
        self.add_widget(units_row)

        convert_btn = Button(
            text="تبدیل",
            size_hint_y=None,
            height=55,
            font_size="20sp",
            background_color=(0.2, 0.6, 1, 1),
        )
        convert_btn.bind(on_press=self.do_convert)
        self.add_widget(convert_btn)

        self.result_label = Label(
            text="نتیجه: —",
            font_size="24sp",
            size_hint_y=None,
            height=80,
            color=(0.9, 0.9, 0.3, 1),
        )
        self.add_widget(self.result_label)

        clear_btn = Button(
            text="پاک کردن",
            size_hint_y=None,
            height=45,
            background_color=(0.5, 0.2, 0.2, 1),
        )
        clear_btn.bind(on_press=self.do_clear)
        self.add_widget(clear_btn)

    def on_category_change(self, spinner, text):
        units = list(CATEGORIES[text].keys())
        self.from_spinner.values = units
        self.to_spinner.values = units
        self.from_spinner.text = units[0]
        self.to_spinner.text = units[1] if len(units) > 1 else units[0]
        self.result_label.text = "نتیجه: —"

    def do_convert(self, instance):
        try:
            value = float(self.input_value.text)
        except ValueError:
            self.result_label.text = "عدد نامعتبر!"
            return

        category = self.category_spinner.text
        from_unit = self.from_spinner.text
        to_unit = self.to_spinner.text

        result = convert(category, value, from_unit, to_unit)
        if abs(result) >= 1e6 or (abs(result) < 1e-3 and result != 0):
            formatted = f"{result:.6e}"
        else:
            formatted = f"{result:.6f}".rstrip("0").rstrip(".")

        self.result_label.text = f"{value} {from_unit} = {formatted} {to_unit}"

    def do_clear(self, instance):
        self.input_value.text = ""
        self.result_label.text = "نتیجه: —"


class UnitConverterApp(App):
    def build(self):
        self.title = "مبدل واحد"
        return UnitConverter()


if __name__ == "__main__":
    UnitConverterApp().run()