FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install auto-gptq --no-build-isolation --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/

COPY handler.py /

CMD ["python3", "-u", "/handler.py"]