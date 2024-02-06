# Imports the Google Cloud client library
from google.cloud import vision
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


def getImageLabels(file_uri = "https://yerngrprgzhttyniubnk.supabase.co/storage/v1/object/sign/images/test/test2.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJpbWFnZXMvdGVzdC90ZXN0Mi5qcGciLCJpYXQiOjE3MDcyMDE5NjAsImV4cCI6MTcwNzgwNjc2MH0.PqzMq7UNg_X8SV0uXHUVBTRitIo4-7gGoQ1H3Kt07Nw&t=2024-02-06T06%3A46%3A01.113Z") -> vision.EntityAnnotation:
    """Provides a quick start example for Cloud Vision."""
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    # The URI of the image file to annotate
    # file_uri = "https://yerngrprgzhttyniubnk.supabase.co/storage/v1/object/sign/images/test1.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJpbWFnZXMvdGVzdDEuanBnIiwiaWF0IjoxNzA3MjAxNjYxLCJleHAiOjE3MDc4MDY0NjF9.nmslMr5a1EZ3Kz9o7zeydzuHnWnBH6aAaFVm_ZCLv44&t=2024-02-06T06%3A41%3A01.953Z"
    image = vision.Image()
    image.source.image_uri = file_uri
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    # response = client.landmarkDetection(image=image)
    labels = response.label_annotations
    print("Labels:")
    for label in labels:
        print(label.description)
    return [label.description for label in labels]


def generate_action_suggestions(items):
    """Generates action suggestions for identified items using OpenAI's GPT."""
    suggestions = {}
    prompt = f""" 
    Please suggest actions for specific items.
    Examples are: 
    item: orange, action: buy it online, know its nutritional value, know its price
    item: book, action: give me a summary, buy it online, who is the author
    item: car, action: know its price, know its fuel efficiency, know its model

    Suggest 3 actions for each of these: {items}. 
    Return the item, followed by the actions.
    """
    try:
        client = OpenAI()

        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"{prompt}"}],
            stream=True,
        )
        #suggestions[item] = stream.choices[0].delta.content
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
    except Exception as e:
        print(f"Error generating suggestion for {items}: {str(e)}")
        suggestions[items] = "No suggestion available."

    return suggestions


if __name__ == "__main__":
    labels = getImageLabels()
    actions = generate_action_suggestions(labels)
    print(actions)
    print("Done!")
