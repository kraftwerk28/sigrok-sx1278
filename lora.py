mode = [
    "SLEEP",
    "STDBY",
    "FSTX",
    "TX",
    "FSRX",
    "RXCONTINUOUS",
    "RXSINGLE",
    "CAD",
]

irq = [
    "RxTimeout",
    "RxDone",
    "PayloadCrcError",
    "ValidHeader",
    "TxDone",
    "CadDone",
    "FhssChangeChannel",
    "CadDetected",
]

reg = dict(
    RegFifo=0x00,
    RegOpMode=0x01,
    RegFrfMsb=0x06,
    RegFrfMid=0x07,
    RegFrfLsb=0x08,
    RegPaConfig=0x09,
    RegOcp=0x0B,
    RegLna=0x0C,
    RegFifoAddrPtr=0x0D,
    RegFifoTxBaseAddr=0x0E,
    RegFifoRxBaseAddr=0x0F,
    RegFifoRxCurrentAddr=0x10,
    RegIrqFlags=0x12,
    RegRxNbBytes=0x13,
    RegPktSnrValue=0x19,
    RegPktRssiValue=0x1A,
    RegRssiValue=0x1B,
    RegModemConfig1=0x1D,
    RegModemConfig2=0x1E,
    RegPreambleMsb=0x20,
    RegPreambleLsb=0x21,
    RegPayloadLength=0x22,
    RegModemConfig3=0x26,
    RegFreqErrorMsb=0x28,
    RegFreqErrorMid=0x29,
    RegFreqErrorLsb=0x2A,
    RegRssiWideband=0x2C,
    RegDetectionOptimize=0x31,
    RegInvertiq=0x33,
    RegDetectionThreshold=0x37,
    RegSyncWord=0x39,
    RegInvertiq2=0x3B,
    RegDioMapping1=0x40,
    RegDioMapping2=0x41,
    RegVersion=0x42,
    RegPaDac=0x4D,
)

reg_label = {v: k for k, v in reg.items()}
