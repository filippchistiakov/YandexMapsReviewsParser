from parser.main import get_organization_reviews
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--org_id', type=str, required=True,
                        help='''On the company page, the numbers in the address bar.
                        For example, for https://yandex.ru/maps/org/yandeks/1124715036/reviews/ we need 1124715036''')

    args = parser.parse_args()
    get_organization_reviews(org_id=args.org_id)
