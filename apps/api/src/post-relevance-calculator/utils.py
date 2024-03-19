def save_submission(url, file_path):
    with open(file_path, "a") as file:
        file.write(f"{url} \n")