from bs4 import BeautifulSoup


def construct_format_tool_for_claude_prompt(name, description, parameters):
    constructed_prompt = (
        "<tool_description>\n"
        f"<tool_name>{name}</tool_name>\n"
        "<description>\n"
        f"{description}\n"
        "</description>\n"
        "<parameters>\n"
        f"{construct_format_parameters_prompt(parameters)}\n"
        "</parameters>\n"
        "</tool_description>"
    )
    return constructed_prompt

tool_name = "define_element_combination"
tool_description = "Define integers of **all** elements for next test"

def construct_format_parameters_prompt(parameters):
    constructed_prompt = "\n".join(f"<parameter>\n<name>{parameter['name']}</name>\n<type>{parameter['type']}</type>\n<description>{parameter['description']}</description>\n</parameter>" for parameter in parameters)
    return constructed_prompt

parameters = [
    {
        "name": "e1",
        "type": "int",
        "description": "Confirm state for element 1 (0 or 1)"
    },
    {
        "name": "e2",
        "type": "int", 
        "description": "Confirm state for element 2 (0 or 1)"
    },
    {
        "name": "e3",
        "type": "int",
        "description": "Confirm state for element 3 (0 or 1)"
    },
    {
        "name": "e4",
        "type": "int",
        "description": "Confirm state for element 4 (0 or 1)"
    },
    {
        "name": "e5",
        "type": "int",
        "description": "Confirm state for element 5 (0 or 1)"
    },
    {
        "name": "e6",
        "type": "int",
        "description": "Confirm state for element 6 (0 or 1)"
    },
    {
        "name": "e7",
        "type": "int",
        "description": "Confirm state for element 7 (0 or 1)"
    },
    {
        "name": "e8",
        "type": "int",
        "description": "Confirm state for element 8 (0 or 1)"
    },
    {
        "name": "e9",
        "type": "int",
        "description": "Confirm state for element 9 (0 or 1)"
    },
    {
        "name": "e10",
        "type": "int",
        "description": "Confirm state for element 10 (0 or 1)"
    },

]

tool = construct_format_tool_for_claude_prompt(tool_name, tool_description, parameters)


def construct_tool_use_system_prompt(tools, general_system_prompt):
    tool_use_system_prompt = (
        f"{general_system_prompt}\n"
        "\n"
        "In addition to the above, you have access to a set of tools you can use to answer the user's question.\n"
        "\n"
        "You may call them like this:\n"
        "<function_calls>\n"
        "<invoke>\n"
        "<tool_name>$TOOL_NAME</tool_name>\n"
        "<parameters>\n"
        "<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>\n"
        "...\n"
        "</parameters>\n"
        "</invoke>\n"
        "</function_calls>\n"
        "\n"
        "Here are the tools available:\n"
        "<tools>\n"
        + '\n'.join([tool for tool in tools]) +
        "\n</tools>"
    )
    return tool_use_system_prompt


def extract_element_values_concatenated(function_calls_content: str) -> str:
    soup = BeautifulSoup(function_calls_content, 'html.parser')
    concatenated_values = ""
    for i in range(1, 11):  # Assuming e1 to e10
        element_tag = f"e{i}"
        element = soup.find(element_tag)
        if element:
            concatenated_values += element.text
        else:
            print("Error in Elements")
    return concatenated_values