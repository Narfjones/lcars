<template>
  <GMapMap
      :center="center"
      :id="map"
      ref="myMapRef"
      :zoom="18"
      map-type-id="roadmap"
      style="width: 1000px; height: 400px"
  >
  <GMapMarker
        :key="marker.id"
        :icon= "markerOptions"
        v-for="marker in markers"
        :position="marker.position"
    />
  </GMapMap>

  <div class="info">
    <canvas id="canvasId" ref="canvas"></canvas>
  </div>

</template>

<script>
import * as mqtt from 'mqtt/dist/mqtt'
import mapMarker from './planets/intrepid_marker.png'
import Speedo2 from './Speedo2.vue';

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
            center: { lat: lati, lng: long },
            mapOptions: {},
            markers: [
                {
                    position: this.center
                }
            ],
            markerOptions: {
                url: mapMarker,
                scaledSize: { width: 45, height: 90 }
            }
        };
    },
    methods: {

      drawSpeedo(speed, c) {
        var ctx = c.getContext('2d');
        ctx.globalAlpha = 1;
        c.width = 150;
        c.height = 75;

        //Rescale the size
        ctx.scale(1,1);

        ctx.fillStyle = "#FFF";
        ctx.strokeStyle = "#000";

        ctx.font = "80 76px lcars";
        ctx.textAlign = "right";
        ctx.fillText(speed, 85, 65);

        ctx.font = "150 50px lcars";
        ctx.textAlign = "left";
        ctx.fillText("mph", 95, 65);

        ctx.beginPath(); 
        ctx.moveTo(0,0);
        ctx.lineTo(0, 0);
        ctx.stroke();
        },

      setSpeed (draw, c) {
        let speedM = 0;
        setInterval(function(){
          if (speedM > 120){
              speedM = 0;
            }
          speedM++;
          draw(speedM, c);
        }, 100);
      }

    },
    mounted() {

        this.$refs.myMapRef.$mapPromise.then((mapObject) => {
            console.log("map is loaded now", mapObject);
        });

        this.$refs.myMapRef.$mapPromise.then((map) => {
            map.setOptions({
                styles: [
                    {
                        featureType: "poi.business",
                        stylers: [{ visibility: "off" }],
                    },
                    {
                        featureType: "transit",
                        elementType: "labels.icon",
                        stylers: [{ visibility: "off" }],
                    },
                ]
            });
        });

      var c = document.getElementById('canvasId');
      this.setSpeed(this.drawSpeedo, c);

    },

    components: { Speedo2 }
}
</script>

<style>
.info{
  height: 70px;
  width: 800px;
}
</style>
