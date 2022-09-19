<template>
  <GMapMap
      :center="center"
      :id="map"
      ref="myMapRef"
      :zoom="18"
      map-type-id="roadmap"
      style="width: 1122px; height: 550px"
  >
  <GMapMarker
        :key="marker.id"
        :icon= "markerOptions"
        v-for="marker in markers"
        :position="marker.position"
    />
  </GMapMap>
 
</template>

<script>
import InspectBracketTL from './InspectBracketTL.vue'
import WarpCore from './warpcore.vue'
import * as mqtt from 'mqtt/dist/mqtt'
import mapMarker from './planets/intrepid_marker.png'

var lati = 39.917905;
var long = -77.573876;;
var coords;
var regex = /[+-]?\d+(\.\d+)?/g;
var msg;

const client  = mqtt.connect('ws://broker.emqx.io:8083/mqtt')

client.on('connect', function () {
console.log('Connected')

client.subscribe('esp/gps', function (err) {
if (!err) {
  client.publish('test', 'Hello mqtt')
}
  })
})

client.on('message', function (topic, message, packet) {
// Payload is Buffer
msg = message.toString();
console.log(msg)
coords = msg.split(',')
lati = parseFloat(coords[0].match(regex).map(function(v) { return parseFloat(v); }));
long = parseFloat(coords[1].match(regex).map(function(v) { return parseFloat(v); }));
console.log(lati)
console.log(long)
})

export default {
  
  data() {
    return {
      center: {lat:lati, lng:long},
      mapOptions: {},
      markers: [
        {
          position: {lat: lati, lng: long},
        }
      ],
      markerOptions: {
        url: mapMarker,
        scaledSize: { width: 45, height: 90}
      }
        };
  },

  methods: {
       
        follow() {
          const map = this.$refs.myMapRef;
          setInterval(function(){
            map.panTo(new google.maps.LatLng(lati,long));
          }, 500)
        }
  },

  mounted() {

    this.$refs.myMapRef.$mapPromise.then((mapObject) => {
    console.log('map is loaded now', mapObject);
    });

    this.$refs.myMapRef.$mapPromise.then((map) => {
        map.setOptions({
          styles: [
            {
              featureType: 'poi.business',
              stylers: [{ visibility: 'off' }],
            },
            {
              featureType: 'transit',
              elementType: 'labels.icon',
              stylers: [{ visibility: 'off' }],
            },
          ]
        })
    });
    this.follow();
  }
}
</script>

