FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV NHVR_MCP_TRANSPORT=stdio
ENV NHVR_MCP_PORT=8080

COPY pyproject.toml README.md /app/
COPY nhvrcontrib /app/nhvrcontrib

RUN useradd --create-home --system nhvr \
    && python -m pip install --no-cache-dir -e ".[mcp]" \
    && chown -R nhvr:nhvr /app

USER nhvr

EXPOSE 8080

CMD ["python", "-m", "nhvrcontrib.server"]
