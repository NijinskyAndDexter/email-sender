import jsonpickle

from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths

from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver, Response
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent, event_source

import email_helper

logger = Logger(clear_state=True)
rest_api = APIGatewayRestResolver()

@rest_api.post("/email")
def send_email():
  json_body = rest_api.current_event.json_body
  logger.info("unpacked json body")
  logger.debug("value of json body", extra={"json_body": json_body})
  email_helper.send_email(**json_body)
  response_body = "Rebecca says thanks! She'll get back to you as soon as she can."
  return Response(
    status_code=200, 
    content_type="application/json", 
    body=jsonpickle.encode(response_body, unpicklable=False)
  )

# TODO not profesh at all
@rest_api.route(".+", method=["GET", "PUT", "POST", "DELETE", "OPTIONS"])
def get_outta_here(): 
  response_body = {"message": "what are you doing?! this is not an api endpoint!!!!"}
  return Response(
    status_code=404, 
    content_type="application/json", 
    body=jsonpickle.encode(response_body, unpicklable=False)
  )

@event_source(data_class=APIGatewayProxyEvent)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event: APIGatewayProxyEvent, context):
  logger.append_keys(path=event.path, method=event.http_method)
  try: 
    return rest_api.resolve(event, context)
  except Exception: 
    logger.exception("something unexpected happened")
    return Response(
      status_code=500, 
      content_type="application/json", 
      body=jsonpickle.encode("We've encountered an unexpected error. Please try again at a later time.")
    )