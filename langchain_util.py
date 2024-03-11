from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret_key import openai_api_key

import os
os.environ['OPENAI_API_KEY'] = openai_api_key
llm = OpenAI(temperature=0.6)


def generate_restaurant_name_and_items(cuisine):
    prompt_restaurant_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_restaurant_name, output_key="restaurant_name")
    prompt_menu_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma separated list."
    )
    menu_items_chain = LLMChain(llm=llm, prompt=prompt_menu_items, output_key="menu_items")
    seq_chain = SequentialChain(
        chains=[name_chain, menu_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )
    response = seq_chain.invoke({'cuisine': cuisine})
    return response
