# VDRC_pyRTCM

## 개요
파이썬으로 구현한 RTCM parser 입니다.
시리얼 포트로 부터 메세지를 읽어 각각의 단일 RTCM 메세지로 분리하는 기능까지 구현되어 있습니다.

### 요구되는 패키지
* serial : 시리얼 포트에 접근해 데이터를 읽음
    '''pip install pyserial'''
* binascii : bytes 개체를 다루는데 사용 (선택적)
 
## API
### 함수 '''getSingleRtcmMsg()'''
+ 단일 RTCM 메세지를 읽어옵니다.
+ 단일 RTCM 메세지를 모두 읽을때 까지 함수가 블록됩니다.
    
#### 입력 매개변수
+ 입력 매개변수는 없습니다

#### 출력 매개변수
+ 출력은 배열의 형태입니다.
+ '''[rtcmFullmsg, rtcmDataFrame, rtcmId]'''
##### return[0] (rtcmFullmsg)
int의 1차원 배열입니다. 각각의 요소가 메세지의 한 바이트입니다. RTCM 메세지의 Magic Marker (0xD3) 부터 CRC 까지 전체 메세지가 포함되어 있습니다. 
##### return[1] (rtcmDataFrame)
int의 1차원 배열입니다. RTCM 메세지 중 데이터 부분만 포함되어 있습니다
##### return[2] (rtcmId)
int입니다. RTCM 메세지 ID 입니다.