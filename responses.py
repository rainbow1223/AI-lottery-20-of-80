def error_400_message(message):
    return {
        "status": 'ERROR',
        "statusCode": '400',
        "message": message
        }

def error_401_message(message):
    return {
        "status": 'ERROR',
        "statusCode": '401',
        "message": message
        }

def error_403_message(message):
    return {
        "status": 'ERROR',
        "statusCode": '403',
        "message": message
        }

def success_200_message(message):
    return {
        "status": 'SUCCESS',
        "statusCode": '200',
        "message": message
        }

def error_500_message(object, function):
    return {
        "status": 'ERROR',
        "statusCode": '400',
        "message": '{} is not valid for {}'.format(object, function)
        }
