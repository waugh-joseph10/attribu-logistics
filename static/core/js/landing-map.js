// Mapbox GL route visualization.
// Public browser token. Restrict allowed URLs and scopes in Mapbox.
(function () {
  const configElement = document.getElementById('landing-config');
  const landingConfig = configElement ? JSON.parse(configElement.textContent) : {};

  if (!window.mapboxgl) return;

  mapboxgl.accessToken = landingConfig.mapboxToken || '';

  const METROS = [
    {
      center: [-112.190, 33.490], zoom: 10.2, pitch: 45, bearing: -17.6,
      routePaneShift: 0,
      stops: [
        { coords: [-112.074, 33.448], name: 'Shop' },
        { coords: [-112.074, 33.508], name: 'Stop 1' },
        { coords: [-112.010, 33.512], name: 'Stop 2' },
        { coords: [-111.926, 33.620], name: 'Stop 3' },
        { coords: [-111.890, 33.580], name: 'Stop 4' },
        { coords: [-111.934, 33.425], name: 'Stop 5' },
        { coords: [-111.980, 33.392], name: 'Stop 6' },
      ],
      wasteCoords: [
        [-112.074, 33.448], [-111.926, 33.620], [-112.074, 33.508],
        [-111.934, 33.425], [-112.010, 33.512], [-111.980, 33.392],
        [-111.890, 33.580], [-112.042, 33.405], [-112.074, 33.448],
      ],
    },
    {
      center: [-118.320, 33.940], zoom: 10.0, pitch: 45, bearing: -12.0,
      routePaneShift: 170,
      stops: [
        { coords: [-118.243, 34.052], name: 'Shop' },
        { coords: [-118.347, 34.093], name: 'Stop 1' },
        { coords: [-118.491, 34.021], name: 'Stop 2' },
        { coords: [-118.396, 33.987], name: 'Stop 3' },
        { coords: [-118.315, 33.865], name: 'Stop 4' },
        { coords: [-118.189, 33.770], name: 'Stop 5' },
        { coords: [-118.113, 33.920], name: 'Stop 6' },
      ],
      wasteCoords: [
        [-118.243, 34.052], [-118.189, 33.770], [-118.491, 34.021],
        [-118.315, 33.865], [-118.347, 34.093], [-118.113, 33.920],
        [-118.396, 33.987], [-118.180, 34.005], [-118.243, 34.052],
      ],
    },
    {
      center: [-97.000, 32.860], zoom: 9.8, pitch: 45, bearing: 8.0,
      routePaneShift: 170,
      stops: [
        { coords: [-96.797, 32.776], name: 'Shop' },
        { coords: [-96.825, 32.870], name: 'Stop 1' },
        { coords: [-96.757, 33.019], name: 'Stop 2' },
        { coords: [-96.664, 33.104], name: 'Stop 3' },
        { coords: [-96.940, 32.810], name: 'Stop 4' },
        { coords: [-97.110, 32.740], name: 'Stop 5' },
        { coords: [-97.330, 32.755], name: 'Stop 6' },
      ],
      wasteCoords: [
        [-96.797, 32.776], [-97.330, 32.755], [-96.757, 33.019],
        [-96.940, 32.810], [-96.664, 33.104], [-96.900, 32.640],
        [-96.825, 32.870], [-97.110, 32.740], [-96.797, 32.776],
      ],
    },
    {
      center: [-87.690, 41.870], zoom: 10.5, pitch: 45, bearing: -5.0,
      routePaneShift: 170,
      stops: [
        { coords: [-87.629, 41.878], name: 'Shop' },
        { coords: [-87.648, 41.926], name: 'Stop 1' },
        { coords: [-87.680, 42.019], name: 'Stop 2' },
        { coords: [-87.750, 41.980], name: 'Stop 3' },
        { coords: [-87.790, 41.877], name: 'Stop 4' },
        { coords: [-87.715, 41.760], name: 'Stop 5' },
        { coords: [-87.630, 41.710], name: 'Stop 6' },
      ],
      wasteCoords: [
        [-87.629, 41.878], [-87.630, 41.710], [-87.680, 42.019],
        [-87.715, 41.760], [-87.750, 41.980], [-87.560, 41.835],
        [-87.790, 41.877], [-87.648, 41.926], [-87.629, 41.878],
      ],
    },
    {
      center: [-77.080, 38.930], zoom: 10.8, pitch: 45, bearing: -22.0,
      routePaneShift: 170,
      stops: [
        { coords: [-77.036, 38.907], name: 'Shop' },
        { coords: [-77.046, 38.961], name: 'Stop 1' },
        { coords: [-77.094, 38.984], name: 'Stop 2' },
        { coords: [-77.147, 39.084], name: 'Stop 3' },
        { coords: [-77.047, 38.803], name: 'Stop 4' },
        { coords: [-77.188, 38.868], name: 'Stop 5' },
        { coords: [-77.026, 38.993], name: 'Stop 6' },
      ],
      wasteCoords: [
        [-77.036, 38.907], [-77.147, 39.084], [-77.047, 38.803],
        [-76.876, 38.998], [-77.094, 38.984], [-77.188, 38.868],
        [-77.046, 38.961], [-77.026, 38.993], [-77.036, 38.907],
      ],
    },
    {
      center: [-80.220, 25.870], zoom: 10.8, pitch: 45, bearing: 5.0,
      routePaneShift: 170,
      stops: [
        { coords: [-80.191, 25.761], name: 'Shop' },
        { coords: [-80.252, 25.720], name: 'Stop 1' },
        { coords: [-80.302, 25.776], name: 'Stop 2' },
        { coords: [-80.338, 25.827], name: 'Stop 3' },
        { coords: [-80.240, 25.886], name: 'Stop 4' },
        { coords: [-80.166, 25.932], name: 'Stop 5' },
        { coords: [-80.139, 25.974], name: 'Stop 6' },
      ],
      wasteCoords: [
        [-80.191, 25.761], [-80.139, 25.974], [-80.338, 25.827],
        [-80.166, 25.932], [-80.252, 25.720], [-80.240, 25.886],
        [-80.302, 25.776], [-80.181, 25.847], [-80.191, 25.761],
      ],
    },
  ];

  const metro = METROS[0];

  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v11',
    center: metro.center,
    zoom: metro.zoom,
    pitch: metro.pitch,
    bearing: metro.bearing,
    interactive: false,
    attributionControl: false,
  });

  map.addControl(new mapboxgl.AttributionControl({ compact: true }), 'bottom-right');

  const stops = metro.stops;
  const routeCoordinates = stops.map(s => s.coords);
  let optimizedRouteCoordinates = routeCoordinates;

  function shiftCenterTowardCopy(center, pixels) {
    if (!pixels) return center;

    const point = map.project(center);
    point.x -= pixels;
    return map.unproject(point).toArray();
  }

  function lineFeature(coordinates) {
    return {
      type: 'Feature',
      properties: {},
      geometry: { type: 'LineString', coordinates },
    };
  }

  function pointFeature(coordinates) {
    return {
      type: 'Feature',
      properties: {},
      geometry: { type: 'Point', coordinates },
    };
  }

  async function getDrivingRoute(coordinates) {
    if (!mapboxgl.accessToken) return coordinates;

    const waypointString = coordinates.map(coord => coord.join(',')).join(';');
    const url = new URL(`https://api.mapbox.com/directions/v5/mapbox/driving-traffic/${waypointString}`);
    url.search = new URLSearchParams({
      access_token: mapboxgl.accessToken,
      alternatives: 'false',
      geometries: 'geojson',
      overview: 'full',
      steps: 'false',
    }).toString();

    try {
      const response = await fetch(url);
      if (!response.ok) return coordinates;

      const data = await response.json();
      return data.routes?.[0]?.geometry?.coordinates || coordinates;
    } catch {
      return coordinates;
    }
  }

  function distanceBetween(a, b) {
    const lon = b[0] - a[0];
    const lat = b[1] - a[1];
    return Math.sqrt(lon * lon + lat * lat);
  }

  function interpolateRoute(coordinates, progress) {
    if (coordinates.length < 2) return coordinates[0] || routeCoordinates[0];

    const segmentLengths = [];
    let totalLength = 0;

    for (let i = 0; i < coordinates.length - 1; i++) {
      const length = distanceBetween(coordinates[i], coordinates[i + 1]);
      segmentLengths.push(length);
      totalLength += length;
    }

    let distance = (progress % 1) * totalLength;
    for (let i = 0; i < segmentLengths.length; i++) {
      if (distance > segmentLengths[i]) {
        distance -= segmentLengths[i];
        continue;
      }

      const start = coordinates[i];
      const end = coordinates[i + 1];
      const localProgress = segmentLengths[i] === 0 ? 0 : distance / segmentLengths[i];
      return [
        start[0] + (end[0] - start[0]) * localProgress,
        start[1] + (end[1] - start[1]) * localProgress,
      ];
    }

    return coordinates[coordinates.length - 1];
  }

  const wasteCoordinates = metro.wasteCoords;
  const drivingRoutesPromise = Promise.all([
    getDrivingRoute(routeCoordinates),
    getDrivingRoute(wasteCoordinates),
  ]);

  const stopsGeoJSON = {
    type: 'FeatureCollection',
    features: stops.map((stop, i) => ({
      type: 'Feature',
      properties: {
        order: i,
        kind: i === 0 ? 'depot' : 'stop',
        label: i === 0 ? 'BASE' : String(i),
      },
      geometry: { type: 'Point', coordinates: stop.coords },
    })),
  };

  map.on('load', async () => {
    const framedCenter = shiftCenterTowardCopy(metro.center, metro.routePaneShift);
    if (metro.routePaneShift) map.jumpTo({ center: framedCenter });

    const [optimizedDrivingRoute, wasteDrivingRoute] = await drivingRoutesPromise;
    optimizedRouteCoordinates = optimizedDrivingRoute;

    map.addSource('route-waste', {
      type: 'geojson',
      data: lineFeature(wasteDrivingRoute),
    });

    map.addSource('route', {
      type: 'geojson',
      lineMetrics: true,
      data: lineFeature(optimizedDrivingRoute),
    });

    map.addSource('route-scout', {
      type: 'geojson',
      data: pointFeature(optimizedDrivingRoute[0]),
    });

    map.addSource('stops', { type: 'geojson', data: stopsGeoJSON });

    const lineLayout = { 'line-join': 'round', 'line-cap': 'round' };

    map.addLayer({
      id: 'route-waste',
      type: 'line',
      source: 'route-waste',
      layout: lineLayout,
      paint: {
        'line-color': '#6b7280',
        'line-width': 2,
        'line-opacity': 0.35,
        'line-dasharray': [0, 2, 2],
      },
    });

    map.addLayer({
      id: 'route-casing',
      type: 'line',
      source: 'route',
      layout: lineLayout,
      paint: {
        'line-color': '#0a0c10',
        'line-width': 14,
        'line-opacity': 0.92,
        'line-blur': 1,
      },
    });

    map.addLayer({
      id: 'route-glow',
      type: 'line',
      source: 'route',
      layout: lineLayout,
      paint: {
        'line-color': '#00DCA0',
        'line-width': 10,
        'line-opacity': 0.22,
        'line-blur': 5,
      },
    });

    map.addLayer({
      id: 'route',
      type: 'line',
      source: 'route',
      layout: lineLayout,
      paint: {
        'line-width': 4,
        'line-gradient': [
          'interpolate',
          ['linear'],
          ['line-progress'],
          0,
          '#fbbf24',
          0.18,
          '#00DCA0',
          1,
          '#00c99a',
        ],
      },
    });

    map.addLayer({
      id: 'route-animated',
      type: 'line',
      source: 'route',
      layout: lineLayout,
      paint: {
        'line-color': '#e6fffa',
        'line-width': 2.5,
        'line-opacity': 0.55,
        'line-dasharray': [0, 4, 3],
      },
    });

    map.addLayer({
      id: 'route-scout-glow',
      type: 'circle',
      source: 'route-scout',
      paint: {
        'circle-radius': 18,
        'circle-color': '#00DCA0',
        'circle-opacity': 0.18,
        'circle-blur': 0.8,
      },
    });

    map.addLayer({
      id: 'route-scout-core',
      type: 'circle',
      source: 'route-scout',
      paint: {
        'circle-radius': 4.5,
        'circle-color': '#e6fffa',
        'circle-stroke-width': 2,
        'circle-stroke-color': '#00DCA0',
        'circle-opacity': 0.9,
      },
    });

    const dashArraySequence = [
      [0, 4, 3],
      [0.5, 4, 2.5],
      [1, 4, 2],
      [1.5, 4, 1.5],
      [2, 4, 1],
      [2.5, 4, 0.5],
      [3, 4, 0],
      [0, 0.5, 3, 3.5],
      [0, 1, 3, 3],
      [0, 1.5, 3, 2.5],
      [0, 2, 3, 2],
      [0, 2.5, 3, 1.5],
      [0, 3, 3, 1],
      [0, 3.5, 3, 0.5],
    ];
    let dashStep = 0;
    function animateDash(timestamp) {
      const newStep = Math.floor((timestamp / 65) % dashArraySequence.length);
      if (newStep !== dashStep) {
        map.setPaintProperty('route-animated', 'line-dasharray', dashArraySequence[newStep]);
        dashStep = newStep;
      }

      const scoutSource = map.getSource('route-scout');
      if (scoutSource) {
        scoutSource.setData(pointFeature(interpolateRoute(optimizedRouteCoordinates, timestamp / 14000)));
      }

      requestAnimationFrame(animateDash);
    }
    requestAnimationFrame(animateDash);

    // Outer pulsing ring.
    map.addLayer({
      id: 'stop-pulse',
      type: 'circle',
      source: 'stops',
      paint: {
        'circle-radius': ['match', ['get', 'kind'], 'depot', 28, 20],
        'circle-color': [
          'match',
          ['get', 'kind'],
          'depot',
          'rgba(251,191,36,0.2)',
          'rgba(0,220,160,0.2)',
        ],
        'circle-opacity': 0,
        'circle-blur': 0.6,
      },
    });

    map.addLayer({
      id: 'stop-halo',
      type: 'circle',
      source: 'stops',
      paint: {
        'circle-radius': ['match', ['get', 'kind'], 'depot', 22, 15],
        'circle-color': [
          'match',
          ['get', 'kind'],
          'depot',
          'rgba(251,191,36,0.5)',
          'rgba(0,220,160,0.4)',
        ],
        'circle-opacity': 0,
        'circle-blur': 0.4,
      },
    });

    map.addLayer({
      id: 'stop-core',
      type: 'circle',
      source: 'stops',
      paint: {
        'circle-radius': ['match', ['get', 'kind'], 'depot', 10, 7.5],
        'circle-color': '#12141a',
        'circle-stroke-width': 2.5,
        'circle-stroke-color': [
          'match',
          ['get', 'kind'],
          'depot',
          '#fbbf24',
          '#00DCA0',
        ],
        'circle-opacity': 0,
      },
    });

    map.addLayer({
      id: 'stop-labels',
      type: 'symbol',
      source: 'stops',
      layout: {
        'text-field': ['get', 'label'],
        'text-size': ['match', ['get', 'kind'], 'depot', 9, 10],
        'text-font': ['DIN Pro Bold', 'Arial Unicode MS Bold'],
        'text-anchor': 'center',
        'text-allow-overlap': true,
      },
      paint: {
        'text-color': '#f4f4f5',
        'text-halo-color': '#0a0b0e',
        'text-halo-width': 1.5,
        'text-halo-blur': 0.25,
        'text-opacity': 0,
      },
    });

    // Sequential stop appearance animation.
    const stopCount = stops.length;
    let currentStop = 0;

    function animateStops() {
      if (currentStop < stopCount) {
        const delay = currentStop * 180;
        setTimeout(() => {
          map.setPaintProperty('stop-core', 'circle-opacity', 1);
          map.setPaintProperty('stop-halo', 'circle-opacity', 0.85);
          map.setPaintProperty('stop-labels', 'text-opacity', 1);
        }, delay);
        currentStop++;
        animateStops();
      }
    }
    setTimeout(animateStops, 1200);

    // Pulsing animation on stop halos.
    let pulsePhase = 0;
    function animatePulse() {
      pulsePhase += 0.015;
      const opacity = 0.3 + Math.sin(pulsePhase) * 0.25;
      const radius = 1 + Math.sin(pulsePhase) * 0.15;

      map.setPaintProperty('stop-pulse', 'circle-opacity', opacity);
      map.setPaintProperty('stop-pulse', 'circle-radius', [
        'match',
        ['get', 'kind'],
        'depot',
        28 * radius,
        20 * radius,
      ]);

      requestAnimationFrame(animatePulse);
    }
    setTimeout(animatePulse, 1500);

    // Slow orbit keeps the tactical map alive without stealing attention from the form.
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const baseBearing = map.getBearing();
    const basePitch = map.getPitch();
    let orbitStartedAt;
    function rotateCameraSlowly(timestamp) {
      if (reduceMotion) return;

      orbitStartedAt = orbitStartedAt || timestamp;
      const elapsed = timestamp - orbitStartedAt;

      map.setBearing(baseBearing + (elapsed / 1000) * 0.55);
      map.setPitch(basePitch + Math.sin(elapsed / 7000) * 3);
      requestAnimationFrame(rotateCameraSlowly);
    }
    setTimeout(() => requestAnimationFrame(rotateCameraSlowly), 2000);
  });
})();
