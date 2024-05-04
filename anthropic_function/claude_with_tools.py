import anthropic
from bs4 import BeautifulSoup

client = anthropic.Anthropic()
# Models: claude-3-sonnet-20240229 claude-3-opus-20240229
# =============================================================================
def extract_with_beautifulsoup(string: str) -> str:
    soup = BeautifulSoup(string, 'html.parser')
    function_calls = soup.find_all('function_calls')
    content = "".join([str(element) for element in function_calls])
    return content

def claude(prompt,
           model="claude-3-opus-20240229",
           temperature=0.7,
           max_tokens=4096,
           top_p=1,
           system_prompt="",
           conversation_history=[],
           stop_sequences=["\n\nHuman:", "\n\nAssistant", "</function_calls>"]):
    try:
        message_sequence = [{"role": "user", "content": prompt}]
        if conversation_history:
            message_sequence = conversation_history + [{"role": "user", "content": prompt}]

        base_params = {
            "model": model,
            "messages": message_sequence,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "system": system_prompt,
            "stop_sequences": stop_sequences
        }
        
        response = client.messages.create(**base_params)
        
        structured_response = {
            "text": "",
            "function_calls": ""
        }

        if response.content:
            content_block = response.content[0]
            if content_block.text:
                # Use BeautifulSoup to extract <function_calls> content
                structured_response["function_calls"] = extract_with_beautifulsoup(content_block.text)
                # The text part is everything before <function_calls>
                structured_response["text"] = content_block.text.split("<function_calls>")[0].strip()

        return structured_response

    except Exception as e:
        return {"error": str(e)}


