# Returns a letter from the sequence A..Z indexed by "idx". 
# For example, zero returns A, 1 returns B, 2 returns C, ...
def a_itoa(idx: int) -> str:
  return chr(idx + 97)


def if_write_code(idx: int) -> str:
  c: str = a_itoa(idx)
  return """
        if(mem_if_{0}.wb_in[3]) begin
          mem[mem_if_{0}.addr_in][31:24] <= mem_if_{0}.data_in[31:24];
        end
        if(mem_if_{0}.wb_in[2]) begin
          mem[mem_if_{0}.addr_in][23:16] <= mem_if_{0}.data_in[23:16];
        end
        if(mem_if_{0}.wb_in[1]) begin
          mem[mem_if_{0}.addr_in][15:8] <= mem_if_{0}.data_in[15:8];
        end
        if(mem_if_{0}.wb_in[0]) begin
          mem[mem_if_{0}.addr_in][7:0] <= mem_if_{0}.data_in[7:0];
        end""".format(c)

def if_read_code(idx: int) -> str:
  c: str = a_itoa(idx)
  return """
        mem_if_{0}.data_out <= mem[mem_if_{0}.addr_in];""".format(c)

# Generate a systemverilog memory module to be used within FPGA 
# projects. The number of interfaces is configurable (num_ifs).
# a text file containing 32-bit wide hexadecimal words can be 
# provided, whose data will be used to initialize the memory.
def gen_sv(num_ifs: int, code_txt: str) -> str:

  # header generation
  interface_vector_declaration = ",\n".join([("    mem_if.MEM mem_if_" + a_itoa(i)) for i in range(num_ifs)])
  
  module_declaration = """
  module ram #(SIZE = 65536)(
    input logic clock,
    input logic reset,
    input logic enable,
{0}
  );""".format(interface_vector_declaration)


  # memory initialization
  boot = open(code_txt, "r+")
  hex_line = boot.read().splitlines()
  memory_initialization = """
  initial begin
"""
  for i in range(0, len(hex_line)):
      line = f"    mem[{i}] = 'h{hex_line[i]};\n"
      memory_initialization += line

  memory_initialization += ("  end\n")
  boot.close()

  # memory vector generation
  memory_vector = """
  reg[31:0] mem[SIZE];"""


  # process region
  rw_proc = """
  always_ff @(posedge clock) begin
    if(enable)begin  
      {0}
      {1}
    end
  end""".format(
    "\n".join([if_write_code(i) for i in range(0, num_ifs) ]),
    "\n".join([if_read_code(i) for i in range(0, num_ifs) ])
  )


  endmodule = "endmodule"


  return "\n".join([
    module_declaration,
    memory_vector,
    memory_initialization,
    rw_proc,
    endmodule
  ])

