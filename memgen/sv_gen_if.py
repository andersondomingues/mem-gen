def gen_sv_if() -> str:
    return """
interface ram_if (input clock, input reset);

logic[31:0] data_in; 
logic[31:0] addr_in;
logic[31:0] data_out;
logic[3:0] wb_in;

modport MEM (
    input data_in, addr_in, wb_in, clock, reset,
    output data_out);

modport DUT (
    output data_in, addr_in, wb_in, 
    input data_out, clock, reset);

endinterface: ram_if
"""