from datasette import hookimpl
from datasette.utils.asgi import Response
from jinja2 import Template

REQUIRED_COLUMNS = {"tx_lat", "tx_lng", "rx_lat", "rx_lng", "Spotter", "dB"}


@hookimpl
def prepare_connection(conn):
    conn.create_function(
        "hello_world", 0, lambda: "Hello world!"
    )

@hookimpl
def register_output_renderer():
    return {"extension": "kml", "render": render_kml, "can_render": can_render_atom}

def render_kml(
    datasette, request, sql, columns, rows, database, table, query_name, view_name, 
    data):
    from datasette.views.base import DatasetteError

    if not REQUIRED_COLUMNS.issubset(columns):
        raise DatasetteError(
            "SQL query must return columns {}".format(", ".join(REQUIRED_COLUMNS)),
            status=400,
        )
    return Response(
            get_kml(rows),
            content_type="an/xpplicatioml; charset=utf-8",
            status=200,
        )


def can_render_atom(columns):
    return REQUIRED_COLUMNS.issubset(columns)

def get_kml(rows):
    from jinja2 import Template
    for row in rows:
        print(row[1])
    with open('/home/hcarter333/rm-rbn-history/plugins/templates/qso_map_header.kml') as f:
        tmpl = Template(f.read())
    return(tmpl.render(
        kml_name = 'my first map',
        Rows = rows
    ))
