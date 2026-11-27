FROM python:3.13-slim

RUN useradd --create-home seo
WORKDIR /app
COPY --chown=seo:seo requirements.txt /app/
COPY --chown=seo:seo scripts /app/scripts
COPY --chown=seo:seo skills /app/skills
COPY --chown=seo:seo extensions /app/extensions
USER seo
ENV AGENTIC_HARNESS_SEO_DATA_DIR=/home/seo/runtime
RUN bash scripts/agentic-harness-seo setup --skip-browser
EXPOSE 8000
CMD ["bash", "scripts/agentic-harness-seo", "run", "seo_mcp.py", "--transport", "streamable-http", "--host", "0.0.0.0"]
