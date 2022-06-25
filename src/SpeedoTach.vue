<template>
  <div class="tach-container">
    <canvas id="canvasId2" ref="canvas2"></canvas>
  </div>
</template>

<script> 
import * as mqtt from 'mqtt/dist/mqtt';
var msg;
const client  = mqtt.connect('ws://localhost:8008')
client.on('connect', function () {
console.log('Connected')
client.subscribe('esp/rpm', function (err) {
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

export default{

  methods: { 

    drawMiniNeedle(rotation, width, rpm, ctx) {
        ctx.lineWidth = width;

        ctx.save();
        ctx.translate(250, 250);
        ctx.rotate(rotation);
        ctx.strokeStyle = "white";
        ctx.fillStyle = "#333";
        ctx.strokeRect(-20 / 2 + 220, -1 / 2, 20, 1);
        ctx.restore();

        let x = (250 + 180 * Math.cos(rotation));
        let y = (250 + 180 * Math.sin(rotation));

        ctx.font = "500 35px Open Sans";
        ctx.fillText(rpm, x, y);

        rotation += Math.PI / 180;
    },

    rpmNeedle(rotation, ctx) {
      ctx.lineWidth = 2;

      ctx.save();
      ctx.translate(250, 250);
      ctx.rotate(rotation);
      ctx.fillRect(-130 / 2 + 170, -4, 135, 3);
      ctx.restore();

      rotation += Math.PI / 180;
    },


    calculateRPMAngle(x, a, b) {
      let degree = (a - b) * (x) + b;
      let radian = (degree * Math.PI)/180;
      return radian <= 4.71238898038 ? radian : 4.71238898038;
    },

    drawTach(rpm, c) {
      var ctx = c.getContext('2d');
      ctx.globalAlpha = 1;
      c.width = 500;
      c.height = 500;

      //Rescale the size
      ctx.scale(1,1);

      var rpmGradient = ctx.createLinearGradient(0, 0, 500, 0);
      rpmGradient.addColorStop(0, '#1afcf1');
      rpmGradient.addColorStop(.31, '#f7b733');
      rpmGradient.addColorStop(.78, '#f7b733');
      rpmGradient.addColorStop(1, 'red');

      ctx.clearRect(0, 0, 500, 500);

      ctx.beginPath();
      ctx.fillStyle = 'rgba(0, 0, 0, 1)';
      ctx.arc(250, 250, 240, 0, 2 * Math.PI);
      ctx.fill();
      ctx.save()
      ctx.restore();
      ctx.fillStyle = "#FFF";
      ctx.stroke();

      ctx.beginPath();
      ctx.strokeStyle = "#333";
      ctx.lineWidth = 10;
      ctx.arc(250, 250, 100, 0, 2 * Math.PI);
      ctx.stroke();

      ctx.beginPath();
      ctx.lineWidth = 1;
      ctx.arc(250, 250, 240, 0, 2 * Math.PI);
      ctx.stroke();

      ctx.font = "700 130px lcars";
      ctx.textAlign = "center";
      ctx.fillText(rpm, 250, 290);

      ctx.font = "600 28px Open Sans";
      ctx.fillText("rpm", 250, 310);

      ctx.fillStyle = "#FFF";

      ctx.beginPath();
      ctx.strokeStyle = "#41dcf4";
      ctx.lineWidth = 10;
      ctx.shadowBlur = 10;
      ctx.shadowColor = "#00c6ff";

      ctx.arc(250, 250, 245, 0, 360 * Math.PI)
      ctx.stroke();

      ctx.fillStyle = "#FFF";
      for (var i = 0; i <= Math.ceil(11 / 1) * 1; i += 1) {
        console.log();
        this.drawMiniNeedle(this.calculateRPMAngle(i / 11, 128, 34.3775) * Math.PI, i % 1 == 0 ? 3 : 1, i%1 == 0 ? i : '', ctx);
        }

      ctx.stroke();
      ctx.beginPath();
      ctx.lineWidth = 25;
      ctx.strokeStyle = rpmGradient;
      ctx.shadowBlur = 10;
      ctx.shadowColor = "#f7b733";

      ctx.arc(250, 250, 228, .598 * Math.PI, this.calculateRPMAngle(rpm / 11000, 128, 34.3775) * Math.PI, false, ctx);
      ctx.stroke();
      ctx.shadowBlur = 0;

      ctx.strokeStyle = 'red';
      ctx.fillStyle = 'red';
      this.rpmNeedle(this.calculateRPMAngle(rpm / 11000, 128, 34.3775) * Math.PI, ctx);

      ctx.strokeStyle = "#000";
    },

    setRpm (draw, c) {
      let rpm = 0;
      setInterval(function(){
      console.log(msg)
      // let rpm = parseInt(msg);
      let rpm = 2300;
      draw(rpm, c);

      }, 40);
    },

    debug (txt) {
    console.log(txt)
    }
  },

  mounted() {
    var c = document.getElementById("canvasId2")
    this.setRpm(this.drawTach, c)
  },
}
</script>

<style scoped>

  * {
    background: black;
    font-family: 'Open Sans', sans-serif;
    width: 100%;
    height: 100%;
  }

  .tach-container {
  position: absolute;
  top: 0;
  left: 55%;
  width: 42%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  }

</style>
