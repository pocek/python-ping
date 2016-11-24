import struct


class IcmpEcho:

    def __init__(self, type=8, code=0, checksum=0, identifier=0, sequence_number=0, payload=b''):
        self.type = type
        self.code = code
        self.checksum = checksum
        self.identifier = identifier
        self.sequence_number = sequence_number
        self.payload = payload

    @property
    def calculated_checksum(self):
        data = struct.pack('>BBHHH', self.type, self.code, 0, self.identifier, self.sequence_number) + self.payload
        if len(data) & 0x1: # Odd number of bytes
            data += b'\0'
        checksum = 0
        for pos in range(0, len(data), 2):
            b1 = data[pos]
            b2 = data[pos + 1]
            checksum += (b1 << 8) + b2
        while checksum >= 0x10000:
            checksum = (checksum & 0xffff) + (checksum >> 16)
        checksum = ~checksum & 0xffff
        return checksum

    @property
    def valid_checksum(self):
        return self.checksum == self.calculated_checksum

    def to_bytes(self):
        return struct.pack('>BBHHH', self.type, self.code, self.checksum, self.identifier, self.sequence_number) + self.payload

    @staticmethod
    def from_bytes(data):
        if len(data) < 8:
            raise ValueError('ICMP Echo packet must be at least 8 bytes')
        ret = IcmpEcho()
        ret.payload = data[8:]
        header = struct.unpack('>BBHHH', data[0:8])
        ret.type = header[0]
        if ret.type not in (0, 8):
            raise ValueError('Not a ICMP Echo message (type={type})'.format(type=ret.type))
        ret.code = header[1]
        ret.checksum = header[2]
        ret.identifier = header[3]
        ret.sequence_number = header[4]
        return ret

    def __repr__(self):
        return 'IcmpEcho(type={type}, code={code}, checksum={checksum}, identifier={identifier}, sequence_number={sequence_number}, payload={payload!r})'.format(
            type=self.type,
            code=self.code,
            checksum=self.checksum,
            identifier=self.identifier,
            sequence_number=self.sequence_number,
            payload=self.payload
            )
