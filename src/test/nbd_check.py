import random

def main():
    results = []
    for _ in range(299):
        if random.randint(1,101) / 100 <= 1/100:
            if random.randint(1,101) / 100 <= 1/15:
                results.append(True)

    print(len(results))


if __name__ == "__main__":
    main()