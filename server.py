from http.server import BaseHTTPRequestHandler
import socketserver
import time
import json
import threading
import selectors
from queue import SynchronizedQueue


PORT        = 8080
NUM_THREADS = 100

MAP = {} # TODO: replace with map class object

if hasattr(selectors, 'PollSelector'):
    _ServerSelector = selectors.PollSelector
else:
    _ServerSelector = selectors.SelectSelector

# TODO: remove when the map api is set
def requestMapUpdate(request):
	print("in requestMapUpdate")
	time.sleep(3)
	return json.dumps({"curr": "Packard Ave", "dir" : "left", "wait_time" : 7})

class GetHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		fields= self.headers.as_string().split('\n')
		output = {}
		for field in fields: 
			kv = field.split(':')
			if len(kv) >= 2:
				output[kv[0]] = kv[1]

		post_body = self.rfile.read(int(output['Content-Length']))
		print(post_body)
		body = json.loads(post_body)
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(bytes(requestMapUpdate(body), "utf-8"))

def consumer(queue_):
	while True:
		httpd = queue_.get()
		httpd.handle_request()

def main():
	queue_ = SynchronizedQueue()
	threads = [threading.Thread(target=consumer, args=[queue_]) for i in range(0, NUM_THREADS)]
	for thread in threads:
		thread.start()

	with socketserver.TCPServer(("", PORT), GetHandler) as httpd:
		with _ServerSelector() as selector:
			selector.register(httpd, selectors.EVENT_READ)

			while True:
				ready = selector.select()
				if ready:
					queue_.put(httpd)

				httpd.service_actions()


if __name__ == '__main__':
	main()