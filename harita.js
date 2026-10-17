// harita.js
const EGE_CONFIG = {
    bounds: [[36.40, 26.50], [40.10, 30.70]],
    minZoom: 7,
    maxZoom: 14
};

function initEgeMapBoundaries(mapInstance) {
    if (!mapInstance) return;

    const egeBounds = L.latLngBounds(EGE_CONFIG.bounds[0], EGE_CONFIG.bounds[1]);
    mapInstance.setMaxBounds(egeBounds);
    mapInstance.setMinZoom(EGE_CONFIG.minZoom);
    mapInstance.options.maxBoundsViscosity = 1.0;

    // Ege dışını karartan / maskeleyen CSS / SVG katmanı eklentisi
    console.log("harita.js başarıyla yüklendi, Ege sınırları kilitlendi.");
}
