<template>
  <GMapMap
      :center="center"
      ref="myMapRef"
      :zoom="18"
      map-type-id="terrain"
      style="width: 1122px; height: 550px"
  >
  <GMapMarker
        :key="marker.id"
        v-for="marker in markers"
        :position="marker.position"
    />
      <GMapCluster>
        <GMapMarker
            :key="index"
            v-for="(m, index) in markers"
            :position="m.position"
            @click="center=m.position"
        />
      </GMapCluster>
  </GMapMap>
 
</template>

<script>
import InspectBracketTL from './InspectBracketTL.vue'
import WarpCore from './warpcore.vue'
import * as mqtt from 'mqtt/dist/mqtt';

var lati = 39.917905;
var long = -77.573876;;
var coords;
var regex = /[+-]?\d+(\.\d+)?/g;
var msg;
var options = {
    host: 'broker.emqx.io',
    port: 8083,
    //protocol: 'wss',
}
const client  = mqtt.connect(options)
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
lati = coords[0].match(regex).map(function(v) { return parseFloat(v); });
long = coords[1].match(regex).map(function(v) {return parseFloat(v); });
})

export default {
  methods() {

  },
  data() {
    return {
      center: { lat:lati, lng:long },
      markers: [{
        id:'dfsldjl3r',
        position:{
          lat:this.lati, lng:this.long
        }
      }]
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
})
  },
}
</script>

