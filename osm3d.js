const czml = ""; 
const viewer = new Cesium.Viewer("cesiumContainer", { terrain: Cesium.Terrain.fromWorldTerrain(), });
var osm = new Cesium.OpenStreetMapImageryProvider({ url : 'https://tile.openstreetmap.org' }); viewer.imageryLayers.addImageryProvider(osm); 
viewer.scene.globe.enableLighting = true;

try {
  const tileset = await Cesium.Cesium3DTileset.fromIonAssetId(<add your asset id>);
  viewer.scene.primitives.add(tileset);
} catch (error) {
  console.log(`Error loading tileset: ${error}`);
}

const dataSourcePromise = Cesium.CzmlDataSource.load("https://raw.githubusercontent.com/hcarter333/rm-rbn-history/refs/heads/main/maps/2024_12_27_US_4571_trying_new_camera_and_counterpoise.czml"); 
viewer.dataSources.add(dataSourcePromise);
