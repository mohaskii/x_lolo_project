import gzip
import zlib
import brotli
import zstandard
def decode_response(response):
    encoding = response.headers.get('Content-Encoding', '')
    if 'gzip' in encoding:
        return gzip.decompress(response.content)
    elif 'deflate' in encoding:
        return zlib.decompress(response.content)
    elif 'br' in encoding:
        return brotli.decompress(response.content)
    elif 'zstd' in encoding:
        return zstandard.decompress(response.content)
    return response.content
