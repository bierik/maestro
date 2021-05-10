FROM alpine:3.12

RUN addgroup --system pdflatex \
     && adduser --system --ingroup pdflatex pdflatex

RUN apk add --no-cache --repository /packages \
    texlive \
    texmf-dist-latexextra \
    py3-aiohttp

COPY ./docker/pdflatex/texmf-local /texmf-local/

RUN /usr/bin/texhash && \
    export PERL5LIB=/usr/share/texmf-dist/tlpkg && \
    echo 'y' | /usr/bin/updmap-sys --syncwithtrees && \
    /usr/bin/updmap-sys --enable Map ma1.map

ENV PYTHONUNBUFFERED 1
WORKDIR /app
USER pdflatex

EXPOSE 8080

COPY ./docker/pdflatex/pdflatex.py .
CMD ["python3", "pdflatex.py"]
