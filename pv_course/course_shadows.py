"""Small CPU shadow investigation driven by notebook parameters; exports the displayed scene for the course website."""
from pathlib import Path
import json
import html
import numpy as np
import pandas as pd
import geopandas as gpd
import pvlib
import shapely
from shapely.ops import triangulate
from .poa_calculation import get_timezone
import math
from shapely.geometry import Polygon, box
from shapely.affinity import translate
from shapely.ops import unary_union

def sweep(poly, dx, dy):
    """Union of all translations of an extruded footprint along a segment."""
    parts=[poly,translate(poly,dx,dy)]
    for ring in [poly.exterior,*poly.interiors]:
        coords=list(ring.coords)
        for a,b in zip(coords,coords[1:]):
            face=Polygon([a,b,(b[0]+dx,b[1]+dy),(a[0]+dx,a[1]+dy)])
            if face.area>1e-9: parts.append(face)
    return unary_union(parts)

def roof_shadow(target, height, obstacles, altitude, azimuth):
    if altitude <= 0: return None, []
    u=-math.sin(math.radians(azimuth))/math.tan(math.radians(altitude))
    v=-math.cos(math.radians(azimuth))/math.tan(math.radians(altitude))
    shadows=[]; contributors=[]
    for i,p,h in obstacles:
        if h <= height: continue
        dx,dy=(h-height)*u,(h-height)*v
        x0,y0,x1,y1=p.bounds
        envelope=box(min(x0,x0+dx),min(y0,y0+dy),max(x1,x1+dx),max(y1,y1+dy))
        if not envelope.intersects(target): continue
        cast=sweep(p,dx,dy).intersection(target)
        if cast.area>1e-7: shadows.append(cast);contributors.append(i)
    return unary_union(shadows),contributors

def paths(geom):
    if geom.is_empty:return []
    polygons=[geom] if geom.geom_type=='Polygon' else [g for g in geom.geoms if g.geom_type=='Polygon']
    return [[[ [round(x,2),round(y,2)] for x,y in ring.coords] for ring in [p.exterior,*p.interiors]] for p in polygons]

def triangles(polygons,z,cx,cy):
 result=[]
 for rings in polygons:
  poly=Polygon(rings[0],rings[1:])
  if not poly.is_valid: poly=poly.buffer(0)
  if poly.is_empty:continue
  def tessellate(piece, level=0):
   if piece.is_empty or piece.area<1e-8:return []
   if piece.geom_type!='Polygon':
    return [t for q in getattr(piece,'geoms',[]) if q.geom_type in ['Polygon','MultiPolygon'] for t in tessellate(q,level)]
   if len(piece.exterior.coords)==4 and not piece.interiors:return [piece]
   if level>12:raise RuntimeError('Triangulation did not converge')
   return [t for tri in triangulate(piece) for t in tessellate(tri.intersection(piece),level+1)]
  ts=tessellate(poly)
  covered=sum(t.area for t in ts)
  for t in ts:
   coords=list(t.exterior.coords)[:3]
   result.append([round(v,3) for x,y in coords for v in (x-cx,y-cy,z)])
  assert abs(covered-poly.area)<max(.5,poly.area*1e-3),(covered,poly.area)
 return result

def area_only(g):
    if g.geom_type == 'Polygon': return g
    if g.geom_type in ['MultiPolygon', 'GeometryCollection']:
        return unary_union([area_only(p) for p in g.geoms
                            if p.geom_type in ['Polygon', 'MultiPolygon', 'GeometryCollection']])
    return Polygon()


def build_shadow_scene(buildings, date, center_id=None, radius_m=80, step_minutes=30):
    if not 30 <= radius_m <= 120:
        raise ValueError('Set the neighborhood radius to 30–120 m to keep the calculation manageable on a lightweight computer.')
    if step_minutes not in (15,30,60):
        raise ValueError('Choose a time step of 15, 30, or 60 minutes.')
    if buildings.crs is None or 'height' not in buildings:
        raise ValueError('Building data require a coordinate reference system and a height field.')
    height=pd.to_numeric(buildings.height, errors='coerce')
    keep=np.isfinite(height)&height.gt(0)&buildings.is_valid&~buildings.is_empty
    b=buildings.loc[keep].copy()
    b['height']=height.loc[keep]
    b=b.loc[~b.geometry.normalize().to_wkb().duplicated()].reset_index(drop=True)
    if b.empty: raise ValueError('No valid buildings are available for the shadow scene.')
    b=b.to_crs(b.estimate_utm_crs())
    if center_id is None:
        # A taller building provides an observable shadow in a compact scene.
        center=b.loc[b.height.idxmax()]
    else:
        matches=b[b.building_id.astype(str).eq(str(center_id))]
        if matches.empty: raise ValueError('The building ID was not found or has no valid positive height.')
        center=matches.iloc[0]
    origin=center.geometry.centroid
    location=gpd.GeoSeries([origin],crs=b.crs).to_crs(4326).iloc[0]
    b.geometry=shapely.set_precision(b.geometry.translate(-origin.x,-origin.y).to_numpy(), .001)
    region=box(-radius_m,-radius_m,radius_m,radius_m)
    visible=b[b.intersects(region)].copy().sort_values('height')
    if len(visible)>150:
        raise ValueError('The neighborhood contains more than 150 buildings. Reduce BLOCK_RADIUS_M and try again.')
    ground=area_only(region.difference(unary_union(visible.geometry)))
    obstacles=[(int(i),r.geometry,float(r.height)) for i,r in b.iterrows()]
    receivers={float(h):area_only(unary_union(group.geometry).difference(
        unary_union(visible.loc[visible.height.gt(h)].geometry)).intersection(region))
        for h,group in visible.groupby('height')}
    day=pd.Timestamp(date)
    if day.tz is not None or day != day.normalize():
        raise ValueError('Use YYYY-MM-DD for the date, without a time or time zone.')
    times=pd.date_range(day+pd.Timedelta(hours=6),day+pd.Timedelta(hours=18),
        freq=f'{step_minutes}min',tz=get_timezone(location.y,location.x))
    sun=pvlib.solarposition.get_solarposition(times,location.y,location.x)
    scene=dict(bounds=list(region.bounds), date=str(day.date()),
        center_id=str(center.building_id), excluded_buildings=int((~keep).sum()),
        buildings=[dict(height=float(r.height),shape=paths(r.geometry.intersection(region)))
                   for _,r in visible.iterrows()],frames=[])
    for stamp,solar in sun.iterrows():
        alt,az=float(solar.apparent_elevation),float(solar.azimuth)
        shade,_=roof_shadow(ground,0,obstacles,alt,az)
        if shade is not None:
            shade=area_only(shapely.intersection(area_only(shade),ground,grid_size=.001))
        layers=[]
        if alt>0:
            for height,receiver in receivers.items():
                if receiver.is_empty: continue
                shadow,_=roof_shadow(receiver,height,obstacles,alt,az)
                shadow=area_only(shapely.intersection(area_only(shadow),receiver,grid_size=.001))
                layers.append(dict(height=height,shape=paths(shadow)))
        scene['frames'].append(dict(time=stamp.strftime('%H:%M'),alt=round(alt,2),
            az=round(az,2),ground=[] if shade is None else paths(shade),roofLayers=layers))
    return scene


def scene_mesh(d):
    bounds=d['bounds'];cx=(bounds[0]+bounds[2])/2;cy=(bounds[1]+bounds[3])/2
    static=[]
    x0,y0,x1,y1=bounds
    for t in triangles([[[[x0,y0],[x1,y0],[x1,y1],[x0,y1],[x0,y0]]]],0,cx,cy):static.append([t,0])
    for b in d['buildings']:
     for t in triangles(b['shape'],b['height'],cx,cy):static.append([t,1])
     for rings in b['shape']:
      for ring in rings:
       for a,c in zip(ring,ring[1:]):
        verts=[(a[0]-cx,a[1]-cy,0),(c[0]-cx,c[1]-cy,0),(c[0]-cx,c[1]-cy,b['height']),(a[0]-cx,a[1]-cy,b['height'])]
        for indices in [(0,1,2),(0,2,3)]:static.append([[round(v,3) for i in indices for v in verts[i]],2])
    frames=[]
    for f in d['frames']:
     shade=triangles(f['ground'],.02,cx,cy)
     for layer in f['roofLayers']:shade.extend(triangles(layer['shape'],layer['height']+.02,cx,cy))
     frames.append({'time':f['time'],'alt':f['alt'],'az':f['az'],'triangles':shade})
    out={'static':static,'frames':frames,'span':max(x1-x0,y1-y0),'date':d['date']}
    out["max_height"]=max(b["height"] for b in d["buildings"])
    return out


def display_shadow_scene(scene, city):
    from IPython.display import HTML, display
    mesh=scene_mesh(scene)
    template=(Path(__file__).resolve().parents[1]/'course_assets/shadow_view.html').read_text(encoding='utf-8')
    document=template.replace('__CITY__',html.escape(city)).replace('__DATE__',scene['date'])
    document=document.replace('__DATA__',json.dumps(mesh,separators=(',',':')))
    import hashlib
    output = Path(__file__).resolve().parents[1] / 'result' / 'assessment' / city
    source = Path(__file__).resolve().parents[1] / 'buildings_data' / f'{city}_building.geojson'
    if source.is_file():
        output.mkdir(parents=True, exist_ok=True)
        (output / 'shadow_scene.html').write_text(document, encoding='utf-8')
        (output / 'shadow_scene.json').write_text(json.dumps({
            'date':scene['date'], 'center_id':scene['center_id'],
            'building_sha256':hashlib.sha256(source.read_bytes()).hexdigest()
        }), encoding='utf-8')
    # srcdoc creates a self-contained interactive output, without another site or server.
    display(HTML('<iframe title="Interactive buildings and shadows" sandbox="allow-scripts" '
                 'style="width:100%;height:850px;border:0" srcdoc="'+html.escape(document,quote=True)+'"></iframe>'))
    return mesh
