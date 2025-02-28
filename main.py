from bs4 import BeautifulSoup
import json

def get_doc_structure(file_path):
    # Open and read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        # Parse the HTML content
        soup = BeautifulSoup(file, 'html.parser')
        
        # Find the body tag
        body = soup.find('body')
        
        if body:
            # Remove all text content while keeping the structure
            for element in body.find_all(text=True):
                if element.parent.name != 'script' and element.parent.name != 'style':
                    element.replace_with('')
            return str(body.encode_contents())
        else:
            return "Body tag not found"

def scrape_content(file_path):
    # Open and read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        # Parse the HTML content
        soup = BeautifulSoup(file, 'html.parser')
        
        # Find and extract text content from header elements
        date = soup.find('p', class_='oj-hd-date')
        language = soup.find('p', class_='oj-hd-lg')
        title = soup.find('p', class_='oj-hd-ti')
        doc_number = soup.find('p', class_='oj-hd-oj')
        
        # Find the eli-main-title div and get all paragraphs
        eli_main = soup.find('div', class_='eli-main-title')
        paragraphs = []
        if eli_main:
            paragraphs = [p.get_text().strip() for p in eli_main.find_all('p') if p.get_text().strip()]
        
        # Create content dictionary
        content = {
            "date": date.get_text().strip() if date else "",
            "language": language.get_text().strip() if language else "",
            "title": title.get_text().strip() if title else "",
            "document_number": doc_number.get_text().strip() if doc_number else "",
            "paragraphs": paragraphs
        }
        
        return json.dumps(content, indent=4, ensure_ascii=False)

def save_html_content(content, output_file):
    # Create a basic HTML structure
    html_structure = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
{content}
</body>
</html>"""
    
    # Write the content to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_structure)

def save_json_content(content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

# Example usage
if __name__ == "__main__":
    input_file = 'testing.html'  # Replace with your input file path
    
    # Get and save the structure
    html_structure = get_doc_structure(input_file)
    save_html_content(html_structure, 'structure2.html')
    print(f"Structure has been saved to structure.html")
    
    """
    # Get and save the content
    json_content = scrape_content(input_file)
    save_json_content(json_content, 'content.json')
    print(f"Content has been saved to content.json")
    """
