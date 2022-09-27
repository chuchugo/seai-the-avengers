with open("coverage.xml") as f:
    for num, line in enumerate(f, 1):
        if "line-rate" in line and "<package" not in line:
            line = line.strip()
            coverage = line[line.index("line-rate") :line.index("branch-rate=")]

            if "<coverage" in line:
                print("Overall coverage : " + coverage+"\n")
            else:
                file = line[line.index('name="') :line.index("filename")]
                print("file" + file)
                print( coverage +"\n")