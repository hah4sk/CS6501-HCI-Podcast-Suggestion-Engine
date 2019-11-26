import base64

def _encode(st):
	return base64.b64encode(st.encode("utf-8"))

def _decode(enc):
	return base64.b64decode(enc.decode("utf-8"))

def praw_keys():
	return [_decode(item) for item in [b'OHhxRUlMZzB3QkhEYlE=', b'MDJScWotOF9oaHJ3cUF4eFJRTjdPWUN6Uzdj', b'UG9kY2F0cw==']]


