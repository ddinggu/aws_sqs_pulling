# AWS SQS 큐에 적재된 메세지 처리 방법

---

### 필요 패키지 설치

```
$ pip install -r requirements.txt
```

### SDK 및 타 AWS 서비스를 활용한 해결방안

1. Consumer Client를 직접 만들어 소비 후 큐 메세지 제거

```
$ python send.py
```

2. AWS 콘솔 상 SQS -> SNS 전달이 불가하여, SQS 메세지 전달 시 SNS에 토픽 전파

```
$ python sqs_to_sns.py
```

3. AWS 콘솔 상 lambda 함수의 트리거로 추가
   -> 이벤트 발생 시 슬랙으로 메세지 전달
   `sqs_to_lambda.py` 파일 참고
