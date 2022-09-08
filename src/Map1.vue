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
  data() {
    return {
      center: { lat:51.093048, lng: 6.84212},
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

