FROM odoo:17

USER root

RUN pip3 install psycopg2-binary

COPY . /mnt/extra-addons/intern_bridge

USER odoo
