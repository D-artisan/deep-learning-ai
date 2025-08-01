# MCP OpenAI Response

As of the **2025-03-26** version of the **MCP (Mesh Control Protocol)** specification, the following **transport protocols** are supported:

### Supported Transport Protocols

1. **HTTP/2**
2. **HTTP/3 (QUIC-based)**
3. **gRPC**  
   (which typically runs over HTTP/2, but is listed separately in the spec)

4. **Unix Domain Sockets**  
   (for intra-node communication, typically using HTTP/2 framing)

---

### Summary Table

| Transport Protocol     | Notes                                                           |
|-----------------------|-----------------------------------------------------------------|
| HTTP/2                | Widely used; baseline for MCP communication                     |
| HTTP/3 (QUIC)         | Added in recent versions; provides lower latency, better mobility|
| gRPC                  | Protobuf/streaming protocol—usually over HTTP/2                 |
| Unix Domain Sockets   | For local (same-host) communication between components          |

---

### Not Supported

- **Raw TCP** (without HTTP/2 framing) is **not supported**
- **WebSockets** are **not officially supported** as a transport in the current MCP spec

---

**Reference:** These details are based on the official [MCP specification](https://github.com/istio/api/blob/master/mcp/v1alpha1/mcp.proto) and associated changelogs up to March 2025.

If you need information about any *experimental* transports or more context (such as security protocols), please specify!
