import boto3
import base64

print('*** Manage Keys - AWS KMS ***')

kms_client = boto3.client("kms")

def list_keys():
    response = kms_client.list_keys()
    for cmk in response["Keys"]:
        print('- KeyId: ', cmk['KeyId'])
        key_info = kms_client.describe_key(KeyId=cmk["KeyArn"])
        #print(key_info["KeyMetadata"])
        print('Arn: ', key_info["KeyMetadata"]["Arn"])
        print('KeyState: ', key_info["KeyMetadata"]["KeyState"])
        print('KeyManager: ', key_info["KeyMetadata"]["KeyManager"])

def create_cmk():
    response = kms_client.create_key()
    return response['KeyMetadata']['KeyId'], response['KeyMetadata']['Arn']

def create_data_key(cmk_id, key_spec='AES_256'):
    response = kms_client.generate_data_key(KeyId=cmk_id, KeySpec=key_spec)
    return response['CiphertextBlob'], base64.b64encode(response['Plaintext'])

def decrypt_data_key(data_key_encrypted):
    response = kms_client.decrypt(CiphertextBlob=data_key_encrypted)
    return base64.b64encode((response['Plaintext']))

list_keys()

#myNewKey = create_cmk()
#print(myNewKey)

#resp = create_data_key('mrk-0c2847113d51412faa8afafa032f0188')
#print(resp)
#print(resp[0])
#print('Value: ', decrypt_data_key(resp[0]))