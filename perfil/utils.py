import requests
import json
import base64
from namoro.settings import ACCOUNT_ID_ZOOM
from django.http import JsonResponse
from time import time
import os
import sys

def get_access_token(client_id, client_secret):
    token_url = 'https://zoom.us/oauth/token'
    payload = {
        'grant_type': 'account_credentials',
        'account_id': ACCOUNT_ID_ZOOM
    }
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, headers=headers, data=payload)
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print(f"Falha ao obter o token de acesso. Código de status: {response.status_code}")
        print("Resposta da API:", response.json())
        return None

def schedule_meeting(access_token, senha, name, date):
    meeting_data = {
        "topic": name,
        "type": 2,
        "start_time": date,
        "duration": 60,  
        "timezone": "Europe/Lisbon",
        "agenda": name,
        "password": senha,
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": True,
            "mute_upon_entry": True,
            "watermark": False,
            "use_pmi": False,
            "approval_type": 0,
            "registration_type": 1,
            "audio": "both",
            "auto_recording": "none",
            "waiting_room": False
        }
    }
    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(meeting_data))
    if response.status_code == 201:
        meeting_info = response.json()
        # print("Reunião agendada")
        # print(f"ID: {meeting_info['id']}")
        # print(f"Link: {meeting_info['join_url']}")
        return meeting_info['join_url']
    else:
        # return f'{response.json()}'
        return False
        # print(f"erro: {response.status_code}")
        # print("LOG da API:", response.json())