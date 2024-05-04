from dotenv import load_dotenv
from functions.nk_landscape import Landscape
import time
from functions.helper import extract_binaries, bitstring_to_int, hamming_distance
import numpy as np
import csv
encoding = 'utf-8'

load_dotenv()

N=10
K=3
T=25
i=1
max_retries=3

model="gpt-4-turbo-preview"


if model in ["gpt-4-turbo-preview", "gpt-3.5-turbo-0125"]:
    from openai_function.chatGPT import chatGPT as client
    print('loaded openai')
elif model in ["claude-3-sonnet-20240229", "claude-3-opus-20240229", "claude-3-haiku-20240307"]:
    from anthropic_function.claude_with_tools import claude as client
    print('loaded anthropic')



#======================================================
#Prompt Templates

generate_strategy = """Before we start, use a step by step approach to develop a strategy for this task. 
What are important information to explore in your testing strategy. How will these information be used to adapt your strategy as you test. 
Be concise and summarize your step by step strategy in concrete action items."""

instruct=""""""
#strategy = client(prompt=generate_strategy, system_prompt=system)



# Open the CSV file in write mode
with open(f"output/{model}_output.csv", 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(['model', 't', 'reward', 'tested', 'global_peak_performance', 'local_peak', 'distance', 'iteration_id', 'think'])

    
    # Run the code i times
    for iteration_id in range(i):
        print(f"Iteration: {iteration_id}")
        retry_count=0
        perf, pos = None, None
        tested = []
        reward = []
        history = []
        distance = []
        think = []
        local_peak = []
        


        #======================================================
        # Landscape calculations
        example_position = np.random.choice([0, 1], size=N)
        example_position = ''.join(map(str, example_position))
        
        landscape = Landscape(N, K)
        peak_indices = np.where(landscape.local_peak)[0]
        global_peak_performance = landscape.global_peak
        #======================================================

        system = f"""You are tasked with the following problem: 
            There are {N} elements in a product.
            Each element can be configured in two distinct ways, namely 0 or 1.
            Each element contributes to the product's overall performance in equal in weight.
            The actual contribution value of a particular element depends on its own state and an 
            unknonw number of other element states.
            You have no other information about the product. All you know 
            is that if you can test a particular combination of elements and measure a reliable performance feedback from the test.
            This feedback is accurate and will not change over time.
            Each 'round', you can test one combination of the {N} elements. There are in total {T} rounds. 
            After those {T} rounds, you are asked to determine your final combination for production. No other information will be available.
            Important: Each round you must submit the exact specifications of all ten elements explicitely.
            \nClearly state the configuration you choose by stating 'CHOICE=[] with the ten element configurations in square brackets (e.g., CHOICE=[{example_position}]\n
            I ask you to think aloud as you work through your answer. Let me explain what I mean by “think aloud.” It means that I would like you to tell me
            everything you think about as you work through your answer. When I say tell me everything, I really mean every thought you have between reading the latest user input to your CHOICE. NEVER WORRY about **how** to say things. NEVER CLARIFY OR JUSTIFY. I DO NOT CARE whether your answer makes sense to me or not. I ONLY want to see every thought you have and the final CHOICE. My intention is not to evaluate your thinking or understand you decision. The purpose
            of this is to learn about the thoughts as you answer. Nothing else!"""

      
        for t in range(T):
            print(f"Round: {t}")
            
            if t == 0:
                prompt = f"Round 1: What is the first position you want to test?{instruct}."
            elif t in range(1,T-1):
                prompt = f"Round {t+1}: The performance of your tested position ({pos}) is {round(1000*perf)}.\nDefine the next position you intend to test.{instruct}"
            else:
                prompt = f"Round {t+1}: The performance of your tested position ({pos}) is {round(1000*perf)}.\nDefine your final position.{instruct}"
            
            while True:
                try:
                    response = client(prompt=prompt,model=model, system_prompt=system, conversation_history=history if t > 0 else [])
                    pos = extract_binaries(response['text'])
                    int_pos = bitstring_to_int(pos)
                    retry_count = 0  # Reset the retry count on successful extraction
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count <= max_retries:
                        print(f"Error extracting position: {str(e)}. Retrying ({retry_count}/{max_retries})...")
                        continue
                    else:
                        time.sleep(3)
                        print(f"Error extracting position: {str(e)}. Maximum retries exceeded. Terminating.")
                        raise

                        
            history.append({'role': "user", 'content': prompt})
            
            
            
            tested.append(int_pos)
            perf = landscape.performance[int_pos]
            reward.append(perf)
            think.append(response['text'])
            local_peak.append(1 if int_pos in peak_indices else 0)
            
            if t == 0:
                distance.append(0)
            else:
                distance.append(hamming_distance(N, tested[-2],tested[-1]))
            
            history.append({'role': "assistant", 'content': response['text']})
             # Write the data for each round to the CSV file
            writer.writerow([model, t, reward[-1], tested[-1], global_peak_performance, local_peak[-1], distance[-1], iteration_id, think[-1]])

    
    # Optionally, you can write other data or perform additional tasks after each iteration
    # For example, you can write the final reward and tested values for each iteration
    #writer.writerow([f"Final (Iteration {iter_number})", reward[-1], tested[-1], iter_number])



# =============================================================================
#print(history)
#print(tested)
#print(reward)
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
