FROM fedora:28

ADD . /usr/src/yuwenmao/iface

RUN dnf install -y python3-virtualenv gcc && \
    virtualenv-3 /usr/src/yuwenmao/iface/venv && \
    source /usr/src/yuwenmao/iface/venv/bin/activate && \
    pip install jieba && \
    pip install flask && \
    pip install uwsgi

WORKDIR /

LABEL io.k8s.display-name="YuWenMao Iface"

ADD ./image/entrypoint.sh /

ENTRYPOINT ["./entrypoint.sh"]
