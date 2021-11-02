from fastapi.responses import JSONResponse

class ErrorCode():

    def __init__(self,status, json_response):
        import pdb;pdb.set_trace()
        self.status = status
        self.json_response = json_response


    def main(self):
        import pdb;pdb.set_trace()
        error_code = self.status
        error_message = self.json_response

        if self.status == 401:
            error_code,error_message = 401,"You are not authorized to access this resource."

        if self.status == 403:
            error_code,error_message = 403,"The request has been refused (most likely for exceeding rate limit)."

        elif self.status == 429:
            error_code,error_message = 429," This request cannot be served due to the application’s rate limit having been exhausted for the resource."

        elif self.status == 503:
            error_code,error_message =  503 ,"Github service is up, but overloaded with requests."

        elif self.status == 504:
            error_code,error_message =  504 ,"Gitserver is up but can not be accessed due to failure on our tech stack."


        elif self.status == 304:
            error_code,error_message = 304,"There is no new data to return."

        return JSONResponse(
            status_code = error_code,
            content= {"message" : error_message}
        )

