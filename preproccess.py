import re
def preprocess_to_table(ocr_text):
    lines = ocr_text.split("\n")
    processed_lines = []
    
    # Define headers based on common keywords
    header_keywords = ["ITEM", "DESCRIPTION", "QUANTITY", "PRICE", "AMOUNT", "TAX"]
    header_line = None

    # Identify and normalize the header row
    for line in lines:
        if any(keyword in line.upper() for keyword in header_keywords):
            # Normalize header with consistent spacing
            header_line = re.sub(r"\s{2,}", " ", line.strip())
            processed_lines.append(header_line)
            break

    # Process data rows
    for line in lines:
        if line.strip() == header_line or not line.strip():
            continue  # Skip the header or empty lines
        # Normalize spacing in data rows
        normalized_line = re.sub(r"\s{2,}", " ", line.strip())
        processed_lines.append(normalized_line)

    # Join lines with newlines to recreate a tabular structure
    return "\n".join(processed_lines)

# Example OCR text
ocr_text = """
ITEMS DESCRIPTION QUANTITY PRICE TAX AMOUNT
item1 Description 1  $0000 0% 56
item1 Description 2  $0000 0% 45
item1 Description 3  $0000 0% 69
item1 Description 4  $0000 0% 4 
item1 Description 5  $0000 0% 25
item1 Description 6  $0000 0% 61
"""

# Preprocess the text
preprocessed_text = preprocess_to_table(ocr_text)
print("Preprocessed Text:")
print(preprocessed_text)
