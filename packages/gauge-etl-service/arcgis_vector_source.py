import requests
from urllib.parse import urlencode
from typing import Dict, Any, Optional

def fetch_arcgis_features(url: str, options: Optional[Dict[str, Any]] = None) -> Dict:
    """
    Fetch features from an ArcGIS REST Service Feature Layer as GeoJSON

    Args:
        url (str): Base url for an ArcGIS Server Feature Layer. Should end in /MapServer/0..n
        options (dict, optional): Configuration options for the source
    
    Returns:
        Dict: A GeoJSON FeatureCollection containing all fetched features
    """
    options = options or {}
    
    # Default properties
    data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Configure options with defaults
    out_fields = options.get("outFields", "*")
    supports_pagination = options.get("supportsPagination", True)
    display_incomplete_collections = options.get("displayIncompleteFeatureCollections", True)
    geometry_precision = options.get("geometryPrecision", 6)
    
    # Continue fetching until we have all data
    continue_fetching = True
    
    while continue_fetching:
        params = {
            "inSR": "4326",
            "outSR": "4326",
            "where": "1>0",
            "outFields": out_fields,
            "returnGeometry": "true",
            "geometryPrecision": str(geometry_precision),
            "returnIdsOnly": "false",
            "f": "geojson"
        }
        
        # Add pagination parameter if supported
        if supports_pagination:
            params["resultOffset"] = str(len(data["features"]))
        
        query_url = f"{url}/query?{urlencode(params)}"
        print(query_url)
        
        try:
            response = requests.get(query_url)
            response.raise_for_status()
            feature_collection = response.json()
            
            if "error" in feature_collection:
                if supports_pagination and "pagination" in feature_collection["error"]["message"].lower():
                    supports_pagination = False
                    # Continue in the next loop iteration with updated settings
                    continue
                else:
                    raise Exception(f"Error retrieving feature data: {feature_collection['error']['message']}")
            else:
                # Add features to our collection
                data["features"].extend(feature_collection["features"])
                
                # Check if there are more features to fetch
                if "properties" in feature_collection and feature_collection['properties'].get('exceededTransferLimit', False) == True:
                    if not supports_pagination:
                        raise Exception("Data source does not support pagination but exceeds transfer limit")
                    else:
                        if display_incomplete_collections:
                            # In a real application, you'd update the map here
                            print(f"Fetched {len(feature_collection['features'])} features. Total so far: {len(data['features'])}")
                        
                        # Continue fetching more data in the next loop iteration
                        continue_fetching = True
                else:
                    # All data has been fetched
                    print(f"Finished fetching all {len(data['features'])} features")
                    continue_fetching = False
        
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            continue_fetching = False
    
    return data