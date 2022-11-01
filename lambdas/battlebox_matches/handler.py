import battlebox_logic


def lambda_handler(event, context):
    match_id = battlebox_logic.create_match()
    return {'statusCode': 200,'body': match_id}