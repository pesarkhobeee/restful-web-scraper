# restful-web-scraper

### Development Environment

At the very beginning, you have to initiate a virtual environment with this:

```
sudo apt-get install -y python3-venv
python3 -m venv venv
```

And then every time that you want to run it:

```
source venv/bin/activate
python -m pip install -r requirements.txt
```

Then you can test the scraper like `./scraper.py B00K19SD8Q` or look at the options:

```
./scraper.py -h
usage: scraper.py [-h] [--base-url BASE_URL] [--log-level LOG_LEVEL] MovieID

MovieID

positional arguments:
  MovieID               ID of the movie in Amazon store

optional arguments:
  -h, --help            show this help message and exit
  --base-url BASE_URL   The base URL to join with Movie ID
  --log-level LOG_LEVEL
                        Set the logging level. Defaults to WARNING.

```

### Production Environment

For production you can use docker and docker-compose: 

```
docker-compose up -d
```

Then you can check this URL inside of your webbrowser : `http://127.0.0.1:8080/movie/amazon/B00K19SD8Q`
If you faced with an error please refresh the page until you see the right result:

![ScreenShot](https://raw.github.com/pesarkhobeee/restful-web-scraper/master/Screenshot-success.png)

![ScreenShot](https://raw.github.com/pesarkhobeee/restful-web-scraper/master/Screenshot-failure.png)

or you can just check the HTTP status:

```
()[~/lab/justWatch/repo, master+1]: curl  -I  http://127.0.0.1:8080/movie/amazon/B00KY1U7GM
HTTP/1.1 500 INTERNAL SERVER ERROR
Server: gunicorn/20.0.4
Date: Wed, 22 Jul 2020 16:20:17 GMT
Connection: close
Content-Type: application/json
Content-Length: 91

()[~/lab/justWatch/repo, master+1, 1s]: curl  -I  http://127.0.0.1:8080/movie/amazon/B00KY1U7GM
HTTP/1.1 200 OK
Server: gunicorn/20.0.4
Date: Wed, 22 Jul 2020 16:20:25 GMT
Connection: close
Content-Type: application/json
Content-Length: 465

```
