import requests, random, re

def task_one():

    def select_random_gutenberg_works():
        """
        Fetches the list of top 100 eBooks from Project Gutenberg,
        parses the links manually without external libraries, and selects five works randomly.

        Returns:
            list: A list of tuples with eBook titles and their download URLs in Plain Text UTF-8 format.
        """
        url = "https://www.gutenberg.org/browse/scores/top"

        try:
            # Fetch the top 100 eBooks page
            response = requests.get(url)
            response.raise_for_status()

            # Extract links to eBook pages manually using regex
            page_content = response.text
            ebook_links = re.findall(r'href="(/ebooks/\d+)"', page_content)
            # print(page_content)
            ebook_links = [f"https://www.gutenberg.org{link}" for link in ebook_links]

            if len(ebook_links) < 5:
                print("Not enough eBooks found.")
                return []

            # Randomly select 5 eBook pages
            selected_pages = random.sample(ebook_links, 5)
            ebooks_with_text_links = []

            for page_url in selected_pages:
                try:
                    # Fetch each eBook page
                    page_response = requests.get(page_url)
                    page_response.raise_for_status()

                    # Extract the Plain Text UTF-8 link manually
                    text_match = re.search(r'href="(.*?\.txt\.utf-8)"', page_response.text)
                    title_match = re.search(r'<title>(.*?)\| Project Gutenberg</title>', page_response.text)

                    if text_match and title_match:
                        full_text_url = f"https://www.gutenberg.org{text_match.group(1)}"

                        actual_book_data = requests.get(full_text_url).text

                        title = title_match.group(1).strip()
                        ebooks_with_text_links.append((title, actual_book_data))

                except requests.RequestException as e:
                    print(f"Error fetching eBook page {page_url}: {e}")

            if len(ebooks_with_text_links) < 5:
                print("Not enough eBooks with Plain Text UTF-8 format found.")
                return []

            return ebooks_with_text_links

        except requests.RequestException as e:
            print(f"Error fetching data from Project Gutenberg: {e}")
            return []
    
    def clean_text(title,work):
        cleaned_text = ''
        print(f"{title}. {work}")
        return cleaned_text

    # run all tasks
    selected_works = select_random_gutenberg_works()
    # print(selected_works)
    for idx, (title, url) in enumerate(selected_works, 1):
        clean_text(title,url)
        # print(f"{idx}. {title}")#: {url}")


task_one()        