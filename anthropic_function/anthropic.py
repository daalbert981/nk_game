import anthropic

#
client = anthropic.Anthropic()
# =============================================================================
# ChatGPT Non-streaming
# Default suggested
# Models: claude-3-sonnet-20240229 claude-3-opus-20240229
# =============================================================================
def claude(prompt, 
            model="claude-3-sonnet-20240229", 
            temperature=0.7, 
            max_tokens=4096, 
            top_p=1, 
            tools=None, 
            system_prompt="",
            conversation_history=[]):
        # Prepare the base parameters for the API call
    try:
        
        
        message_sequence = [{"role": "user", "content": prompt}
        ]
        
        if conversation_history:
           message_sequence = [conversation_history + {"role": "user", "content": prompt}
           ]
        
        
        # Function to simulate typing effect
        

        base_params = {
                "model": model,
                "system": system_prompt,
                "messages": message_sequence,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
        
            # Include tools if they are provided (not None)
        if tools is not None:
            base_params["tools"] = tools
            base_params["tool_choice"] = "auto"


        
            
        response = client.messages.create(**base_params)

        
            # Initialize a dictionary to structure the response
        structured_response = {
                "text": "",
                "function_calls": []
            }
    
            # Check for general message content
        if response.content[0].text:
            structured_response["text"] = response.content[0].text
    
        
    
        return structured_response
    except Exception as e:
        return {"error": str(e)} 
    
    
