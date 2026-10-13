"""Export course CSV results as a self-contained offline website."""
from pathlib import Path
from datetime import datetime
import json
import math
import hashlib
import geopandas as gpd
from .building_pv_potential import audit_buildings
import pandas as pd

def assessment_details(root, folder, monthly):
    meta = json.loads((folder / "forecast_input.json").read_text(encoding="utf-8"))
    source = root / "buildings_data" / f"{folder.name}_building.geojson"
    if hashlib.sha256(source.read_bytes()).hexdigest() != meta["source_sha256"][source.name]:
        raise ValueError(f"{folder.name} building data have changed. Rerun the guided practical before exporting the website.")
    buildings, _ = audit_buildings(gpd.read_file(source))
    if "building_id" not in buildings:
        buildings["building_id"] = buildings.index
    values = pd.read_csv(folder / "building_energy.csv", dtype={"building_id": str})
    if "building_id" not in values:
        if len(values) != len(buildings):
            raise ValueError("Building geometry and result counts differ. Rerun the assessment cells in PV_Practical.ipynb, then export the website again.")
        values["building_id"] = buildings.building_id.astype(str).to_numpy()
    buildings["building_id"] = buildings.building_id.astype(str)
    local = buildings.to_crs(buildings.estimate_utm_crs())
    local = local[["building_id", "geometry"]].merge(values, on="building_id", validate="one_to_one")
    if len(local) != len(buildings):
        raise ValueError("Building IDs do not match the assessment records. Rerun the assessment cells in PV_Practical.ipynb, then export the website again.")
    x0, y0, x1, y1 = local.total_bounds
    features = []
    for _, row in local.iterrows():
        polys = [row.geometry] if row.geometry.geom_type == "Polygon" else row.geometry.geoms
        rings = [[[ [round(x-x0, 2), round(y1-y, 2)] for x, y in ring.coords]
                  for ring in [poly.exterior, *poly.interiors]] for poly in polys]
        features.append(dict(id=row.building_id, shape=rings, area=float(row.roof_area),
                             usable=float(row.usable_area), energy=float(row.annual_energy)))
    shadow = folder / "shadow_scene.html"
    shadow_meta = folder / "shadow_scene.json"
    shadow_html = None
    if shadow.is_file() and shadow_meta.is_file():
        saved = json.loads(shadow_meta.read_text(encoding="utf-8"))
        if saved.get("building_sha256") == meta["source_sha256"][source.name]:
            shadow_html = shadow.read_text(encoding="utf-8")
    return dict(buildings=features, bounds=[float(x1-x0), float(y1-y0)],
        meta={k:meta[k] for k in ["module_area_m2", "roof_fraction", "surface_tilt", "surface_azimuth", "timezone"]},
        shadow=shadow_html)

def build_website(root=None):
    root = Path(root or Path(__file__).resolve().parents[1]).resolve()
    cities = []
    for folder in sorted((root / "result/assessment").glob("*")):
        if not (folder / "assessment_summary.csv").is_file():
            continue
        summary = pd.read_csv(folder / "assessment_summary.csv").to_dict("records")
        monthly = {}
        meta = json.loads((folder / "forecast_input.json").read_text(encoding="utf-8"))
        for system in ("fixed", "tracking"):
            frame = pd.read_csv(folder / f"power_{system}.csv")
            # Course exports contain 10-minute mean power; sum observed energy.
            times = pd.to_datetime(frame.iloc[:, 0])
            energy = pd.Series(frame["power"].to_numpy() * meta["step_minutes"] / 60000, index=times)
            monthly[system] = energy.groupby(times.dt.month.to_numpy()).sum(min_count=1).reindex(range(1,13)).tolist()
        cities.append({"name": folder.name, "summary": summary, "monthly": monthly,
                       **assessment_details(root, folder, monthly)})
    if not cities:
        raise ValueError("Run the guided practical first to generate assessment results in result/assessment.")
    def clean(value):
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items()}
        if isinstance(value, list):
            return [clean(v) for v in value]
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return value
    payload = json.dumps(clean({"generated": datetime.now().astimezone().isoformat(timespec="seconds"),
                                "cities": cities}), ensure_ascii=False, allow_nan=False)
    payload = payload.replace("<", "\\u003c")
    template = (root / "course_assets/results_site.html").read_text(encoding="utf-8")
    output = root / "result/course_website.html"
    output.write_text(template.replace("__COURSE_DATA__", payload), encoding="utf-8")
    return output

if __name__ == "__main__":
    print(build_website())
