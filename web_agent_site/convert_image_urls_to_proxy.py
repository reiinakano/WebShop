import json
from tqdm import tqdm

from web_agent_site.utils import DEFAULT_FILE_PATH


def main():
    print(f"Opening {DEFAULT_FILE_PATH}")
    with open(DEFAULT_FILE_PATH, "r") as f:
        list_of_dicts = json.load(f)

    for dct in tqdm(list_of_dicts):
        for i in range(len(dct["images"])):
            if dct["images"][i].startswith("https://m.media-amazon.com/"):
                dct["images"][i] = dct["images"][i].replace("https://m.media-amazon.com/", "http://10.0.2.1:8050/p/m.media-amazon.com/")

        customization_options = dct["customization_options"]
        if customization_options:
            for _, option_contents in customization_options.items():
                if option_contents is None:
                    continue
                for option_content in option_contents:
                    option_image = option_content.get('image', None)
                    if option_image and option_image.startswith("https://m.media-amazon.com/"):
                        option_content["image"] = option_content["image"].replace("https://m.media-amazon.com/", "http://10.0.2.1:8050/p/m.media-amazon.com/")

    with open(DEFAULT_FILE_PATH, "w") as f:
        json.dump(list_of_dicts, f)


if __name__ == "__main__":
    main()
