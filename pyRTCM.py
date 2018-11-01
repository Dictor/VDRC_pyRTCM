import serial
import binascii

def ByteToHexStr(byte): 
    return binascii.hexlify(byte).decode('utf-8').upper()

def getSingleRtcmMsg():
    dropMsg, rtcmFullmsg, rtcmDataFrame = [], [], []
    msgByteCount, rtcmId, rtcmLength = 0, 0, 0
    while True:
        nowByte = int(ByteToHexStr(gpsSerial.read(1)), base=16)
        if msgByteCount == 0:
            if nowByte == 211: #0xD3
                if len(dropMsg) != 0:
                    print("[UNKNOWN] : ", end="")
                    print(dropMsg)
                    dropMsg = []
            else:
                dropMsg.append(nowByte)
                continue
        elif msgByteCount == 1:
            rtcmLength = (nowByte & 3) << 8
        elif msgByteCount == 2:
            rtcmLength += nowByte
        elif msgByteCount <= 2 + rtcmLength:
            rtcmDataFrame.append(nowByte)
        #elif (msgByteCount > 2 + rtcmLength) and (msgByteCount <= (2 + rtcmLength) + 2):
            #여기는 CRC 앞 두바이트
        elif msgByteCount == (2 + rtcmLength) + 3:
            rtcmFullmsg.append(nowByte) #CRC 마지막 한바이트
            rtcmId = rtcmFullmsg[3]
            rtcmId = rtcmId << 4
            rtcmId = rtcmId | ((rtcmFullmsg[4] >> 4) or 15)
            return [rtcmFullmsg, rtcmDataFrame, rtcmId]
        msgByteCount += 1
        rtcmFullmsg.append(nowByte)

gpsSerial = serial.Serial("COM" + input("GPS의 시리얼 포트 번호를 입력하세요 : COM"), 115200, timeout=None)
rtcmExplain = {1005 : "Stationary RTK reference station ARP", 1074 : "GPS MSM4", 1077 : "GPS MSM7", 1084 : "GLONASS MSM4", 1087 : "GLONASS MSM7",  1094 : "Galileo MSM4",  1097 : "Galileo MSM7",  1124 : "BeiDou MSM4",  1127 : "BeiDou MSM7", 1230 : "GLONASS code-phase biases", 4072 : "Reference station PVT (u-blox proprietary RTCM Message)"}
while True:
    rtcmMsg = getSingleRtcmMsg()
    rtcmex = rtcmExplain[rtcmMsg[2]] if rtcmMsg[2] in rtcmExplain else str(rtcmMsg[2])
    print("[RTCM] (", rtcmex , ") : ", rtcmMsg[0])