from datasette import hookimpl
from datasette.utils.asgi import Response
from jinja2 import Template

signal_colors = {"1": "#ff004b96",
                 "0": "#ff004b96",
                 "2": "#ff0000ff",
                 "3": "#ff00a5ff",
                 "4": "#ff00ffff",
                 "5": "#ff00ff00",
                 "6": "#ffff0000",
                 "7": "#ff82004b",
                 "8": "#ffff007f",
                 "9": "#ffffffff",
                 }

def db_to_s(db):
    test_db = int(db)
    if(test_db > 32):
        return "9"
    if(test_db > 27):
        return "8"
    if(test_db > 21):
        return "7"
    if(test_db > 15):
        return "6"
    if(test_db > 8):
        return "5"
    if(test_db > 2):
        return "4"
    if(test_db >= 1):
        return "3"
    return "0"



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
    #print(datasette.plugin_config)
    if not REQUIRED_COLUMNS.issubset(columns):
        raise DatasetteError(
            "SQL query must return columns {}".format(", ".join(REQUIRED_COLUMNS)),
            status=400,
        )
    return Response(
            get_kml(rows),
            content_type="application/vnd.google-earth.kml+xml; charset=utf-8",
            status=200,
        )


def can_render_atom(columns):
    return REQUIRED_COLUMNS.issubset(columns)

def line_color(rst):
    if(len(str(rst)) == 3):
        return signal_colors[str(rst)[1]] 
    else:
        return signal_colors[db_to_s(rst)]

def is_qso(rst):
    if(len(str(rst)) == 3):
        return True
    else:
        return False

def get_kml(rows):
    from jinja2 import Template

    for row in rows:
        print(row[1])
    with open('./plugins/templates/qso_map_header.kml') as f:
        tmpl = Template(f.read())
        tmpl.globals['line_color'] = line_color
        tmpl.globals['is_qso'] = is_qso
    return(tmpl.render(
        kml_name = 'my first map',
        Rows = rows
    ))
