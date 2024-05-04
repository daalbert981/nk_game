import re

def extract_binaries(text):
    # First, find all sequences of 10 consecutive 0s and 1s in the text
    binaries = re.findall(r'\b[01]{10}\b', text)
    
    # If more than one binary sequence is found, look for one following 'NEXT=['
    if len(binaries) > 1:
        next_pattern = r'CHOICE=\[([01]{10})\]'
        next_match = re.search(next_pattern, text)
        if next_match:
            return next_match.group(1)  # Return the specific sequence after 'NEXT=['
    
    return binaries[0]


def bitstring_to_int(bitstring):
    """Converts a bit string to the respective integer."""
    return int(bitstring, 2)

def int_to_bitstring(integer, N):
    """Converts an integer to a N-bit string, padded with zeros if necessary."""
    return format(integer, '0{}b'.format(N))


def hamming_distance(N, num1, num2):
    # Convert the integers to binary strings of length N
    bin1 = format(num1, f'0{N}b')
    bin2 = format(num2, f'0{N}b')
    
    # Initialize the Hamming distance to 0
    distance = 0
    
    # Compare each bit position
    for bit1, bit2 in zip(bin1, bin2):
        if bit1 != bit2:
            distance += 1
    
    return distance