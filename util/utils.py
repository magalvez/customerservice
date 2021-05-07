from util.exceptions.exceptions import InvalidFileExtension


def validate_document(document_file, extension):
    """
    Validates uploaded document extension
    :param document_file: File, the file to be validated
    :param extension: String, Extension file. Ie, 'txt'
    """
    file_extension = document_file.filename.split('.')[-1].lower()

    if file_extension != extension:
        raise InvalidFileExtension
