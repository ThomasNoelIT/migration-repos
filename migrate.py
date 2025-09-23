import os
import subprocess
import requests

SOURCE_TOKEN = os.getenv("SOURCE_TOKEN")
DEST_TOKEN = os.getenv("DEST_TOKEN")

SOURCE_USER = "TonPseudoPerso"  # compte perso (source)
DEST_USER = "TonPseudoPro"      # compte pro (destination)

API_URL = "https://api.github.com"

def create_repo_on_dest(repo_name):
    url = f"{API_URL}/user/repos"
    headers = {"Authorization": f"token {DEST_TOKEN}"}
    data = {
        "name": repo_name,
        "private": False,   # change en True si tu veux en privé
        "auto_init": True,  # crée un README vide
    }
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 201:
        print(f"[OK] Dépôt {repo_name} créé sur {DEST_USER}")
    elif r.status_code == 422 and "name already exists" in r.text:
        print(f"[SKIP] {repo_name} existe déjà, on continue")
    else:
        raise RuntimeError(f"Erreur création dépôt {repo_name}: {r.text}")

def migrate_repo(repo_name):
    source_url = f"https://{SOURCE_TOKEN}@github.com/{SOURCE_USER}/{repo_name}.git"
    dest_url = f"https://{DEST_TOKEN}@github.com/{DEST_USER}/{repo_name}.git"

    subprocess.run(["git", "clone", "--mirror", source_url], check=True)
    os.chdir(f"{repo_name}.git")

    subprocess.run(["git", "push", "--mirror", dest_url], check=True)

    os.chdir("..")
    subprocess.run(["rm", "-rf", f"{repo_name}.git"])

if __name__ == "__main__":
    # lire liste de dépôts
    with open("repos.txt") as f:
        repos = [line.strip() for line in f if line.strip()]

    # lire l'état (dernier repo migré)
    index_file = "progress.txt"
    if os.path.exists(index_file):
        with open(index_file) as f:
            done = int(f.read().strip())
    else:
        done = 0

    if done >= len(repos):
        print("✅ Tous les dépôts ont déjà été migrés.")
        exit(0)

    repo = repos[done]
    print(f"\n=== Migration de {repo} ===")
    create_repo_on_dest(repo)
    migrate_repo(repo)

    # sauvegarde de la progression
    with open(index_file, "w") as f:
        f.write(str(done + 1))

    print(f"[OK] {repo} migré avec succès ✅")
