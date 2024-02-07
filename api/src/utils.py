import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseHandler():
    def __init__(self) -> None:
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)


    def readPostgreSQL(self):
        try:
            # Connect to your Supabase database
            response = self.client.table('Images').select("*").execute()
            print(response)
        except Exception as e:
            print(f"An error occurred: {e}")
        return response


    def uploadImage(self, file, bucket, path_on_supastorage, content_type="image/jpeg"):
        self.client.storage.from_(bucket).upload(file=file, path=path_on_supastorage, file_options={"content-type": f"{content_type}" })
        print("Image uploaded")


    def createDatabaseEntryImage(self, table, user_id):
        data, count = self.client.table(table).insert({"user_id": user_id}).execute()
        return data, count
