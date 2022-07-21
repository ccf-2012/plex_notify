from plexapi.server import PlexServer
import argparse
import os

parser = argparse.ArgumentParser(
    description='Notify plex server to add a file/folder.')
parser.add_argument('-l', '--library', type=str, required=True, help='the plex library index/name.')
parser.add_argument('-f', '--filepath', type=str, required=True, help='the file/foler path to add.')
parser.add_argument( '-s', '--plex', type=str, required=True,
    help='the plex server url, ex: http://plex.server.ip:32400')
parser.add_argument( '-t', '--token', type=str, required=True,
    help=
    'the plex auth token, ref: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/'
)

ARGS = parser.parse_args()
ARGS.filepath = os.path.expanduser(ARGS.filepath)

plex = PlexServer(ARGS.plex, ARGS.token)

if plex:
    if ARGS.library.isnumeric():
        lib = plex.library.sections()[int(ARGS.library)]
    else:
        lib = plex.library.section(ARGS.library)

    if lib:
        lib.update(path=ARGS.filepath)
    else:
        print("Can't find the library section: " + ARGS.library)
else:
    print("Can't connect to the PLEX server. " + ARGS.plex)
