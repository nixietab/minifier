import re
import os
import sys
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QCheckBox, QListWidget


class MinifierGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minifier")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.log_label = QLabel("Log:")
        self.layout.addWidget(self.log_label)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.layout.addWidget(self.log_display)

        self.file_list_label = QLabel("Selected Files/Folders:")
        self.layout.addWidget(self.file_list_label)

        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        self.recursive_checkbox = QCheckBox("Recursive")
        self.layout.addWidget(self.recursive_checkbox)

        self.select_button = QPushButton("Select Folder/File")
        self.select_button.clicked.connect(self.select_folder_file)
        self.layout.addWidget(self.select_button)

        self.optimize_button = QPushButton("Optimize")
        self.optimize_button.clicked.connect(self.optimize)
        self.layout.addWidget(self.optimize_button)

        self.selected_files = []

    def log_message(self, message):
        self.log_display.append(message)

    def select_folder_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if directory_path:
            self.selected_files = [directory_path]
            self.update_file_list()

    def update_file_list(self):
        self.file_list.clear()
        for file_path in self.selected_files:
            self.file_list.addItem(file_path)

    def optimize(self):
        if not self.selected_files:
            self.log_message("Please select a folder or file.")
            return

        self.recursive = self.recursive_checkbox.isChecked()
        output_folder = "minified"  # Set output folder here
        for file_path in self.selected_files:
            self.minify(file_path, self.recursive)

        self.log_message(f"Optimization completed. Output folder: {os.path.abspath(output_folder)}")

    def minify(self, input_path, recursive):
        output_folder = "minified"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if os.path.isdir(input_path):
            if recursive:
                self.minify_recursive(input_path, output_folder)
            else:
                for root, _, files in os.walk(input_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.minify_file(file_path, output_folder)
        else:
            self.minify_file(input_path, output_folder)

    def minify_recursive(self, input_folder, output_folder):
        for root, _, files in os.walk(input_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_folder)
                output_directory = os.path.join(output_folder, os.path.dirname(relative_path))
                os.makedirs(output_directory, exist_ok=True)
                self.minify_file(file_path, output_directory)

    def minify_file(self, input_path, output_folder):
        file_name, file_extension = os.path.splitext(os.path.basename(input_path))
        output_path = os.path.join(output_folder, file_name + file_extension)
        minified_content = ""

        if file_extension == ".html":
            with open(input_path, "r") as html_file:
                html_content = html_file.read()
                minified_content = self.minify_html(html_content)
        elif file_extension == ".css":
            with open(input_path, "r") as css_file:
                css_content = css_file.read()
                minified_content = self.minify_css(css_content)
        else:
            self.log_message(f"Unsupported file format for '{input_path}'. Copying file directly.")
            shutil.copyfile(input_path, output_path)
            return

        with open(output_path, "w", encoding="utf-8") as min_file:
            min_file.write(minified_content)

        self.log_message(f"{file_extension.upper()} file '{input_path}' has been minified successfully!")

    @staticmethod
    def minify_html(html):
        html = re.sub(r"<!--(.*?)-->", "", html, flags=re.DOTALL)
        html = re.sub(r">\s+<", "><", html)
        html = html.replace("\n", "")
        return html

    @staticmethod
    def minify_css(css):
        css = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", css)
        css = re.sub(r"\s+", " ", css)
        css = re.sub(r"\s?([:,;{}])\s?", r"\1", css)
        css = re.sub(r"([^:])\s?(\{)", r"\1\2", css)
        return css


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinifierGUI()
    window.show()
    sys.exit(app.exec_())
import re
import os
import sys
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QCheckBox, QListWidget


class MinifierGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML and CSS Minifier")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.log_label = QLabel("Log:")
        self.layout.addWidget(self.log_label)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.layout.addWidget(self.log_display)

        self.file_list_label = QLabel("Selected Files/Folders:")
        self.layout.addWidget(self.file_list_label)

        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        self.recursive_checkbox = QCheckBox("Recursive")
        self.layout.addWidget(self.recursive_checkbox)

        self.select_button = QPushButton("Select Folder/File")
        self.select_button.clicked.connect(self.select_folder_file)
        self.layout.addWidget(self.select_button)

        self.optimize_button = QPushButton("Optimize")
        self.optimize_button.clicked.connect(self.optimize)
        self.layout.addWidget(self.optimize_button)

        self.selected_files = []

    def log_message(self, message):
        self.log_display.append(message)

    def select_folder_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if directory_path:
            self.selected_files = [directory_path]
            self.update_file_list()

    def update_file_list(self):
        self.file_list.clear()
        for file_path in self.selected_files:
            self.file_list.addItem(file_path)

    def optimize(self):
        if not self.selected_files:
            self.log_message("Please select a folder or file.")
            return

        self.recursive = self.recursive_checkbox.isChecked()
        output_folder = "minified"  # Set output folder here
        for file_path in self.selected_files:
            self.minify(file_path, self.recursive)

        self.log_message(f"Optimization completed. Output folder: {os.path.abspath(output_folder)}")

    def minify(self, input_path, recursive):
        output_folder = "minified"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if os.path.isdir(input_path):
            if recursive:
                self.minify_recursive(input_path, output_folder)
            else:
                for root, _, files in os.walk(input_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.minify_file(file_path, output_folder)
        else:
            self.minify_file(input_path, output_folder)

    def minify_recursive(self, input_folder, output_folder):
        for root, _, files in os.walk(input_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_folder)
                output_directory = os.path.join(output_folder, os.path.dirname(relative_path))
                os.makedirs(output_directory, exist_ok=True)
                self.minify_file(file_path, output_directory)

    def minify_file(self, input_path, output_folder):
        file_name, file_extension = os.path.splitext(os.path.basename(input_path))
        output_path = os.path.join(output_folder, file_name + file_extension)
        minified_content = ""

        if file_extension == ".html":
            with open(input_path, "r") as html_file:
                html_content = html_file.read()
                minified_content = self.minify_html(html_content)
        elif file_extension == ".css":
            with open(input_path, "r") as css_file:
                css_content = css_file.read()
                minified_content = self.minify_css(css_content)
        else:
            self.log_message(f"Unsupported file format for '{input_path}'. Copying file directly.")
            shutil.copyfile(input_path, output_path)
            return

        with open(output_path, "w", encoding="utf-8") as min_file:
            min_file.write(minified_content)

        self.log_message(f"{file_extension.upper()} file '{input_path}' has been minified successfully!")

    @staticmethod
    def minify_html(html):
        html = re.sub(r"<!--(.*?)-->", "", html, flags=re.DOTALL)
        html = re.sub(r">\s+<", "><", html)
        html = html.replace("\n", "")
        return html

    @staticmethod
    def minify_css(css):
        css = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", css)
        css = re.sub(r"\s+", " ", css)
        css = re.sub(r"\s?([:,;{}])\s?", r"\1", css)
        css = re.sub(r"([^:])\s?(\{)", r"\1\2", css)
        return css


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinifierGUI()
    window.show()
    sys.exit(app.exec_())
