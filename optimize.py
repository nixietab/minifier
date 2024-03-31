import re
import os
import argparse
import shutil

def minify_html(html):
    html = re.sub(r"<!--(.*?)-->", "", html, flags=re.DOTALL)
    html = re.sub(r">\s+<", "><", html)
    html = html.replace("\n", "")
    return html

def minify_css(css):
    css = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s?([:,;{}])\s?", r"\1", css)
    css = re.sub(r"([^:])\s?(\{)", r"\1\2", css)
    return css

def minify_file(input_path, output_folder):
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    file_name, file_extension = os.path.splitext(os.path.basename(input_path))
    output_path = os.path.join(output_folder, file_name + file_extension)
    minified_content = ""

    if file_extension == ".html":
        with open(input_path, "r") as html_file:
            html_content = html_file.read()
            minified_content = minify_html(html_content)
    elif file_extension == ".css":
        with open(input_path, "r") as css_file:
            css_content = css_file.read()
            minified_content = minify_css(css_content)
    else:
        print(f"Unsupported file format for '{input_path}'. Copying file directly.")
        shutil.copyfile(input_path, output_path)
        return

    with open(output_path, "w", encoding="utf-8") as min_file:
        min_file.write(minified_content)

    print(f"{file_extension.upper()} file '{input_path}' has been minified successfully!")

def main():
    parser = argparse.ArgumentParser(description="HTML and CSS minifier")
    parser.add_argument("path", help="Path to the file or folder to be minified")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive mode")
    args = parser.parse_args()

    input_path = args.path
    output_folder = "minified"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if os.path.isdir(input_path):
        if args.recursive:
            minify_recursive(input_path, output_folder)
        else:
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    minify_file(file_path, output_folder)
    else:
        minify_file(input_path, output_folder)

def minify_recursive(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, input_folder)
            output_directory = os.path.join(output_folder, os.path.dirname(relative_path))
            os.makedirs(output_directory, exist_ok=True)
            minify_file(file_path, output_directory)

if __name__ == "__main__":
    main()
