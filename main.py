from pathlib import Path
import json
import shutil

print("hello world")
rules = json.load(open("rules.json"))["rules"]
home = Path.home()
download_dir = home / "Downloads"
print(download_dir)


def valid_name(path,name):
    folder = path / name
    if folder.exists() and folder.is_dir():
        return folder
    
    elif folder.exists() and not folder.is_dir():
        return valid_name(path,name+"1")

    else :
        return folder        


for item in download_dir.iterdir():
    suffix1 = item.suffix.lower()
    src = Path(home / "Downloads" / item.name)
    if not src.exists():
        continue
   
    # if suffix1 in rules[0]:
    #     dst = Path(home / "Downloads" / "pdf" )
    #     if(dst.exists()):
    #         shutil.move(src, dst / item.name)
    #     else:
    #         dst.mkdir()
    #         shutil.move(src, dst / item.name)

        # print(suffix1 + " pdf")

    if suffix1 in rules[0]:
        dst = Path(valid_name(download_dir,"Documents"))
        if(dst.exists()):
            shutil.move(src, dst / item.name)
        else:
            dst.mkdir(parents=True)
            shutil.move(src, dst / item.name)

   

    elif suffix1 in rules[1]:
        dst = Path(valid_name(download_dir,"Images"))
        if(dst.exists()):
            shutil.move(src, dst / item.name)
        else:
            dst.mkdir(parents=True)
            shutil.move(src, dst / item.name)

    elif suffix1 in rules[2]:
        dst = Path(valid_name(download_dir,"Executables"))
        if(dst.exists()):
            shutil.move(src, dst / item.name)
        else:
            dst.mkdir(parents=True)
            shutil.move(src, dst / item.name)

    elif suffix1 in rules[3]:
        dst = Path(valid_name(download_dir,"Textfiles"))
        if(dst.exists()):
            shutil.move(src, dst / item.name)
        else:
            dst.mkdir(parents=True)
            shutil.move(src, dst / item.name)


    else:
        dst = Path(valid_name(download_dir,"Unknown"))
        if(dst.exists()):
            shutil.move(src, dst / item.name)
        else:
            dst.mkdir(parents=True)
            shutil.move(src, dst / item.name)

        # print(suffix1 + " image")
    # elif suffix1 in rules[2]:
    #     dst = Path(home / "Downloads" / "executables" )
    #     if(dst.exists()):
    #         shutil.move(src, dst / item.name)
    #     else:
    #         dst.mkdir()
    #         shutil.move(src, dst / item.name)
    #     # print(suffix1 + " executable")
    # elif suffix1 in rules[3]:
    #     dst = Path(home / "Downloads" / "text" )
    #     if(dst.exists()):
    #         shutil.move(src, dst / item.name)
    #     else:
    #         dst.mkdir()
    #         shutil.move(src, dst / item.name)
    #     # print(suffix1 + " text")
    # else:
    #     dst = Path(home / "Downloads" / "unknown" )
    #     if(dst.exists()):
    #         shutil.move(src, dst / item.name)
    #     else:
    #         dst.mkdir()
    #         shutil.move(src, dst / item.name)
        # print(suffix1 + " unknown")

print(rules)    