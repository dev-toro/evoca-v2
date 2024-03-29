

import os
from django.contrib.gis.utils import LayerMapping
from .models import VeredasColombia

veredascol_mapping = {
    'dptompio' : 'DPTOMPIO',
    'codigo_ver' : 'CODIGO_VER',
    'nom_dep' : 'NOM_DEP',
    'nomb_mpio' : 'NOMB_MPIO',
    'nombre_ver' : 'NOMBRE_VER',
    'vigencia' : 'VIGENCIA',
    'fuente' : 'FUENTE',
    'descripcio' : 'DESCRIPCIO',
    'seudonimos' : 'SEUDONIMOS',
    'area_ha' : 'AREA_HA',
    'cod_dpto' : 'COD_DPTO',
    'shape_area' : 'SHAPE_AREA',
    'shape_len' : 'SHAPE_LEN',
    'geom' : 'MULTIPOLYGON',
}


veredasCOL_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'veredas.shp'),
)


def run(verbose=True):
    lm = LayerMapping(
        VeredasColombia, veredasCOL_shp, veredascol_mapping,
        transform=False, encoding='UTF-8',
    )
    lm.save(strict=True, verbose=verbose)
