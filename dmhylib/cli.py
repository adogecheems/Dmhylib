import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     '''
                                     Welcome to Dmhylib cli!
                                     For more informations, see https://github.com/adogecheems/Dmhylib
                                     ''')

    search = parser.add_subparsers(metavar='Search:')

    search.add_parser('search', )
