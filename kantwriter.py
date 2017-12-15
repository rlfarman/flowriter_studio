import os.path
import logging
import urllib.request
import hashlib


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


available_works = {
    'critique of pure reason': 'http://www.gutenberg.org/cache/epub/4280/pg4280.txt',
    'critique of practical reason': 'http://www.gutenberg.org/cache/epub/5683/pg5683.txt',
    'critique of judgment': 'http://www.gutenberg.org/files/48433/48433-0.txt',
    'prolegomena': 'http://www.gutenberg.org/files/52821/52821-0.txt'
    }


def get_available_works():
    """Parameters: none
    Returns: string with newline-delimited titles"""
    available_works_string = ''
    for key in available_works:
        available_works_string += (key + '\n')
    return available_works_string


def get_file_name(title):
    """Parameters: string that represents title in "available_works"
    Returns: string that represents file name for the work"""
    title_hash = hashlib.sha256(title.encode('utf-8')).hexdigest()
    n_hash_chars = 20
    file_extension = '.txt'
    file_name = title_hash[:n_hash_chars] + file_extension
    return file_name


def get_model_name(title):
    """Parameters: string that represents title in "available_works"
    Returns: string that represents file name for the work's Markov model"""
    file_name = get_file_name(title)
    model_name = file_name + '.model'
    return model_name


def download_work(title, file_name):
    """Parameters: title that is a key in "available_works"
    Returns: none, downloads work to "file_name"
    NOTE: text parsing is included here to deal with info from the sources"""
    log.debug('Downloading text of "%s"', title)
    response = urllib.request.urlopen(available_works[title])
    lines = response.readlines()
    # Text begins with Gutenberg info
    in_body = False
    info_end = '*** START OF THIS PROJECT GUTENBERG EBOOK '
    info_begin = 'End of Project Gutenberg\'s '
    write_buffer = ""
    for data in lines:
        line = data.decode('utf-8')
        # If inside the actual text
        if in_body:
            # Make sure the current line is actual text
            if info_begin in line:
                log.debug('Reached end of body in "%s"', title)
                break
            # If so, save the line
            else:
                write_buffer += line
        # Otherwise check to see if line is end of info section
        else:
            in_body = info_end in line
    file_ = open(file_name, 'w')
    file_.write(write_buffer)
    file_.close()


def work_is_present(title, file_name):
    """Parameters: title that represents a key in "available_works",
                   file name that should hold the work
    Returns: none, downloads work to file_name
             If file is present or downloaded, return 0
             If title not in available_works,  return 1"""
    # Check for valid title
    if title not in available_works:
        log.error('Title not available: %s', title)
        return 1
    # Check if title already downloaded
    elif os.path.isfile(file_name):
        log.info('File alredy present for "%s"', title)
        return 0
    # Otherwise, download title to file_name
    else:
        log.info('Downloading "%s" to %s', title, file_name)
        download_work(title, file_name)
        return 0