# =============================================================================
# DEFINE chatGPT function
# Author: Daniel Albert, PhD
# 2024
# da692@drexel.edu
# =============================================================================
import openai
import json


# =============================================================================
# ChatGPT Non-streaming
# Default suggested
# =============================================================================
def chatGPT(prompt, 
            model="gpt-4-turbo-preview", 
            temperature=0.7, 
            max_tokens=4096, 
            top_p=1, 
            tools=None,
            force="auto",
            system_prompt="",
            conversation_history=[]):
        # Prepare the base parameters for the API call
    try:
        message_sequence = [{"role": "system", "content": system_prompt}] + conversation_history + [
            {"role": "user", "content": prompt}
        ]
        
        # Function to simulate typing effect
        

        base_params = {
                "model": model,
                "messages": message_sequence,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
        
            # Include tools if they are provided (not None)
        if tools is not None:
            base_params["tools"] = tools
            base_params["tool_choice"] = force


            
        response = openai.chat.completions.create(**base_params)

        
            # Initialize a dictionary to structure the response
        structured_response = {
                "text": "",
                "function_calls": []
            }
    
            # Check for general message content
        if response.choices[0].message.content:
            structured_response["text"] = response.choices[0].message.content.strip()
    
        # Check for tool outputs or function calls
        if response.choices[0].message.tool_calls:
            tool_calls = response.choices[0].message.tool_calls
            for tool_call in tool_calls:
                 function_call_info = {
                        "function_name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    }
                 structured_response["function_calls"].append(function_call_info)
    
        return structured_response
    except Exception as e:
        return {"error": str(e)} 
    
    

    
# =============================================================================
# STREAMING ChatGPT
# For on the fly assembling
# =============================================================================
def chatGPT_stream(prompt, 
            model="gpt-4-turbo-preview", 
            temperature=0.7, 
            max_tokens=2048, 
            top_p=1, 
            tools=None, 
            system_prompt="",
            conversation_history=[]):
    try:
        # Prepare the base parameters for the API call
        message_sequence = [{"role": "system", "content": system_prompt}] + conversation_history + [
            {"role": "user", "content": prompt}
        ]
                
        base_params = {
                "model": model,
                "messages": message_sequence,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": True
            }
            
        response = openai.chat.completions.create(**base_params)
            
        accumulated_chunk = ""
            
        for message in response:
            #print(message.choices[0].message.content
            content = message.choices[0].delta.content
            if isinstance(content, str):
                accumulated_chunk += content
                # Decide when to yield the accumulated_chunk, for example, whenever a full sentence or a pause is detected.
                if '.' in accumulated_chunk or '!' in accumulated_chunk or '?' in accumulated_chunk or len(accumulated_chunk) > 2:
                    yield accumulated_chunk
                    accumulated_chunk = ""  # Reset the accumulator after yielding
        if accumulated_chunk:  # Yield any remaining text that wasn't yielded in the loop
            yield accumulated_chunk

    except Exception as e:
        return {"error": str(e)}
        