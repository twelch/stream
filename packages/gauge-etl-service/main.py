from arcgis_vector_source import fetch_arcgis_features
import json

def main():
    # Example: Fetch cities from the ArcGIS sample server
    features = fetch_arcgis_features(
        url="https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/Live_Stream_Gauges_v1/FeatureServer/0",
        options={
            "geometryPrecision": 5,
            "supportsPagination": True,
            "outFields": "OBJECTID,stationid,stationurl,stageurl,flowurl,graphurl,org,stage_ft,flow_cfs,status, lastupdate, name, governing_location, lastupdate_age, statusClass, status_full, status_24h, status_48h, status_72h",
            "displayIncompleteFeatureCollections": True
        }
    )
    
    # For demonstration, let's save the fetched data to a file
    with open("gauge.geojson", "w") as f:
        json.dump(features, f)

main()