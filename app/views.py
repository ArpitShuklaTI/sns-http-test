import json
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def list_users(request):
    return Response(['Arpit', 'Utsav', 'Man', 'Sahil', 'Andrei'])


@api_view(['POST'])
def receive_sns_notification(request):
    print('Started receive_sns_notification')
    print(request.headers)
    if 'X-Amz-Sns-Message-Type' in request.headers:
        print('X-Amz-Sns-Message-Type header found')
        payload = json.loads(request.body.decode('utf-8'))
        message_type = request.headers['X-Amz-Sns-Message-Type']
        if message_type == 'SubscriptionConfirmation':
            print("SubscriptionConfirmation message received")
            subscribe_url = payload.get('SubscribeURL')
            res = requests.get(subscribe_url)
            if res.status_code != status.HTTP_200_OK:
                print(f'Failed to verify SNS Subscription. '
                      f'verification_response: {res.content}, sns-payload: {request.body}')

                return Response(
                    data=f'Invalid verification:\n${res.content}',
                    status=status.HTTP_400_BAD_REQUEST
                )
            print('Subscription confirmed')
        else:
            sns_message = json.loads(payload.get('Message'))
            meeting_id = sns_message['meetingId']
            message = sns_message['message']
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(meeting_id, {
                'type': 'send_message',
                'message': message
            })
            print(f"Payload meeting id: {meeting_id} && message: {message}")
    return Response(status=status.HTTP_200_OK)
