import sys
import os.path
import logging
import urllib.request
import hashlib
import markovify
import json


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
    write_buffer.encode('utf-8')
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


def model_is_present(title):
    """Parameters: string that represents title in "available_works"
    Returns: model object, ensures model is created at file get_model_name()"""
    file_name = get_file_name(title)
    model_name = get_model_name(title)
    if os.path.isfile(model_name):
        log.info('Model alredy present for "%s"', title)
        model = read_model(model_name)
    else:
        log.info('Creating and saving model of %s to %s', title, model_name)
        model =  build_model(file_name, model_name)
    return model


# Modified from lyricwriter module
def build_model(file_name, model_name):
    """Parameters: file name of text to modeled
                   file name for saving model
    Returns: a markovify model object, and writes model to file_name+.model"""
    with open(file_name) as file_:
        text = file_.read()
    log.debug('Creating model from %s', file_name)
    model = markovify.Text(text)
    write_model(model, model_name)
    return model


# Modified from lyricwriter module
def read_model(model_name):
    """Parameters: file name of saved model
    Returns: model object"""
    with open(model_name, 'r') as f:
        model_json = json.load(f)
        model = markovify.NewlineText.from_json(
            model_json
        )
        return model


# Modified from lyricwriter module
def write_model(model, model_name):
    """Parameters: model object, file name of model's *original text*
    Returns: none, writes model to .model file in json format"""
    model_json = model.to_json()
    log.debug('Writing model to %s', model_name)
    with open(model_name, 'w') as f:
        json.dump(model_json, f)


def get_model(title):
    """Parameters: string that represents title in "available_works"
    Returns: Markovify object of that title"""
    file_name = get_file_name(title)
    model_name = get_model_name(title)
    work_is_present(title, file_name)
    model = model_is_present(title)
    return model


def get_sentence(title):
    """Parameters: string that represents title in "available_works"
    Returns: string of generated sentence for that title"""
    model = get_model(title)
    log.info('Making sentence from "%s"', title)
    sentence = model.make_sentence()
    return sentence


def get_short_sentence(title):
    """Parameters: string that represents title in "available_works"
    Returns: string of generated short sentence for that title"""
    n_chars = 140
    model = get_model(title)
    log.info('Making short sentence from "%s"', title)
    sentence = model.make_short_sentence(n_chars)
    return sentence


def main(title):
    """Parameters: string that represents title in "available_works"
    Returns: none, prints sentence generated from that title"""
    model = get_model(title)
    print(model.make_sentence())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        q = sys.argv[1]
    else:
        sys.exit(1)
    sentence = main(q)
