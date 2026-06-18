from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

class SupabaseClient:
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.client: Client = create_client(self.url, self.key)

    def get_client(self) -> Client:
        return self.client

    def insert_data(self, table: str, data: dict):
        return self.client.table(table).insert(data).execute()

    def query_data(self, table: str, query: dict):
        # Basic query implementation
        return self.client.table(table).select("*").match(query).execute()
