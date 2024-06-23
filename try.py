import codecs

def convert_encoding(input_file_path, output_file_path, source_encoding='cp949'):
    # Open the source file with the specified source encoding
    with codecs.open(input_file_path, 'r', encoding=source_encoding) as file:
        content = file.read()

    # Write the content to a new file, encoding it in UTF-8
    with codecs.open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Specify the path to your existing file and the output file
convert_encoding('data.json', 'converted_data.json')
