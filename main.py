import os
import random
import json

POOL_DIR = "pools"

def load_pools(filename):
    path = os.path.join(POOL_DIR, filename)
    with open(path, 'r' , encoding='utf-8') as f:
        items = []
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                items.append(line)
    return items

def lottery(pool , k):
    if k > len(pool):
        raise ValueError("抽取数量不能大于池子中的元素数量")
    return random.sample(pool, k)

def reload_pools():
    global worlds_pool, main_character_identity, main_character_personality, topic_pool, cheat_pool
    worlds_pool = load_pools("世界观.txt")
    main_character_identity = load_pools("主角身份.txt")
    main_character_personality = load_pools("主角性格.txt")
    topic_pool = load_pools("题材.txt")
    cheat_pool = load_pools("金手指.txt")

def reload_config(config_file="config.json"):
    with open(config_file, 'r', encoding='utf-8') as f:
        global config
        config = json.load(f)
    for key, val in config.items():
        if not isinstance(val, int) or val < 0:
            raise ValueError(f"配置项 {key} 的值必须是非负整数")
    

def main():
    reload_pools()
    reload_config()

    categories = [
        ("世界观", worlds_pool),
        ("主角身份", main_character_identity),
        ("主角性格", main_character_personality),
        ("题材", topic_pool),
        ("金手指", cheat_pool)
    ]
    print("欢迎来到小说创作抽签器！")

    while True:
        print("\n抽签结果：")
        for name, pool in categories:
            k = config.get(name, 0)
            if k > 0:
                try:
                    results = lottery(pool, k)
                    print(f"{name}：{', '.join(results)}")
                except ValueError as e:
                    print(f"{name}：{e}")

        cont = input("\n是否继续抽签？(y/n): ").strip().lower()
        if cont == 'n':
            print("感谢使用，再见！")
            break
        elif cont == 'c':
            reload_config()
            print("配置已重新加载。")
        elif cont == 'r':
            reload_pools()
            print("池子已重新加载。")


if __name__ == "__main__":
    main()