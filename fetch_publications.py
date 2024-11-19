from scholarly import scholarly
import json

def fetch_publications(author_name, output_file="publications.json",max_authors=3):
    try:
        # Search for the author by name
        search_query = scholarly.search_author(author_name)
        author = next(search_query)  # Get the first result
        scholarly.fill(author)  # Fetch detailed information

        print(f"Fetching publications for: {author['name']}")

        # Lists to store journal and conference papers
        journal_papers = []
        conference_papers = []
        
        for pub in author.get('publications', []):
            scholarly.fill(pub)  # Fetch detailed publication info




            # Get DOI link if available, fallback to pub_url
            doi = pub.get("eprint_url", None)  # DOI is often in eprint_url
            link = doi if doi else pub.get("pub_url", "#")

            # Parse authors and ensure 'author_name' is included
            raw_authors = pub.get("bib", {}).get("author", "Unknown Authors").split("and")
            authors = raw_authors[:max_authors]  # Limit number of authors
            if len(raw_authors) > max_authors:
                authors[-1] = "et al."  # Indicate more authors
            if author_name not in authors:
                authors[0]=author_name  # Ensure your name is included
            # Check if it's a journal or conference paper
            bib = pub.get("bib", {})
            venue_type = "Unknown Venue"
            if "journal" in bib:  # It's a journal paper
                venue_type = bib.get("journal", "Unknown Journal")
                journal_papers.append({
                    "title": bib.get("title", "Unknown Title"),
                    "authors": ", ".join(authors),
                    "year": bib.get("pub_year", "Unknown Year"),
                    "venue": venue_type,
                    "link": link
                })
            elif "conference" in bib:  # It's a conference paper
                venue_type = bib.get("conference", "Unknown Conference")
                conference_papers.append({
                    "title": bib.get("title", "Unknown Title"),
                    "authors": ", ".join(authors),
                    "year": bib.get("pub_year", "Unknown Year"),
                    "venue": venue_type,
                    "link": link
                })

        # Combine and save to JSON
        result = {
            "journal_papers": journal_papers,
            "conference_papers": conference_papers
        }
        with open(output_file, "w") as f:
            json.dump(result, f, indent=4)

        print(f"Publications saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'Your Name' with the name used in your Google Scholar profile
fetch_publications("Leshan Zhao")
