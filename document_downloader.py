import requests

def download_pdf(url):
    response = requests.get(url, allow_redirects=True)

    with open("resumes/resume.pdf",'wb') as f:
        f.write(response.content)