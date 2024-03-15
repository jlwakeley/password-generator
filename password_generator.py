import sys
import secrets
import string
import pyperclip  # type: ignore # noqa: PGH003
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QMessageBox,
    QCheckBox,
)


def calculate_password_strength(password: str) -> int:
    # Calculate password strength based on length and character variety
    length_strength = min(len(password) // 4, 5)
    variety_strength = len(set(password)) // 4
    return min(length_strength + variety_strength, 10)


class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle("Password Generator")
        self.resize(400, 300)  # Set the size of the window
        layout = QVBoxLayout()

        excluded_symbols_label = QLabel("Exclude what symbols?")
        self.excluded_symbols_entry = QLineEdit()
        layout.addWidget(excluded_symbols_label)
        layout.addWidget(self.excluded_symbols_entry)

        length_label = QLabel("Length requirement?")
        self.length_entry = QLineEdit()
        layout.addWidget(length_label)
        layout.addWidget(self.length_entry)

        self.require_upper_checkbox = QCheckBox("Require at least one uppercase letter")
        layout.addWidget(self.require_upper_checkbox)

        self.require_lower_checkbox = QCheckBox("Require at least one lowercase letter")
        layout.addWidget(self.require_lower_checkbox)

        self.require_special_checkbox = QCheckBox(
            "Require at least one special character"
        )
        layout.addWidget(self.require_special_checkbox)

        self.password_strength_label = QLabel()
        layout.addWidget(self.password_strength_label)

        generate_button = QPushButton("Generate Password")
        generate_button.clicked.connect(self.generate_password_clicked)
        layout.addWidget(generate_button)

        self.password_display = QTextEdit()
        self.password_display.setReadOnly(True)
        layout.addWidget(self.password_display)

        copy_button = QPushButton("Copy to Clipboard")
        copy_button.clicked.connect(self.copy_to_clipboard_clicked)
        layout.addWidget(copy_button)

        self.setLayout(layout)

    def generate_password_clicked(self) -> None:
        require_upper = self.require_upper_checkbox.isChecked()
        require_lower = self.require_lower_checkbox.isChecked()
        require_special = self.require_special_checkbox.isChecked()
        password = self.generate_password(require_upper, require_lower, require_special)
        self.update_password_strength(password)
        self.password_display.setPlainText(password)
        pyperclip.copy(password)

    def generate_password(
        self, require_upper: bool, require_lower: bool, require_special: bool
    ) -> str:
        excluded_symbols = self.excluded_symbols_entry.text()
        length = self.length_entry.text()
        try:
            length = int(length)  # type: ignore # noqa: PGH003
            if length <= 0:  # type: ignore # noqa: PGH003
                raise ValueError()
        except ValueError:
            show_error_message(
                "Invalid length requirement. Please input a positive integer."
            )
            return ""

        char_symb = string.ascii_lowercase + string.digits
        if require_upper:
            char_symb += string.ascii_uppercase
        if require_special:
            char_symb += string.punctuation

        for char in excluded_symbols:
            char_symb = char_symb.replace(char, "")

        if not char_symb:
            raise ValueError(
                "All symbols, numbers, and letters are excluded. Please try again."
            )

        password = "".join(secrets.choice(char_symb) for _ in range(length))  # type: ignore # noqa: PGH003

        if require_lower and not any(char.islower() for char in password):
            password = secrets.choice(string.ascii_lowercase) + password[1:]

        if require_upper and not any(char.isupper() for char in password):
            password = secrets.choice(string.ascii_uppercase) + password[1:]

        if require_special and not any(char in string.punctuation for char in password):
            password = password[:-1] + secrets.choice(string.punctuation)

        return password

    def update_password_strength(self, password: str) -> None:
        strength = calculate_password_strength(password)
        if strength < 4:
            self.password_strength_label.setText("Password Strength: Weak")
            self.password_strength_label.setStyleSheet("color: red")
        elif strength < 8:
            self.password_strength_label.setText("Password Strength: Moderate")
            self.password_strength_label.setStyleSheet("color: orange")
        else:
            self.password_strength_label.setText("Password Strength: Strong")
            self.password_strength_label.setStyleSheet("color: green")

    def copy_to_clipboard_clicked(self) -> None:
        password = self.password_display.toPlainText()
        pyperclip.copy(password)


def show_error_message(message: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(message)
    msg.setWindowTitle("Error")
    msg.exec_()


def main() -> None:
    app = QApplication(sys.argv)
    ex = PasswordGeneratorApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
