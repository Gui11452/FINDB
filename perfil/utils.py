import requests
import json
import base64
from namoro.settings import TOKEN_API_CLOUDFARE_R2, ACCOUNT_ID_CLOUDFARE_R2, ACCESS_KEY_ID_CLOUDFARE_R2, SECRET_ACCESS_CLOUDFARE_R2, ACCOUNT_ID_ZOOM
from django.http import JsonResponse
from time import time
import os
import sys


# Cloudfare - Início
# https://developers.cloudflare.com/r2/api/s3/api/
import boto3
from botocore.client import Config
""" Valores Possíveis para ACL:
- private: Apenas o dono do bucket pode acessar o objeto.
- public-read: Qualquer pessoa pode ler o objeto publicamente (recomendado para objetos que precisam ser acessados via link público).
- public-read-write: Qualquer pessoa pode ler e escrever no objeto (não recomendado, pois permite modificações públicas).
- authenticated-read: Somente usuários autenticados podem ler o objeto. """

def add_file_bucket(foto, video, bucket_name, object_name_foto, object_name_video):
    # Configuração do cliente S3 com credenciais e endpoint do Cloudflare R2
    s3 = boto3.client('s3',
        aws_access_key_id=ACCESS_KEY_ID_CLOUDFARE_R2,
        aws_secret_access_key=SECRET_ACCESS_CLOUDFARE_R2,
        endpoint_url=f'https://{ACCOUNT_ID_CLOUDFARE_R2}.r2.cloudflarestorage.com',
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

    obj_status = {}

    # Verifica se o bucket existe
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    if bucket_name not in buckets:
        obj_status['error_bucket'] = 'Bucket não existe.'
        return obj_status

    # Upload da foto
    if foto:
        try:
            # Lê o conteúdo do arquivo de foto em binário
            s3.put_object(Bucket=bucket_name, Key=object_name_foto, Body=foto.read(), ACL='public-read')
            obj_status['success_foto'] = f"Foto '{object_name_foto}' enviada com sucesso!"
        except Exception as e:
            obj_status['error_foto'] = str(e)

    # Upload do vídeo
    if video:
        try:
            # Lê o conteúdo do arquivo de vídeo em binário
            s3.put_object(Bucket=bucket_name, Key=object_name_video, Body=video.read(), ACL='public-read')
            obj_status['success_video'] = f"Vídeo '{object_name_video}' enviado com sucesso!"
        except Exception as e:
            obj_status['error_video'] = str(e)

    obj_status['response'] = response
    return obj_status



def add_certificado_bucket(arquivo, bucket_name_arquivo, object_name_arquivo):
    # Configuração do cliente S3 com credenciais e endpoint do Cloudflare R2
    s3 = boto3.client('s3',
        aws_access_key_id=ACCESS_KEY_ID_CLOUDFARE_R2,
        aws_secret_access_key=SECRET_ACCESS_CLOUDFARE_R2,
        endpoint_url=f'https://{ACCOUNT_ID_CLOUDFARE_R2}.r2.cloudflarestorage.com',
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

    obj_status = {}

    # Verifica se o bucket existe
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    if bucket_name_arquivo not in buckets:
        obj_status['error_bucket'] = 'Bucket não existe.'
        return obj_status

    # Upload certificado
    try:
        # Lê o conteúdo do arquivo de foto em binário
        s3.put_object(Bucket=bucket_name_arquivo, Key=object_name_arquivo, Body=arquivo.read(), ACL='public-read')
        obj_status['success_arquivo'] = f"Arquivo '{object_name_arquivo}' enviado com sucesso!"
    except Exception as e:
        obj_status['error_arquivo'] = str(e)

    obj_status['response'] = response
    return obj_status



def generate_presigned_url(bucket_name, object_name):
    BUCKET_NAME = 'findb-therapy-perfil'
    OBJECT_NAME = 'foto2.jpg'
    EXPIRATION = 3600 # 3600s - 1 hora

    s3 = boto3.client('s3',
        aws_access_key_id=ACCESS_KEY_ID_CLOUDFARE_R2,
        aws_secret_access_key=SECRET_ACCESS_CLOUDFARE_R2,
        endpoint_url=f'https://{ACCOUNT_ID_CLOUDFARE_R2}.r2.cloudflarestorage.com',
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

    try:
        # Gerar URL pré-assinada
        response = s3.generate_presigned_url('get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': OBJECT_NAME},
            ExpiresIn=EXPIRATION)
    except Exception as e:
        print(f"Erro ao gerar URL pré-assinada: {e}")
        return JsonResponse({'error': e})
    
    return JsonResponse({'link': response})


def delete_object_from_r2(bucket_name, object_name):
    s3 = boto3.client('s3',
        aws_access_key_id=ACCESS_KEY_ID_CLOUDFARE_R2,
        aws_secret_access_key=SECRET_ACCESS_CLOUDFARE_R2,
        endpoint_url=f'https://{ACCOUNT_ID_CLOUDFARE_R2}.r2.cloudflarestorage.com',
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

    obj_status = {}

    try:
        # Excluindo o objeto do bucket
        response = s3.delete_object(Bucket=bucket_name, Key=object_name)
    except Exception as e:
        obj_status['error_delete'] = e
        return obj_status
    
    obj_status['response'] = response
    return obj_status
# Cloudfare - Fim



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