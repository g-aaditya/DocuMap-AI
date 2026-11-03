def extract_clean_text(soup):
    for tag in soup(["script","style","nav","footer","header","aside"]):
        tag.decompose()
    blocks=[]
    for tag in soup.find_all(["h1","h2","h3","p","li"]):
        text=tag.get_text(strip=True)
        if len(text)>30:
            blocks.append(text)
    return "\n".join(blocks)
