if __name__ == "__main__":
    from Utils import CarParser

    p = CarParser("./sample.txt")

    while True:
        try:
            roi = p.nextRoi()
            if roi == None:
                continue
            print(roi)
        except Exception:
            break
