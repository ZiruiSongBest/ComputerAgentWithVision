import requests
import torch

class SeeclickClient:
    def __init__(self, url='http://100.119.14.85:8998/upload'):
        self.url = url

    def get_point(self, img_path: str, ref: str) -> torch.Tensor:
        prompt = "In this UI screenshot, what is the position of the element corresponding to the command \"{}\" (with point)?"
        try:
            with open(img_path, 'rb') as img_file:
                files = {'image': (img_path, img_file)}
                data = {'text': prompt.format(ref)}
                response = requests.post(self.url, files=files, data=data)
                response.raise_for_status()  # Raises HTTPError for bad responses
                
                response_data = response.json()
                if 'dot_location' not in response_data:
                    raise ValueError("Missing 'dot_location' in response.")

                location = response_data['dot_location']
                boxes = torch.tensor([[float(coord) for coord in location.strip("()").split(",")]])

                return boxes

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print("The request timed out:", timeout_err)
        except requests.exceptions.RequestException as req_err:
            print("An error occurred while handling your request:", req_err)
        except ValueError as val_err:
            print("There was an issue with the response data:", val_err)
        except Exception as e:
            print("An unexpected error occurred:", e)

        return torch.tensor([])
