import httpx


class DataDAO:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_post_data(self, params: dict):
        with httpx.Client() as client:
            response = client.post(f"{self.base_url}/getDataFromDao", params={"id": params["dao_name"]})
            response.raise_for_status()
            return response.json()


if __name__ == "__main__":
    dao = DataDAO("http://127.0.0.1:8000")
    params = {
        "dat_name": 1,
    }

    dao.fetch_post_data(params)
