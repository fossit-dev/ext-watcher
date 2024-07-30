import subprocess
import os

token = os.getenv('TOKEN')

map = {
    "go-guardian": {
        "extension-id": "haldlgldplgnggkjaafhelgiaglafanh",
        "versions": []
    },

    "securly-for-chromebooks": {
        "extension-id": "joflmkccibkooplaeoinecjbmdebglab",
        "versions": []
    },

    "blocksi": {
        "extension-id": "pgmjaihnmedpcdkjcgigocogcbffgkbn",
        "versions": []
    },

    "securly-for-chromebooks-old": {
        "extension-id": "iheobagjkfklnlikgihanlhcddjoihkg",
        "versions": []
    },

    "linewize-connect": {
        "extension-id": "ddfbkhpmcdbciejenfcolaaiebnjcbfc",
        "versions": []
    },

    "securly-for-classrooms": {
        "extension-id": "jfbecfmiegcjddenjhlbhlikcbfmnafd",
        "versions": []
    }
}

os.chdir('ext-watcher/extensions')

for repo_name, details in map.items():
    ext_id = details["extension-id"]

    os.chdir(ext_id)

    versions = details["versions"]

    for folder in os.listdir():
        if os.path.isdir(folder):
            versions.append(folder)

    map[repo_name]["versions"] = versions
    os.chdir('..')

for repo_name, details in map.items():
    ext_id = details["extension-id"]
    versions = details["versions"]

    os.chdir(ext_id)

    for version in versions:
        os.chdir(version)

        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', f'Add version {version}'])

        branch_name = f'version-{version}'
        subprocess.run(['git', 'branch', '-M', branch_name])

        remote_url = f'https://{token}@github.com/fossit-dev/{repo_name}.git'
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url])

        subprocess.run(['git', 'push', '-u', 'origin', branch_name])

        os.chdir('..')
    os.chdir('..')
