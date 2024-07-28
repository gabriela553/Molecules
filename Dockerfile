FROM python:3.12

WORKDIR /root

COPY requirements.txt ./
ENV PYTHONPATH=/root
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "uvicorn[standard]"

COPY molecules_app /root/molecules_app
#COPY molecules_app/* ./
EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
