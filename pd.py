import sigrokdecode as srd
from . import lora


class Decoder(srd.Decoder):
    api_version = 3
    id = "sx1278"
    name = "SX 1278"
    longname = "SX 1278"
    desc = "A decoder for LoRa chips controlled through SPI"
    license = "mit"
    inputs = ["spi"]
    outputs = []
    tags = ["LoRa", "SX1278"]
    annotations = (
        ("r", "Read flag"),
        ("w", "Write flag"),
        ("addr", "Address"),
        ("data", "Data"),
    )
    annotation_rows = (("commands", "Commands", (0, 1, 2, 3)),)

    def __init__(self):
        self.mosi_bits = []
        self.miso_bits = []

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def reset(self):
        pass

    def decode(self, ss, es, data):
        if data[0] == "BITS" and len(self.mosi_bits) < 2:
            self.mosi_bits.append(data[1])
            self.miso_bits.append(data[2])
        if data[0] == "TRANSFER" and len(self.mosi_bits) >= 2:
            _, mosi, miso = data
            if len(mosi) < 1:
                return
            addr = mosi[0]
            reg = addr.val & 0x7F
            reg_name = lora.reg_label.get(reg)
            if reg_name is None:
                return
            rwbit = self.mosi_bits[0][-1]
            addrbit = self.mosi_bits[0][-2]

            if addr.val & 0x80:
                self.put(rwbit[1], rwbit[2], self.out_ann, [1, ["Write", "W"]])
                self.put(
                    addrbit[1],
                    addr.es,
                    self.out_ann,
                    [2, [reg_name, reg_name.removeprefix("Reg")]],
                )
                data1 = mosi[1]
                data1_bits = self.mosi_bits[1]
            else:
                self.put(rwbit[1], rwbit[2], self.out_ann, [0, ["Read", "R"]])
                self.put(
                    addrbit[1],
                    addr.es,
                    self.out_ann,
                    [2, [reg_name, reg_name.removeprefix("Reg")]],
                )
                data1 = miso[1]
                data1_bits = self.miso_bits[1]

            if reg == lora.reg["RegFifo"]:
                pass
            elif reg == lora.reg["RegOpMode"]:
                self.put(
                    data1_bits[7][1],
                    data1_bits[7][2],
                    self.out_ann,
                    [3, ["LoRa" if data1.val & 0x80 else "FSK/OOK"]],
                )
                self.put(
                    data1_bits[3][1],
                    data1_bits[3][2],
                    self.out_ann,
                    [3, ["LF" if data1.val & 0x08 else "HF"]],
                )
                self.put(
                    data1_bits[2][1],
                    data1_bits[0][2],
                    self.out_ann,
                    [3, [lora.mode[data1.val & 0x07]]],
                )
            elif reg == lora.reg["RegIrqFlags"]:
                flags = []
                for i in range(8):
                    if data1.val << i & 0x80:
                        bit = data1_bits[7 - i]
                        self.put(bit[1], bit[2], self.out_ann, [3, [lora.irq[i]]])
            else:
                self.put(data1.ss, data1.es, self.out_ann, [3, [hex(data1.val)]])
            self.mosi_bits, self.miso_bits = [], []
