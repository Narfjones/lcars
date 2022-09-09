<template>
  <GMapMap
      :center="center"
      ref="myMapRef"
      :zoom="7"
      map-type-id="terrain"
      style="width: 1122px; height: 550px"
  >
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

var lati = -34.397;
var long = 150.644;
var regex = /[+-]?\d+(\.\d+)?/g;
var msg;
const client  = mqtt.connect('ws://localhost:8008')
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
})

export default {
  methods() {

  },
  data() {
    return {
      center: {lat: this.lati, lng: this.long},
      markers: []
    }
  },
  mounted() {
    this.$refs.myMapRef.$mapPromise.then((mapObject) => {
      console.log('map is loaded now', mapObject);
    });
  },
}
</script>

