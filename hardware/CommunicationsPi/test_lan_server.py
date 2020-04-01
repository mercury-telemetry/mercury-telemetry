import lan_client

if __name__ == "__main__":

    # log_file_name and lan_server_url are configurable for lan_client
    client = lan_client.LANClient()
    sample_payload = {"key1": "value1", "key2": "value2"}
    client.ping_lan_server(sample_payload)
