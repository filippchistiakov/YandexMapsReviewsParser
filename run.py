import argparse
import logging

from parser.log import configure_logging
from parser.main import get_organization_reviews, MODE_DICT
from parser.selenium_helper import make_driver




def run():
    parser = argparse.ArgumentParser()

    parser.add_argument('--org_id',
                        type=str,
                        required=False,
                        default='1124715036',
                        help='''On the company page, the numbers in the address bar.
                            For example, for https://yandex.ru/maps/org/yandeks/1124715036/reviews/ we need 1124715036''')
    parser.add_argument('--debug',
                        action=argparse.BooleanOptionalAction
                        )
    parser.add_argument('--mode',
                        choices=(modes_list := list(MODE_DICT.keys())),
                        required=False,
                        default=modes_list[0],
                        )
    args = parser.parse_args()
    args.debug = args.debug or False
    configure_logging(
        debug=args.debug,
    )
    logging.info(f"{args=} {args.debug=}")
    with make_driver(
            debug=args.debug,
    ) as driver:
        get_organization_reviews(
            org_id=args.org_id,
            driver=driver,
            implicitly_wait=1,
            mode=args.mode,
        )


if __name__ == '__main__':
    run()
