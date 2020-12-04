from src import music_server

if __name__ == "__main__":
    args = music_server.parse_args()
    if args.http:
        music_server.app.run()
    else:
        music_server.process_file(args.input)
