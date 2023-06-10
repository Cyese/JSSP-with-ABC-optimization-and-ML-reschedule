# from utilities import pd


file = open("test.txt", "w+")
file.write("Hello World!")

file.close()

file = open("test.txt", "a")
file.write("Hello again!")

file.close()