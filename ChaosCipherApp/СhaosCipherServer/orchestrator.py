from typing import Dict, Any, Iterator

from generators import ChaosFactory
from strategies import TextCryptor, FileCryptor, ImageCryptor, AudioCryptor

class CryptoOrchestrator:
    def __init__(self):
        self._factory = ChaosFactory()
        self._strategies = {
            "text": TextCryptor(),
            "image": ImageCryptor(),
            "file": FileCryptor(),
            "audio": AudioCryptor(),
        }
    def execute_request(self, system_type:str, system_params: Dict,
                        crypt_method:str, mode:str, content: Any, process_type:str) -> Any:
        strategy = self._strategies.get(crypt_method)
        generator_factory = self._factory
        generator= generator_factory.create_generator(system_type, system_params, mode)
        if not strategy:
            raise ValueError(f"Unknown crypt_method {crypt_method}")
        result = strategy.process(content, generator, process_type, mode)
        return result
    def execute_request_stream(
                self, system_type: str, system_params: Dict,
                crypt_method: str, mode: str,
                data_stream: Iterator[bytes], process_type: str
        ) -> Iterator[bytes]:
            strategy = self._strategies.get(crypt_method)
            if not strategy:
                raise ValueError(f"Unknown crypt_method {crypt_method}")
            generator = self._factory.create_generator(system_type, system_params, mode)

            if strategy.supports_streaming:
                yield from strategy.process_stream(data_stream, generator, process_type, mode)
            else:
                full_data = b"".join(data_stream)
                result = strategy.process(full_data, generator, process_type, mode)
                yield result