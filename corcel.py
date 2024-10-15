import requests
import json
import sys
import time

from typing import List, Optional, Union, Iterator

class Url: 
    CHAT = "https://api.corcel.io/v1/chat/completions"

class Model: 
    GPT_4o = "gpt-4o"
    GPT_3_DOT_5_TURBO = "gpt-3.5-turbo"

class Message: 
    class Role:
        USER = "user"
        SYSTEM = "system"
        ASSISTANT = "assistant"

    def __init__(self, role, content): 
        self.role = role
        self.content = content

    def __str__(self): 
        content = self.content.replace("\n", "\\n")
        return "Message(role=%s, content=%s)" % (self.role, content)
    
    def to_dict(self): 
        return dict(role=self.role, content=self.content)

class Headers: 
    @staticmethod
    def get() -> dict: 
        headers = {}
        headers["accept"] = "application/json"
        headers["content-type"] = "application/json"
        headers["Authorization"] = Corcel.API_KEY

        return headers.copy()

class Payload: 
    def __init__(
        self,
        prompt: str,
        system_instruction: str = "",
        messages: Optional[List[Message]] = [],
        model: Model = Model.GPT_4o,
        stream: bool = True,
        top_p: float = 1,
        temperature: float = 0.0001,
        max_tokens: int = 4096
    ) -> dict: 

        payload = {}
        payload["model"] = model
        payload["stream"] = stream
        payload["top_p"] = top_p
        payload["temperature"] = temperature
        payload["max_tokens"] = max_tokens

        if system_instruction: 
            role = Message.Role.SYSTEM
            messages.append(dict(role=role, content=system_instruction))

        role = Message.Role.USER
        messages.append(dict(role=role, content=prompt))
        
        payload["messages"] = messages

        self.payload = payload
    
    def json(self) -> dict: 
        return self.payload

    def serialize(self) -> dict: 
        payload = self.payload.copy()
        messages = []
        for message in payload["messages"]: 
            role, content = message.values()
            messages.append(Message(role=role,content=content))

        payload["message"] = messages
        return payload
        
        
class Corcel: 
    API_KEY = "46f8f6ee-4c95-4eb4-871d-f0fcb265b753"
        
    def chat_yield_wrapper(self, response: requests.Response) -> Iterator[str]: 
        for chunk in response.iter_lines(): 
            chunk = chunk.decode("utf-8")
            if chunk.startswith("data: ") and not chunk.startswith("data: [DONE]"): 
                raw_data = chunk.lstrip("data: ") 
                content = json.loads(raw_data)
                delta = content["choices"][0]["delta"]

                yield delta["content"] if delta.get("content") else ""
                
    def chat(
        self,
        prompt: str,
        stream: bool = False,
        model: Model = Model.GPT_4o,
        history: Optional[List[str]] = None,
        **kwargs
    ) -> Union[str, Iterator[str]]: 
        
        if history is None: 
            history = []

        headers = Headers.get()
        payload = Payload(prompt, model=model, stream=stream, messages=history, **kwargs)

        while True: 
            try: 
                response = requests.post(Url.CHAT, json=payload.json(), headers=headers)

                if response.status_code == 200: 
                    resp = ""
                    for chunk in response.iter_lines(): 
                        if chunk: 
                            chunk = chunk.decode("utf-8") or ""
                            chunk = chunk.lstrip("data:").strip()

                            if chunk.startswith("[DONE]"): 
                                break
                            
                            completion = json.loads(chunk)
                            choices = completion["choices"]
                            if choices: 
                                text = choices[0]["delta"]["content"]
                                resp += text

                    role = Message.Role.ASSISTANT
                    history.append(dict(role=role, content=text))
                    return resp
            except Exception as e: 
                print("Error: ",e)
                return
            
            time.sleep(2)

if __name__ == "__main__": 
    provider = Corcel()
    prompt = """What animal is the most poisonous in the world?

A. Poison dart frog
B. Cobra
C. Black widow spider
D. Black Mamba"""
    # prompt = "1 + 1 berapa jawabannya?"
    stream = False
    model = Model.GPT_4o
    loop = False
    history = []
    
    resp = provider.chat("1+1 berapa jangan dijawab dulu", model=model)
    resp = provider.chat("sekarang boleh kamu jawab", model=model)
    print(resp)
    # while True: 
    #     result = provider.chat(prompt, stream=stream, model=model, history=history)
    #     if stream: 
    #         import time

    #         for text in result: 
    #             print(text, flush=True, end="")
    #             time.sleep(0.05)
    #         print()
    #     else:     
    #         print(result)
        
    #     if not loop: 
    #         break
