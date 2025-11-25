# 1) Imagem base
FROM python:3.12-slim

# 2) Variável para rodar sem buffer
ENV PYTHONUNBUFFERED=1

# 3) Criar diretório de trabalho
WORKDIR /app

# 4) Copiar dependências
COPY church_project/requirements.txt ./requirements.txt

# 5) Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copiar todo o projeto
COPY . .

# 7) Rodar collectstatic (executado dentro do container)
RUN cd church_project && python manage.py collectstatic --noinput

# 8) Porta onde o Django vai rodar
EXPOSE 8000

# 9) Start (gunicorn)
CMD ["bash", "-c", "cd church_project && gunicorn church_site.wsgi:application --bind 0.0.0.0:8000"]