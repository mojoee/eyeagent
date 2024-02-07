import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseHandler():
    def __init__(self) -> None:
        super().__init__()
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
        self.client.storage.from_(bucket).upload(file=file, path=path_on_supastorage, file_options={"content-type": f"{content_type}"})
        print("Image uploaded")


    def createDatabaseEntryImage(self, user_id):
        data, count = self.client.table("Images").insert({"user_id": user_id}).execute()
        id = data[1][0]["id"]
        fileName = user_id + "/" + str(id)
        data[1][0]["file_name"] = fileName
        _, _ = self.client.table("Images").update({"file_name": fileName}).eq('id', id).execute()
        return data, count


if __name__=="__main__":
    dbHandler = DatabaseHandler()
    test_user = 'd7d51b5d-3c77-436d-910c-972b59567d21'
    dbHandler.createDatabaseEntryImage(test_user)
    print("Done!")