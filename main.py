from flask import Flask, render_template, request, send_file

from pytube import YouTube

app = Flask(__name__, template_folder='template')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/auto", methods=['get'])
def auto():
    url = request.args.get('url')
    file_format = request.args.get('format')
    filename = request.args.get('filename')

    yt = YouTube(url)
    if filename.__contains__(" "):
        filename = filename.replace(" ", "_")
    elif filename == "":
        filename = yt.title

    return send_file(f'Downloads\\{filename}{file_format}', as_attachment=True)


@app.route('/', methods=['POST'])
def my_form_post():
    filename = request.form['filename']
    url = request.form['url']
    file_format = request.form['format']

    print(f"[+] Filename: {filename}")
    print(f"[+] URL: {url}")
    print(f"[+] Format: {file_format}")

    yt = YouTube(url)

    if filename == "":
        filename = yt.title
    elif filename == " ":
        filename = yt.title

    if file_format == '.mp4':
        print("[+] Video found")
        print("[+] Starting download")

        yt.streams.filter().get_highest_resolution().download(output_path='Downloads/',
                                                              filename=f"{filename}{file_format}")
        print("[+] Converted & Downloaded")

        return send_file(f'Downloads\\{filename}{file_format}', as_attachment=True)
    elif file_format == '.mp3':
        print("[+] Audio found")
        print("[+] Starting download")

        yt.streams.filter(only_audio=True).get_audio_only().download(output_path='Downloads/',
                                                                     filename=f"{filename}{file_format}")
        print("[+] Converted & Downloaded")

        return send_file(f'Downloads\\{filename}{file_format}', as_attachment=True)


if __name__ == "__main__":
    from waitress import serve

    serve(app, port=8080)
