import billboard
# billboard is a Python library that allows you to fetch and analyze music chart data from Billboard. It provides an easy way to access various charts, such as the Hot 100, Billboard 200, and many genre-specific charts. You can use it to retrieve information about songs, artists, and their rankings on the charts.

#  AI WAY copy and paste from the billboard gemini code example
# import billboard

# Using 'date' instead of 'year' avoids the Year-End scraper bug.
# This pulls the chart from the end of 2006.
# import billboard

# 1. Use the exact lowercase slug
# 2. Use 'date' instead of 'year' to avoid the library's scraping bug
chat_info = [
    ['Hip-Hop / R&B', 'hot-r-b-hip-hop-songs'],
    ['Rap', 'hot-rap-songs'],
    ['Rock & Alternative', 'hot-rock-songs'],
    ['Country', 'hot-country-songs'],
    ['Dance / Electronic', 'hot-dance-electronic-songs'],
    ['Latin', 'hot-latin-songs'],
    ['Pop', 'pop-songs'],
    ['Afrobeats', 'afrobeats-songs'],
] # chart names
 
target_date = '2006-12-30' 
 
for title, chart_name in chat_info:
    print(f"Title: {title}, Chart Name: {chart_name}")
    try:
        chart = billboard.ChartData(chart_name, date=target_date)
        print(f"Successfully fetched: {chart.title}")
    
        # Print the top 10 songs/artists
        for i, entry in enumerate(chart[:10], 1):
            print(f"{i}. Artist Name: {entry.artist} - Song Name: {entry.title} - Chart: {title}")
        
    except Exception as e:
        print(f"Error: {e}")

 