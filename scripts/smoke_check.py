"""Offline CPU compatibility check; run with the student's course Python."""
from pathlib import Path
import sys, tempfile, json, platform

def main():
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root))
    print("Checking scientific imports and CPU calculations. First-time imports may take a few minutes.", flush=True)
    import numpy as np
    import pandas as pd
    import scipy
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import geopandas as gpd
    import fiona, pyproj, shapely, pvlib, timezonefinder, contextily
    import nbformat, ipykernel, jupyterlab
    from shapely.geometry import box
    from sklearn.cluster import KMeans
    from sklearn.neural_network import MLPRegressor
    from pv_course.course_shadows import build_shadow_scene, scene_mesh
    from pv_course.course_website import build_website
    times=pd.date_range('2020-06-21 10:00',periods=3,freq='h',tz='Asia/Bangkok')
    sun=pvlib.solarposition.get_solarposition(times,13.7,100.5)
    assert np.isfinite(sun.zenith).all()
    geo=gpd.GeoDataFrame({'building_id':[1,2],'height':[10.,25.]},
        geometry=[box(500000,1500000,500010,1500010),box(500020,1500000,500030,1500010)],crs=32647)
    assert np.allclose(geo.area,100)
    mesh=scene_mesh(build_shadow_scene(geo,'2020-06-21',center_id=1,radius_m=40,step_minutes=60))
    assert len(mesh['frames'])==13 and mesh['static']
    x=np.array([[0.,0.],[.1,.2],[5.,5.],[5.1,5.2]])
    assert len(set(KMeans(2,n_init=2,random_state=42).fit_predict(x)))==2
    model=MLPRegressor(hidden_layer_sizes=(4,),random_state=42,batch_size=4)
    model.partial_fit(x,np.array([0.,.1,1.,1.1]));assert np.isfinite(model.predict(x)).all()
    with tempfile.TemporaryDirectory(prefix='pv course ') as td:
        folder=Path(td)/'data files';folder.mkdir()
        path=folder/'buildings.geojson';geo.to_file(path,driver='GeoJSON')
        assert len(gpd.read_file(path))==2
        fig,ax=plt.subplots();ax.plot([0,1],[0,1]);fig.savefig(folder/'plot.png');plt.close(fig)
        assert (folder/'plot.png').stat().st_size>0
    result={'status':'passed','platform':platform.platform(),'machine':platform.machine(),'python':sys.version.split()[0]}
    print(json.dumps(result))
    return result

if __name__=='__main__':main()
