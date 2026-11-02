
import requests

url = "http://127.0.0.1:5000/submit"

samples = {
    "rich_dad": """The book Rich Dad, Poor Dad is the story of Robert Kiyosaki, the man who has two fathers. His "poor" dad is his biological father, and his "rich" dad is the father of his childhood friend, Mike. Both fathers educated Robert on their views of finance and success, but he clearly knew which one to follow. His rich dad educated him on the ideals of finance as he was growing up, such as the ideas of working for learning and not for money, the importance of financial literacy, and how the poor and middle class are in an endless rat race of working just to get rich. On the other hand, the poor dad is a highly educated man who educates his son on the importance of going to school, getting a degree, and eventually getting a high-paying job. In the end, Robert incorporates the advice of his rich dad in order to gain financial success.""",

    "ai_geology": """Uniformitarianism is an important principle in geology because it helps explain how landscapes and rock formations develop over long periods of time. During the field trip, Manhattan Schist provided an example of how geological processes can shape the materials found in a particular region. Glaciers are especially significant because they can transport rocks and sediment away from their original locations. By examining rock samples, consulting geological maps, and observing the surrounding landscape, we can make informed interpretations about where different rocks originated. These observations help connect present-day evidence with the geological processes that occurred throughout Earth's history.""",
    "edited_ai_geology": """Uniformitarianism is an important principle in geology because it helps explain how landscapes and rock formations develop over extended periods of time. During the field trip, Manhattan Schist gives an example of how geological processes can shape the materials found in a particular region. Glaciers are especially significant because they can transport rocks and sediment away from their original locations. By examining rock samples, consulting geological maps, and observing the surrounding landscape, we can make informed interpretations about where different rocks originated. These observations help connect present-day evidence with the geological processes that occurred throughout Earth's history."""
}

for name, sample_text in samples.items():
    response = requests.post(
        url,
        json={
            "text": sample_text,
            "creator_id": "debug-check"
        }
    )

    print(f"\n{name}")
    print("HTTP status:", response.status_code)
    print(response.json())
