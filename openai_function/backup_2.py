# =============================================================================
# DEFINE chatGPT function
# Author: Daniel Albert, PhD
# 2024
# da692@drexel.edu
# =============================================================================
import openai
import json

def chatGPT(prompt, 
            model="gpt-4-turbo-preview", 
            temperature=0.7, 
            max_tokens=4096, 
            top_p=1, 
            tools=None, 
            system_prompt="",
            conversation_history=[],
            stream=True):
    try:
        # Prepare the base parameters for the API call
        message_sequence = [{"role": "system", "content": system_prompt}] + conversation_history + [
            {"role": "user", "content": prompt}
        ]
        
        # Function to simulate typing effect
        if stream:
            import time
            def typing_effect(text):
                for char in text:
                    print(char, end='', flush=True)
                    time.sleep(0.05)  # Adjust the delay to suit the desired speed

            base_params = {
                "model": model,
                "messages": message_sequence,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": True
            }
            response = openai.chat.completions.create(**base_params)
            
            for chunk in response:
                content = chunk.choices[0].delta.content
                if isinstance(content, str):
                   for char in content:
                       yield char  # Yield each character for SSE
                        
# =============================================================================
#             for chunk in response:
#                content = chunk.choices[0].delta.content
#                # Ensure the chunk is a string.
#                if isinstance(content, str):
#                    # Simulate typing effect for each character.
#                    typing_effect(content)
# =============================================================================
                   
            #for chunk in response:
            #    content = chunk['choices'][0]['message']['content']
            #    if isinstance(content, str):
            #        yield content  # Yield each chunk of content
       
        else:
            

            # Include tools if they are provided (not None)
            if tools is not None:
                base_params["tools"] = tools
                base_params["tool_choice"] = "auto"
            
            base_params = {
                "model": model,
                "messages": message_sequence,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
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