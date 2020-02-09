from PyQt5.QtGui import QPalette, QColor, QFont

def set_style(app):
    app.setStyle(Style.style())
    app.setPalette(Style())
    app.setStyleSheet(Style.style_sheet())
    app.setFont(Style.set_font())


class Style(QPalette):
    style_dark = True

    def __init__(self, *args):
        super().__init__(*args)
        if Style.style_dark:
            # https://github.com/gmarull/qtmodern
            self.setColor(QPalette.WindowText, QColor(255, 255, 255))
            self.setColor(QPalette.Button, QColor(53, 53, 53))
            self.setColor(QPalette.Light, QColor(255, 255, 255))
            self.setColor(QPalette.Midlight, QColor(90, 90, 90))
            self.setColor(QPalette.Dark, QColor(35, 35, 35))
            self.setColor(QPalette.Text, QColor(255, 255, 255))
            self.setColor(QPalette.BrightText, QColor(255, 255, 255))
            self.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            self.setColor(QPalette.Base, QColor(65, 65, 130))  # !
            self.setColor(QPalette.Window, QColor(53, 53, 53))
            self.setColor(QPalette.Shadow, QColor(20, 20, 20))
            self.setColor(QPalette.Highlight, QColor(42, 130, 218))
            self.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            self.setColor(QPalette.Link, QColor(56, 252, 196))
            self.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
            self.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
            self.setColor(QPalette.ToolTipText, QColor(255, 255, 255))

            # disabled
            self.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
            self.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
            self.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
            self.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
            self.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))

    @staticmethod
    def style_sheet():
        if Style.style_dark:
            return 'QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }'
        else:
            return ''

    @staticmethod
    def style():
        return 'Fusion'

    @staticmethod
    def set_font():
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(40)
        return font
