from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict) :
    messages: Annotated[list[ BaseMessage], add_messages]

def chat_model(state: ChatState) :
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': response}

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_model', chat_model)
graph.add_edge(START, 'chat_model')
graph.add_edge('chat_model', END)

chatbot = graph.compile(checkpointer=checkpointer)

