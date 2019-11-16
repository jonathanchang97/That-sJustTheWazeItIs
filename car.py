import requests
import sys
import json
import time

class Car:
    def __init__ (self, curr, dest, server, port=8080):
        self.curr = curr
        self.dest = dest
        self.url = server
        self.port = port
        self.wait_time = 0
    
    def loop(self):
        print(f"Beginning journey from {self.curr} to {self.dest}")
        while True:
            time.sleep(self.wait_time) 
            res = json.loads(requests.post(self.url, json = {"curr": self.curr, "dest": self.dest}).text)
            if self.dest == res["curr"]:
                break
            if res["dir"] == "straight":
                print(f"Continue straight on {self.curr}")
            else:
                print(f"Turn {res['dir']} onto {res['curr']}")
            self.curr = res['curr']
            self.wait_time = res['wait_time']

        print("You have arrived at your destination")


def main(argv):
    argc = len(argv)
    curr, dest, server = "", "", ""
    if argc == 4:
        curr = argv[1]
        dest = argv[2]
        server = argv[3]
    car = Car(curr, dest, server)
    car.loop()
   

if __name__ == "__main__":
    main(sys.argv) 
