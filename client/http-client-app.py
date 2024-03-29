import requests
import time
import threading
import os




room_number=-1

def get_messages(room_number):
    base_url = os.environ.get("CHAT_API_BASE_URL", "http://localhost:5000")
    response = requests.get(f'{base_url}/messages?room_number={room_number}')
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def insert_user(username,room_number):
    base_url = os.environ.get("CHAT_API_BASE_URL", "http://localhost:5000")
    response = requests.post(f'{base_url}/user',json={'username':username,'room_number':room_number})
    if response.status_code == 200:
        return response.json()
    else:
        return None


def send_message(message):
    base_url = os.environ.get("CHAT_API_BASE_URL", "http://localhost:5000")
    response = requests.post(f'{base_url}/messages', json=message)
    if response.status_code != 200:
        print('error: failed to send message')
        
def poll_messages(room_number):
    while True:
        messages = get_messages(room_number)
        for message in messages: 
            print(message[0]+":"+message[1])

        time.sleep(1)


def main_loop():
    username = input('Enter your username: ')
    # Choose to implement chosen 'known' rooms instead of implementing room displaying list display as it was not requested
    room_number = input('Enter your room number: ')
    userid = insert_user(username, room_number)
    polling_messages = threading.Thread(target=poll_messages,args=(room_number,))
    polling_messages.start()
    try:
        while True:
            text = input('Enter your message: ')
            message = {"userid": userid, "message": text}
            send_message(message)
    finally:
        polling_messages.join()

if __name__ == "__main__":
    main_loop()