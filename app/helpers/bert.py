import requests
from bs4 import BeautifulSoup
from bert_score import score

def candidate_text(final_response: dict, selected_platform: str) -> str:
    """This function extracts text from the final response dictionary based on the selected sections."""

    if selected_platform.lower() == 'facebook':
        text = ""
        for i in range(len(final_response['output'])):
            text += final_response['output'][i]['shortForm']['body'] + " " + \
                    final_response['output'][i]['longForm']['body']

    elif selected_platform.lower() == 'email':
        text = ""
        for i in range(len(final_response["generatedModuleContent"])):
            text += final_response['generatedModuleContent'][i]['body'][20:]
    else:
        text = ""
        for i in range(len(final_response['output'])):
            for j in range(len(final_response['output'][0]['frames'])):
                text += final_response['output'][i]['frames'][j]['body']

    return text





def html_to_readable_text(url) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}

    # Make a GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # Fix: pass response.text, not the response object itself
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Extract text with newlines
    text = soup.get_text(separator="\n")

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [line for line in lines if line]
    return "\n".join(non_empty_lines)



def calculate_bert_score(final_response_dict: dict, url: str,selected_platform) -> None:
    """This function calculates the BERT score for the generated text against the reference text."""

    # Convert the final response dictionary to a string
    string_content = html_to_readable_text(url)

    # Generate candidate text from the final response dictionary
    output_text = candidate_text(final_response_dict, selected_platform)

    candidates = [output_text]  # What the model generated
    references = [string_content]

    P, R, F1 = score(candidates, references, lang="en", verbose=True)
    return {
        "precision": round(P.mean().item(), 4),
        "recall": round(R.mean().item(), 4),
        "f1": round(F1.mean().item(), 4)
    }

