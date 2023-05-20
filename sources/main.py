import fire
import logging

from extractor_nbc import NbcExtractor
from extractor_abc import AbcExtractor
class Main:
    def __init__(self) -> None:
        logging.basicConfig(
            format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s",  # noqa: E501
            level=logging.INFO,
        )

    def run_all(self) -> None:
        output = {}
        nbc_output = NbcExtractor().extract()
        abc_output = AbcExtractor().extract()
        output.update(nbc_output)
        output.update(abc_output)
        for slug in output:
            for data in output[slug]:
                logging.info(f'{slug=} {data=}')

if __name__ == "__main__":
    fire.Fire(Main)