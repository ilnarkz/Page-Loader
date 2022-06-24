def save_page(data: str, file_path: str) -> None:
    with open(file_path, 'w') as f:
        f.write(data)
