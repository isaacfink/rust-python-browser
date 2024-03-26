use std::io::{BufRead, BufReader, Write};
use std::net::TcpStream;

pub struct Url {
    schema: String,
    host: String,
    port: usize,
    path: String,
}

impl Url {
    fn new(url: &str) -> Self {
        let (schema, url) = url
            .split_once("://")
            .expect(&format!("Invalid Url, {}", url));
        assert!(
            matches!(schema, "http" | "https"),
            "Unsupported schema: {}",
            schema
        );
        let port: usize = if schema == "http" { 80 } else { 443 };
        let (host_port, path) = url.split_once("/").unwrap_or((url, ""));
        let path = format!("/{}", path);
        let (host, port_str) = match host_port.split_once(":") {
            Some((host, port_str)) => (
                host.to_string(),
                port_str
                    .parse()
                    .expect(&format!("Invalid port: {}", port_str)),
            ),
            None => (host.to_string(), port),
        };

        Self {
            schema: schema.to_string(),
            host,
            port,
            path,
        }
    }

    fn request(&self) -> std::io::Result<String> {
        let mut stream = TcpStream::connect(format!("{}:{}", self.host, self.port))?;
        let request = format!("GET {} HTTP/1.0\r\nHost: {}\r\n\r\n", self.path, self.host);

        stream.write_all(request.as_bytes())?;

        let mut reader = BufReader::new(stream);
        let mut response = String::new();
        reader.read_line(&mut response)?;

        Ok(response)
    }
}
