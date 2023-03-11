from bs4 import BeautifulSoup

def html_to_structured_text(html_string):
    # Create a BeautifulSoup object from the HTML string
    soup = BeautifulSoup(html_string, 'html.parser')

    # Extract the text and create a structured text string
    structured_text = ''
    for tag in soup.find_all():
        tag_name = tag.name
        if tag_name == 'p':
            structured_text += f'\n\n{tag.text}\n\n'
        elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            structured_text += f'\n\n{tag.text}\n{"=" * len(tag.text)}\n\n'
        elif tag_name == 'ul':
            for li in tag.find_all('li'):
                structured_text += f'* {li.text}\n'
        elif tag_name == 'ol':
            for li in tag.find_all('li'):
                index = li.find_previous_siblings('li')
                index = str(len(index) + 1)
                structured_text += f'{index}. {li.text}\n'

    if structured_text == '':
        return html_string
        
    return structured_text