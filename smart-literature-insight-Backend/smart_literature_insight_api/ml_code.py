import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration
import warnings
# import os

warnings.filterwarnings("ignore")



    # Split the paragraph into chunks of length 512
    # Chunking on character size
    

    # chunking on word count
    # paragraph = paragraph.split()
    # chunks = []
    # for i in range(0, len(paragraph), chunk_size):
    #   chunks.append(" ".join(paragraph[i:i+chunk_size]))


def generate(question, paragraph):

    #Model
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

    #Tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    chunk_size = 512
    chunks = [paragraph[i:i+chunk_size] for i in range(0, len(paragraph), chunk_size)]

    answers = []
    progress = 1
    for chunk in chunks[:25]:
        encoding = tokenizer.encode_plus(text=question,text_pair=chunk, max_length=chunk_size, truncation=True)

        inputs = encoding['input_ids']  #Token embeddings
        sentence_embedding = encoding['token_type_ids']  #Segment embeddings
        tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens

        start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]), return_dict=False)

        start_index = torch.argmax(start_scores)
        end_index = torch.argmax(end_scores)
        answer = ' '.join(tokens[start_index:end_index+1])

        corrected_answer = ''
        for word in answer.split():
            #If it's a subword token
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word
            
        print(progress, corrected_answer)
        progress += 1
        answers.append(corrected_answer)

    # BART
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    torch_device = 'cpu'
    prefix = "context: "
    def bart_summarize(text, num_beams=4, length_penalty=2.0, max_length=142, min_length=56, no_repeat_ngram_size=3):
    
        text = text.replace('\n','')
        text_input_ids = tokenizer.batch_encode_plus([text], return_tensors='pt', max_length=1024)['input_ids'].to(torch_device)
        summary_ids = model.generate(text_input_ids, num_beams=int(num_beams), length_penalty=float(length_penalty), max_length=int(max_length), min_length=int(min_length), no_repeat_ngram_size=int(no_repeat_ngram_size), do_sample=True)           
        summary_txt = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
        return summary_txt

    answers = " ".join(answers)
    return bart_summarize(answers)