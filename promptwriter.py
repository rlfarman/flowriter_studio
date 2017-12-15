import markovify
import json

def build_model(txt_file):
    """Builds a markov model for an artist."""
    with open(txt_file) as f:
        text = f.read()

    # Build the model.
    model = markovify.NewlineText(text)
    write_model(model)
    return(model)

def write_model(model):
    """Writes a markov model to the file promptmodel.json."""
    model_json = model.to_json()
    file_name = 'promptmodel.json'
    with open(file_name, 'w') as f:
        json.dump(model_json, f)

def read_model(file_name):
    """Reades a markov model from a file corresponding to artist ID."""
    with open(file_name, 'r') as f:
        model_json = json.load(f)
        model = markovify.NewlineText.from_json(model_json)
        return(model)

def get_model(prompt_model):
    """Either loads a model from memory or builds one from scratch."""
    try:
        file_name = "promptmodel.json"
        model = read_model(file_name)
    except Exception:
        model = build_model(prompt_model)
    return(model)

def make_sentence(model):
    """Construct a sentence."""
    while True:
        sentence = model.make_sentence(max_overlap_total=6)
        if sentence:
            return(sentence)


def generate_prompt():
    txt_file = "650prompts.txt"

    model = get_model(txt_file)
    sentence = make_sentence(model)
    
    return sentence

    # sentences_list
    # Get raw text as string.
    
    #with open(txt_file) as f:
    #    text = f.read()

    # Build the model.
    #text_model = markovify.NewlineText(text)

    # Print five randomly-generated sentences
    #for i in range(5):
        #print(text_model.make_sentence())

    # Print three randomly-generated sentences of no more than 140 characters
    #for i in range(3):
        #print(text_model.make_short_sentence(140))

    # Print three randomly-generated sentences of no more than 140 characters
    #for i in range(num_sentences):
    #    sentences_list.append(text_model.make_sentence(max_words=length))
    
    return(text_model.make_sentence())

def main():
    """Generates a writing prompt"""
    #print("Writing Prompt generator v0.1")
    return(generate_prompt())


if __name__ == '__main__':
    sentence = main()
    print(sentence)
