from dotenv import load_dotenv
from functions.nk_landscape import Landscape
from openai_function.chatGPT import chatGPT as client
from openai_function.tools import binary_retrieve
from anthropic_function.tools import construct_tool_use_system_prompt, tool, extract_element_values_concatenated
from anthropic_function.claude_with_tools import claude

load_dotenv()

N=10
K=3

reward=[]
tested=[]
history=[]

def extract_strategy_from_response(response):
    """
    Extracts the binary strategy string from the tool function call response.

    Parameters:
    - response (dict): The JSON response object from the tool function call.

    Returns:
    - str: The extracted binary strategy string.
    """
    # Navigate through the 'function_calls' list and then to 'arguments' if they exist
    if 'function_calls' in response and response['function_calls']:
        # Assuming the first function call contains the desired strategy
        arguments = response['function_calls'][0]['arguments']
        # Construct the strategy string from the binary values of each element
        strategy_string = ''.join(str(arguments[f'e{i}']) for i in range(1, 11))
        return strategy_string
    else:
        raise ValueError("The response format is unexpected or does not contain 'function_calls'.")



def bitstring_to_int(bitstring):
    """Converts a bit string to the respective integer."""
    return int(bitstring, 2)

def int_to_bitstring(integer, N):
    """Converts an integer to a N-bit string, padded with zeros if necessary."""
    return format(integer, '0{}b'.format(N))


landscape = Landscape(N, K)

system = f"""You are tasked with the following problem: 
    There are {N} elements in a product.
    Each element can be configured in two distinct ways, namely 0 or 1.
    Each element contributes to the product's performance.
    The contribution value of the element depends on its own state and an ex-ante 
    unknonw number of other other elements' states.
    You have no information about the product or how performance is defined. All you know 
    is that if you can test a particular combination and retrieve a reliable performance feedback from the test.
    This feedback is accurate and will not change over time. You can trust it.
    Each 'round', you can test one combination of all 10 elements. There are in total 25 rounds. 
    After those 25 rounds, you are asked to determine your final combination for production. No other information will be available.
    Important: Each round you must submit the specifications of all ten elements explicitely."""

generate_strategy = """ """

instruct=""


first_position = f"Round 1: What is the first position you want to test?{instruct}."

force = {"type": "function", "function": {"name": "define_element_combination"}}

#Anthropic Specs
system_prompt = construct_tool_use_system_prompt([tool], system)


llm="openai"


for t in range(25):
    if t==0:
        print(f"Round: {t}")
        
        if llm=="openai":
            ##############
            #OpenAI
            response = client(prompt = first_position, system_prompt=system, tools=binary_retrieve, force=force)
            print(response)
            pos = extract_strategy_from_response(response)
            int_pos = bitstring_to_int(pos)
            tested.append(int_pos)
            perf=landscape.performance[int_pos]
            reward.append(perf)
            combined_response = response['function_calls'][0]['arguments']['Reasoning'] + " The position to test: " +pos
            history.append({'role': "assistant", 'content': combined_response})
        elif llm=="anthropic":
            ##############
            #Anthropic
            response = claude(prompt = first_position, system_prompt=system_prompt)
            pos = extract_element_values_concatenated(response['function_calls'])
            int_pos = bitstring_to_int(pos)
            tested.append(int_pos)
            perf=landscape.performance[int_pos]
            reward.append(perf)
            combined_response = response['text'] + " The position to test: " + pos
            history.append({'role': "assistant", 'content': combined_response})
        elif llm=="google":
            print("tbd")
            ##############
            #Google
            ##############
        else:
            print("No valid LLM specified.")
        
        
        
    else:
        print(f"Round: {t}")
        if llm=="openai":
            ##############
            #OpenAI
            next_position = f"Round {t+1}: The performance of your tested position ({pos}) is {perf}.\nDefine the next position you intend to test.{instruct}"    
            response = client(prompt = next_position, system_prompt=system, tools=binary_retrieve, conversation_history=history, force=force)
            print(response)
            history.append({'role': "user", 'content': next_position})
            pos = extract_strategy_from_response(response)
            int_pos = bitstring_to_int(pos)
            tested.append(int_pos)
            perf=landscape.performance[int_pos]
            reward.append(perf)
            reasoning_exists = response.get('function_calls', [{}])[0].get('arguments', {}).get('Reasoning', None) is not None
            if reasoning_exists:
                combined_response =  response['function_calls'][0]['arguments']['Reasoning'] + " The position to test: " + pos 
            else:
                combined_response = "The position to test: " + pos
            history.append({'role': "assistant", 'content': combined_response})
        elif llm=="anthropic":
            ##############
            #Anthropic
            next_position = f"Round {t+1}: The performance of your tested position ({pos}) is {perf}.\nExplain what position you want to test and why.{instruct}"    
            response = claude(prompt = next_position, system_prompt=system_prompt)
            history.append({'role': "user", 'content': next_position})
            pos = extract_element_values_concatenated(response['function_calls'])
            int_pos = bitstring_to_int(pos)
            tested.append(int_pos)
            perf=landscape.performance[int_pos]
            reward.append(perf)
            combined_response = response['text'] + " The position to test: " + pos
            history.append({'role': "assistant", 'content': combined_response})
        elif llm=="google":
            print("tbd")
        
        else:
            print("No valid LLM specified.")

# =============================================================================
print(history)
print(tested)
print(reward)
# 
# system_prompt = construct_tool_use_system_prompt([tool], system)
# response = claude(prompt = first_position, system_prompt=system_prompt)
# print(response)
# 
# 
# 
# extract_element_values_concatenated(response['function_calls'])
# 
# 
# =============================================================================
