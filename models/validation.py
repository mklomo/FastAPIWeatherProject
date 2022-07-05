class ValidationError(Exception):
    
    def __init__(self, err_msg: str, status_code: int):
        super().__init__(err_msg)
        self.err_msg = err_msg
        self.status_code = status_code