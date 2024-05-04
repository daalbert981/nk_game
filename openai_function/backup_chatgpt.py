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
            "top_p": top_p
        }

        # Include tools if they are provided (not None)
        if tools is not None:
            base_params["tools"] = tools
            base_params["tool_choice"] = "auto"

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

