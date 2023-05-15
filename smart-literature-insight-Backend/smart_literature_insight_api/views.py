from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import json

# code to generate output
import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration
from .ml_code import generate


# Create your views here.
@api_view(['GET'])
def index(request):
    return_data = {
        "error_code" : "0",
        "info" : "success",
    }
    return Response(return_data)

@api_view(["POST"])
def giveAnswer(request):
    try:
        data = json.loads(request.body)
        question = data['data']['question']
        paragraph = data['data']['paragraph']
        
        ret = generate(question, paragraph)
        print(ret)
        _response = {
            'info': 'success',
            "Access-Control-Allow-Origin": "*",
            'answer': ret,
        }

    except ValueError as ve:
        _response = {
            'error_code' : '-1',
            "Access-Control-Allow-Origin": "*",
            "info": str(ve)
        }
    return Response(_response)