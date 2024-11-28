import re
import json

def extract_items_from_invoice(ocr_text):
    """
    Extracts item details from OCR output of an invoice.

    Args:
        ocr_text (str): The raw OCR output as a string.

    Returns:
        list: A list of dictionaries containing item details.
    """
    items = []

    # Look for lines with item details: dynamic pattern to match descriptions, quantities, prices, and amounts
    # Matches formats like:
    # - Item A Description    2    $300.00    $600.00
    # - Widget                10   $20        $200
    item_lines = re.findall(
        r"(?:(?:Item|tem|ITEM|Code)?\s*\w+.*?)"  # Match item line with a description
        r"(\d+)\s+"                              # Match Quantity
        r"\$?([\d,]+\.\d{2})\s+"                 # Match Unit Price
        r"(?:\$?([\d,]+\.\d{2}))?",              # Match optional Amount or Tax
        ocr_text, re.IGNORECASE
    )

    # Process each matched item line
    for line in item_lines:
        description_match = re.search(r"(?:Item|item|ITEM|ITEMS|Code)?\s*(.*)\s+\d+", line[0], re.IGNORECASE)
        description = description_match.group(1).strip() if description_match else "Unknown Description"

        item = {
            "Description": description,
            "Quantity": line[0].strip(),
            "Unit Price": line[1].strip(),
            "Amount": line[2].strip() if line[2] else "N/A"
        }
        items.append(item)

    return items

def save_items_as_json(items, filename="items_details.json"):
    """
    Saves item details as a JSON file.

    Args:
        items (list): The list of item dictionaries.
        filename (str): The name of the file.
    """
    with open(filename, "w") as json_file:
        json.dump(items, json_file, indent=4)
    print(f"Items saved to {filename}")


# Example OCR Texts for Testing
examples = [
    """
    ITEMS DESCRIPTION QUANTITY PRICE TAX AMOUNT
    item1 Description 1  $0000 0% 56
    item1 Description 2  $0000 0% 45
    item1 Description 3  $0000 0% 69
    item1 Description 4  $0000 0% 4 
    item1 Description 5  $0000 0% 25
    item1 Description 6  $0000 0% 61
    """
]

# Process each example
for i, example in enumerate(examples, 1):
    print(f"\n--- Processing Example {i} ---")
    extracted_items = extract_items_from_invoice(example)
    print(json.dumps(extracted_items, indent=4))

    # Save JSON for each example
    save_items_as_json(extracted_items, filename=f"items_details_example_{i}.json")
