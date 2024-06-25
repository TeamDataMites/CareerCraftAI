def log(tag="", message=""):
    with open("logs.txt", "a") as f:
        f.write(f"{tag} : {message}\n")