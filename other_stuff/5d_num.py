if __name__ == "__main__":
    for x1 in range(1, 10):
        for x2 in range(0, 10):
            for x3 in range(0, 10):
                for x4 in range(0, 10):
                    for x5 in range(0, 10):
                        if (
                            x1 * x2 == 24
                            and x1 + x2 + x3 + x4 + x5 == 26
                            and x4 * 2 == x2
                            and x1 + x3 == x2 + x4
                        ):
                            print(x1, x2, x3, x4, x5, sep="", end="\n")
