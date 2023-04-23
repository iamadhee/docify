class Model:

    def __init__(
        self,
        api_key: str,
        model: str,
        api_wait: int = 60,
        api_retry: int = 6,
        **kwargs
    ):
        self.api_key = api_key
        self.model = model
        self.api_wait = api_wait
        self.api_retry = api_retry

    def supported_models(self):
        raise NotImplementedError

    def _verify_model(self):
        raise NotImplementedError

    def set_key(self, api_key: str):
        raise NotImplementedError

    def run(self, prompts: str):
        raise NotImplementedError
