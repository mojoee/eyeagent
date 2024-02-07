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
        return data, count
    

    def updateImagePath(self):
        data, count = self.client.table("Images").select('*').eq('file_name', "").execute()
        for row in data[1]:
            self.client.table("Images").update({"file_name": f"{row['user_id']}/{str(row['id'])}.jpg"}).eq('id', row['id']).execute()
        return data, count


    def getFileName(self, id):
        data, count = self.client.table("Images").select("*").eq('id', id).execute()
        return data[1][0]["user_id"]+"/"+str(id)+".jpg"

if __name__ == "__main__":
    dbHandler = DatabaseHandler()
    test_user = 'd7d51b5d-3c77-436d-910c-972b59567d21'
    #dbHandler.createDatabaseEntryImage(test_user)
    #dbHandler.updateImagePath()
    dbHandler.getFileName(39)
    print("Done!")