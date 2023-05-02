import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk

def analyze_url():
    url = url_entry.get()

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.title.string if soup.title else "N/A"

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_tag["content"] if meta_tag else "N/A"

    headings = [heading.text.strip() for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    headings = headings if headings else "N/A"

    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            if href.startswith("http"):
                links.append(href)
            else:
                links.append(url + href)

    links = links if links else "N/A"

    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    keywords = keywords_tag["content"] if keywords_tag else "N/A"

    author_tag = soup.find("meta", attrs={"name": "author"})
    author = author_tag["content"] if author_tag else "N/A"

    pub_date_tag = soup.find("meta", attrs={"name": "pubdate"})
    pub_date = pub_date_tag["content"] if pub_date_tag else "N/A"

    social_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            if "facebook" in href or "twitter" in href or "linkedin" in href or "instagram" in href:
                social_links.append(href)

    social_links = social_links if social_links else "N/A"

    contact_tag = soup.find("section", {"class": "contact-info"})
    contact_info = contact_tag.text.strip() if contact_tag else "N/A"

    data = {
        "Output Description": ["Page Title", "Meta Description", "Headings", "Links", "Keywords", "Author Information",
                                "Publication Date", "Social Media Links", "Contact Information"],
        "Data": [title, meta_desc, headings, links, keywords, author, pub_date, social_links, contact_info],
        "Status": ["Available" if x != "N/A" else "Not Available" for x in [title, meta_desc, headings, links, keywords, author, pub_date, social_links, contact_info]]
    }

    df = pd.DataFrame(data)
    output_table["column"] = list(df.columns)
    output_table["show"] = "headings"
    for column in output_table["columns"]:
        output_table.heading(column, text=column)
    output_table.delete(*output_table.get_children())
    for i, row in df.iterrows():
        output_table.insert("", "end", text=str(i), values=list(row))

window = tk.Tk()
window.title("Homepage Analyzer")

url_label = tk.Label(window, text="Enter URL:")
url_label.grid(column=0, row=0)

url_entry = tk.Entry(window)
url_entry.grid(column=1, row=0)

analyze_button = tk.Button(window, text="Analyze", command=analyze_url)
analyze_button.grid(column=2, row=0)

output_table = ttk.Treeview(window)
output_table.grid(column=0, row=1, columnspan=3)

window.mainloop()
