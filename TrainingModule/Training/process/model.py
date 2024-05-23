from transformers import BertModel, BertTokenizer
import torch
from langchain_openai import OpenAI
import langchain.chains 
from openai import OpenAI

import tiktoken
from transformers import GPT2Tokenizer

from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import logging
from django.conf import settings

########
# from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
# from langchain.chat_models import ChatOpenAI
from langchain_community.llms import VertexAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter


from transformers import BartForConditionalGeneration, BartTokenizer

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI



logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

#All the vector embedding Models

#Model Name pre-trained BERT Model
#Target file type PDF
def generate_document_vector_bert (text):
    # Load pre-trained BERT model and tokenizer
    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    tokens = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        output = model(**tokens)
    embeddings = output.last_hidden_state.mean(dim=1).squeeze().numpy()
    serial_vector = embeddings.tolist()
    return serial_vector




def generate_document_vector_openai (text):

    truncated_token = truncate_text_tokens (text, settings.OPEN_AI_PDF_EMBEDDING_ENCODING, int(settings.OPEN_AI_PDF_EMBEDDING_CTX_LENGTH) )
    response = client.embeddings.create(model= settings.OPEN_AI_PDF_EMBEDDING_MODEL,
    input=truncated_token)
    embeddings = response.data[0].embedding
    print (len(embeddings))
    return embeddings

def truncate_text_tokens(text, encoding_name, max_tokens):
    # runcate a string to have `max_tokens` according to the given encoding
    encoding = tiktoken.get_encoding(encoding_name)
    return encoding.encode(text)[:max_tokens]
     

def summarize_combined_text(texts):
    max_tokens_per_chunk = 3500
    #chunks = split_text_by_tokens(text, max_tokens_per_chunk)
    summary = ''
    for  text in texts:
        print ("-------------Hit ----------")
        response = client.completions.create(model="gpt-3.5-turbo-instruct",    #gpt-3.5-turbo-instruct
        prompt=f"Rephrase the following text like an answer, ignore any broken sentence but don't discard any information: {text}",
        temperature=0.9,
        max_tokens=200,  # You may adjust this based on how concise or detailed you want the summary to be
        top_p=0.8,
        frequency_penalty=0.0,
        presence_penalty=0.0)
        print (response.choices[0].text.strip())
        summary = summary + response.choices[0].text.strip() + "\n"
    
    return summary

####### Generating related question ##########

def generate_prompt(texts, num_questions=settings.NUM_RELATED_QUESTIONS):
    max_tokens_per_chunk = 3500
    summary = []

    prompt_variations = [
    "Given the following topic, create a question that would help in context of {previous_question}.\n\nTopic: {previous_question}\n\nYour Question:",
    "From the topic provided below, formulate a question suitable for context of {previous_question}.\n\nTopic: {previous_question}\n\nYour Question:",
    "Imagine a user wants to know more about {previous_question}. Create a relevant question for them.\n\nTopic: {previous_question}\n\nYour Question:"
    # Add more prompt variations here as needed
]

    prompt_index = 0
    try:
        previous_question = texts  # Initialize the previous question with the initial text
        
        for _ in range(num_questions):
            # Choose a prompt variation from the sequence
            prompt = prompt_variations[prompt_index]
            
            response = client.completions.create(model="gpt-3.5-turbo-instruct",  
            prompt=prompt.format(previous_question=previous_question),
            temperature=0.7,
            max_tokens=128,  # You may adjust this based on how concise or detailed you want the summary to be
            top_p=0.7,
            frequency_penalty=0.0,
            presence_penalty=0.0)
            
            generated_question = response.choices[0].text.strip()
            summary.append(generated_question)
            
            # Update prompt index for the next iteration
            prompt_index = (prompt_index + 1) % len(prompt_variations)
            
            # Update previous question for the next iteration
            previous_question = generated_question
    except Exception as e:
        logging.error(f"Error creating Queries : {e}") 
    return summary



# Function to split text into chunks based on token count
def split_text_by_tokens(text, max_tokens_per_chunk):
    # Initialize the tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokens = tokenizer.encode(text)
    # Tokenize the entire text to get tokens

    # Initialize variables to hold chunks and current chunk information
    chunks = []
    current_chunk = []

    for token in tokens:
        # If adding this token does not exceed the max limit, add it to the current chunk
        if len(current_chunk) + 1 <= max_tokens_per_chunk:
            current_chunk.append(token)
        else:
            # When the current chunk is full, decode it back to text and start a new chunk
            chunks.append(tokenizer.decode(current_chunk))
            current_chunk = [token]

    if current_chunk:
        chunks.append(tokenizer.decode(current_chunk))
    

    return chunks


def summarize_combined_text_lc(data):
    model_name = "gpt-3.5-turbo" # also we can use gpt-3.5-turbo
    
    # Create a text splitter from the tiktoken encoder
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        model_name=model_name
    )
    
    # Prompt template for summarization
    # prompt_template = """Given the following information:
    #     {text}
    #     generate a summary that starts with the greeting "Dear Requestor," which provides a clear, comprehensive overview of the main points, conclusions, or recommendations based on the provided information. End with "Thank you."
    # """

    prompt_template = """Given the following information:
    {text}
    generate a summary that starts with the greeting "Dear Requestor," which provides a clear, comprehensive overview of the main points, conclusions, or recommendations based on the provided information. Present your summary in bullet points. End with "Thank you."
    """

    
    # Instantiate ChatOpenAI with specified model and API key
    llm = ChatOpenAI(temperature=0.5, openai_api_key=settings.OPENAI_API_KEY, model_name=model_name)
    
    # Create a prompt using the prompt template
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    
    # Load the summarize chain with map-reduce method using the specified LLM and prompts
    chain = load_summarize_chain(
        llm, 
        chain_type="map_reduce",
        map_prompt=prompt,
        combine_prompt=prompt,
        verbose=False
    )
    
    # Combine all data into a single string
    data_text = '\n'.join(data)
    
    # Split the data text into smaller chunks using the text splitter
    texts = text_splitter.split_text(data_text)
    
    # Convert each chunk into a document
    docs = [Document(page_content=text) for text in texts]
    
    # Invoke the chain with the documents and get the summary
    final_summary = chain.invoke(docs)
    
    # Access the 'output_text' key from the dictionary
    final_summary_text = final_summary.get('output_text', '')
    
    # Refine the summary to be more human-readable and around 200 words
    refined_summary = refine_summary(final_summary_text, target_words=200)
    
    print(refined_summary)
    return refined_summary

def refine_summary(summary_text, target_words):
    # Split the summary into sentences
    sentences = summary_text.split('. ')
    
    # Initialize variables
    refined_summary = ''
    word_count = 0
    
    # Iterate through sentences and add them to the refined summary until target_words is reached
    for sentence in sentences:
        # Check if adding the next sentence would exceed the word limit
        if word_count + len(sentence.split()) <= target_words:
            refined_summary += sentence + '. '
            word_count += len(sentence.split())
        else:
            break
    
    return refined_summary.strip()  # Remove trailing whitespace


# Refine query

def query_refiner(query):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Given the following user query, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base and also make the correct spelling of the words given in the query and it should be gramatically correct and the sentence should be sound good\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.7,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    refined_query = response.choices[0].text.strip()
    return refined_query