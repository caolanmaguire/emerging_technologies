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
    
    def clean_text(work):
        """
        Removes the preamble and postamble from the text,
        removes unwanted characters, makes all letters uppercase,
        and removes specific words from the cleaned text.

        Args:
            work (str): The full text of the book.
            forbidden_words (list): A list of words that will be removed from the text.

        Returns:
            str: The cleaned and transformed text with forbidden words removed.
        """
        # 1. Remove the preamble and postamble using regex
        start_marker = r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK .*? \*\*\*"
        end_marker = r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK .*? \*\*\*"

        # Find the start and end of the main content
        start_match = re.search(start_marker, work, re.IGNORECASE)
        end_match = re.search(end_marker, work, re.IGNORECASE)

        if not start_match or not end_match:
            print("Markers not found. Returning full text.")
            return work.strip()

        # Extract the main content between the start and end markers
        start_index = start_match.end()
        end_index = end_match.start()

        work = work[start_index:end_index].strip()

        # 2. Remove all characters except ASCII letters (uppercase and lowercase), full stops, and spaces
        cleaned_work = re.sub(r'[^A-Za-z. ]', '', work)

        # 3. Convert all letters to uppercase
        cleaned_work = cleaned_work.upper()

        forbidden_words = ['chapters','chapter']

        # 4. Remove forbidden words from the cleaned text
        for word in forbidden_words:
            # Use regex to remove the word and any surrounding spaces
            cleaned_work = re.sub(r'\b' + re.escape(word.upper()) + r'\b', '', cleaned_work)

        # 5. Return the cleaned text
        return cleaned_work.strip()


    # Run all tasks
    selected_works = select_random_gutenberg_works()

    for idx, (title, work) in enumerate(selected_works, 1):
        cleaned_work = clean_text(work)
        print(f"{idx}. {title}")
        print("First 500 characters:")
        print(cleaned_work[:500])  # Print the first 500 characters of the cleaned work
        print('\n\n')
        print("Last 500 characters:")
        print(cleaned_work[-500:])  # Print the last 500 characters of the cleaned work
        print("\n" + "-"*40)  # Separator between works

task_one()
