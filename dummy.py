import time


def compute_CRC(message, length):
    crc = 0x0ffff
    temp = None
    quick = None
    for i in range(0, length):
        temp = (crc >> 8) ^ message[i]
        crc <<= 8
        quick = temp ^ (temp >> 4)
        crc ^= quick
        quick <<= 5
        crc ^= quick
        quick <<= 7
        crc ^= quick
    return crc


Data = b"\xaa\x41\x00\x12\x00\x0a\x64\x02\x43\xb6\x00\x00\x00\x00\x00\x05\x72\x2d"
count = 1
for byte in Data:
    print(count, byte)
    count += 1


CMDSYNC = [0, 10]
message = CMDSYNC[0].to_bytes(2, byteorder='big')
message += CMDSYNC[1].to_bytes(2, byteorder='big')
fsize = [18 >> 8, 18]
message += fsize[0].to_bytes(2, byteorder='big')
message += fsize[1].to_bytes(2, byteorder='big')
pmu_id = [0, 10]
message += pmu_id[0].to_bytes(2, byteorder='big')
message += pmu_id[1].to_bytes(2, byteorder='big')
sec = time.time()
sec = int(sec)
sec = [sec >> 24, sec >> 16, sec >> 8, sec]
message += sec[0].to_bytes(2, byteorder='big')
message += sec[1].to_bytes(2, byteorder='big')
# message += sec[2].to_bytes(2, byteorder='big')
# message += sec[3].to_bytes(2, byteorder='big')
# print(sec[3].to_bytes(2, byteorder='big'))
fracsec = [0, 0, 0, 0]
message += fracsec[0].to_bytes(2, byteorder='big')
message += fracsec[1].to_bytes(2, byteorder='big')
message += fracsec[2].to_bytes(2, byteorder='big')
message += fracsec[3].to_bytes(2, byteorder='big')
CMDDATASEND = [0, 5]
message += CMDDATASEND[0].to_bytes(2, byteorder='big')
message += CMDDATASEND[1].to_bytes(2, byteorder='big')
chk = compute_CRC(message, 16)
Chk1 = (chk >> 8) & ~(~0 << 8)
chk2 = chk & ~(~0 << 8)
print(chk2)
message += Chk1.to_bytes(2, byteorder='big')
message += chk2.to_bytes(2, byteorder='big')
print(chk2.to_bytes(2, byteorder='big'))
print(message)
