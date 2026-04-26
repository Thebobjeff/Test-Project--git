import os
import csv
import lyricsgenius
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# 1. Setup Environment
load_dotenv()
token = os.getenv("client_access_token")

# Initialize Genius with optimized settings
genius = lyricsgenius.Genius(token)
genius.verbose = False
genius.remove_section_headers = True
genius.skip_non_songs = True  # Prevents downloading tracklists or liner notes

input_file = 'hooks/test.csv'
output_file = 'hooks/updateTestFile1.csv'

def fetch_lyrics_task(row):
    """
    Worker function to process a single row.
    Accesses columns by name based on your CSV header.
    """
    artist = row['Artist']
    song_title = row['Song']

    # Clean up song titles that have movie info like (From "Young Guns II")
    # This helps Genius find the song more accurately
    clean_song = song_title.split(' (From ')[0]

    # FIX 1: Define defaults BEFORE the try block so they always exist,
    # even if an exception is thrown and we jump straight to except.
    lyrics = "Lyrics Not Found"
    tags = "Unknown"

    try:
        # Searching by (song, artist) is faster and more accurate than a single string
        result = genius.search_song(clean_song, artist)
        if result:
            lyrics = result.lyrics
            # Pull genre tags from the raw Genius API response body
            raw_tags = result._body.get("tags", [])
            tags = ", ".join(t.get("name", "") for t in raw_tags) if raw_tags else "Unknown"
    except Exception as e:
        lyrics = "Song Not Found"
        tags = "Unknown"

    # Replace newlines with a pipe — always safe now since lyrics has a default
    clean_lyrics = lyrics.replace("\n", " | ")

    # Return the original row data plus the two new columns
    return {**row, 'Lyrics': clean_lyrics, 'Tags': tags}

def main():
    # 1. Read the file using DictReader
    # DictReader AUTOMATICALLY skips the header and uses it for keys
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # FIX 2: Add 'Tags' to fieldnames so the DictWriter knows about it
        fieldnames = reader.fieldnames + ['Lyrics', 'Tags']

        # Convert to a list so ThreadPoolExecutor can process it
        rows = list(reader)

    print(f"Starting lyrics fetch for {len(rows)} songs...")

    # 2. Process in parallel
    with ThreadPoolExecutor(max_workers=8) as executor:
        final_results = list(executor.map(fetch_lyrics_task, rows))

    # 3. Write results
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_results)

    print(f"Successfully created: {output_file}")

if __name__ == "__main__":
    main()

