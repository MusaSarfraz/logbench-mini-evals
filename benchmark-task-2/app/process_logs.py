import json

def main():
    counts={}
    with open("/app/logs.txt") as f:
        for line in f:
            parts=line.split()
            level=parts[2]
            counts[level]=counts.get(level,0)+1

    with open("/app/summary.json","w")  as f:
        json.dump(counts,f)      

if __name__=="__main__" :
    main()     