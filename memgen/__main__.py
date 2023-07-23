from sys import argv
from memgen.sv_gen import gen_sv
from memgen.sv_gen_if import gen_sv_if

def __main__():
  num_ifs: int = int(argv[1])
  file_contents: str = gen_sv(num_ifs, "")

  # memory file
  f = open("ram.sv", "w")
  f.write(file_contents)
  f.close()

  # interface
  f = open("ram_if.sv", "w")
  f.write(gen_sv_if())
  f.close()





if __name__ == "__main__":
  __main__()
