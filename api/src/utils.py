import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def getClient():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase

def readPostgreSQL():
    supabase = getClient()

    try:
        # Connect to your Supabase database
        response = supabase.table('Images').select("*").execute()
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")
    return response


def uploadImage(file, bucket, path_on_supastorage, content_type="image/jpeg"):
    supabase = getClient()
    supabase.storage.from_(bucket).upload(file=file, path=path_on_supastorage, file_options={"content-type": f"{content_type}" })
    print("Image uploaded")


