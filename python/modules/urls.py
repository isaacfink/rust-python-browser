import socket
import ssl


class Url:
    def __init__(self, url: str) -> None:
        self.schema, url = url.split("://", 1)
        assert self.schema in ("http", "https"), f"Unsupported schema: {self.schema}"
        if self.schema == "http":
            self.port = 80
        else:
            self.port = 443
        self.host, url = url.split("/", 1)
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
        self.path = "/" + url

    def __str__(self) -> str:
        return f"{self.schema}://{self.host}{self.path}"

    def request(self):
        ssl.create_default_context = ssl._create_unverified_context
        ctx = ssl.create_default_context()

        s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
        s = ctx.wrap_socket(s, server_hostname=self.host)

        s.connect((self.host, self.port))
        s.send(
            f"GET {self.path} HTTP/1.0\r\nHost: {self.host} \r\n\r\n".encode("utf-8")
        )
        response = s.makefile("r", encoding="utf-8", newline="\r\n")
        status_line = response.readline()

        version, status, explanation = status_line.split(" ", 2)

        response_headers = {}

        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers, "Unsupported encoding"
        assert "content-encoding" not in response_headers, "Unsupported encoding"
        body = response.read()
        s.close()
        return body
