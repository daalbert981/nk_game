binary_retrieve = [{
    "type": "function",
    "function": {
        "name": "define_element_combination",
        "description": "Define integers of **all** elements for next test",
        "parameters": {
            "type": "object",
            "properties": {
                "Reasoning": {
                    "type": "string",
                    "description": "Explain your reasoning for your next test.",
                    },
                "e1": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 1",
                },
                "e2": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 2",
                },
                "e3": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 3",
                },
                "e4": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 4",
                },
                "e5": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 5",
                },
                "e6": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 6",
                },
                "e7": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 7",
                },
                "e8": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 8",
                },
                "e9": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 9",
                },
                "e10": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "Confirm state for element 10",
            },
            
        },
    },
        "required": ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10","Reasoning"]
}
}]
    