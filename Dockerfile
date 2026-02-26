FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && rm -rf /var/lib/apt/lists/*

# Install torch with CUDA support first
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu124

# Install remaining dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

ENV HF_HOME=/runpod-volume

COPY handler.py /handler.py

CMD ["python", "-u", "/handler.py"]
