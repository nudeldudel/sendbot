FROM python:slim

WORKDIR /usr/local/bin

RUN pip install deltachat deltachat_rpc_client aiosmtpd
RUN curl https://sh.rustup.rs -sSf | sh

COPY send* .

CMD ["python","sendbot.py"]
