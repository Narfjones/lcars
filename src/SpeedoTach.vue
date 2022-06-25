<template>
  <canvas id="canvasId" ref="canvas"></canvas>
</template>

<script> 
import * as mqtt from 'mqtt/dist/mqtt';
var msg;
const client  = mqtt.connect('ws://localhost:8008')
client.on('connect', function () {
console.log('Connected')
client.subscribe('esp/speed', function (err) {
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
    
    speedNeedle(rotation, ctx) {
      ctx.lineWidth = 2;

      ctx.save();
      ctx.translate(250, 250);
      ctx.rotate(rotation);
      ctx.strokeRect(-130 / 2 + 170, -1 / 2, 135, 1);
      ctx.restore();

      rotation += Math.PI / 180;
    },

    rpmNeedle(rotation, ctx) {
      ctx.lineWidth = 2;

      ctx.save();
      ctx.translate(250, 250);
      ctx.rotate(rotation);
      ctx.strokeRect(-130 / 2 + 170, -1 / 2, 135, 1);
      ctx.restore();

      rotation += Math.PI / 180;
    },

    drawMiniNeedle(rotation, width, speed, ctx) {
      ctx.lineWidth = width;

      ctx.save();
      ctx.translate(250, 250);
      ctx.rotate(rotation);
      ctx.strokeStyle = "#333";
      ctx.fillStyle = "#333";
      ctx.strokeRect(-20 / 2 + 220, -1 / 2, 20, 2);
      ctx.restore();

      let x = (250 + 180 * Math.cos(rotation));
      let y = (250 + 180 * Math.sin(rotation));

      ctx.font = "700 20px Open Sans";
      ctx.fillText(speed, x, y);

      rotation += Math.PI / 180;
    },

    calculateSpeedAngle(x, a, b) {
      let degree = (a - b) * (x) + b;
      let radian = (degree * Math.PI) / 180;
      return radian <= 1.45 ? radian : 1.45;
    },

    calculateRPMAngle(x, a, b) {
      let degree = (a - b) * (x) + b;
      let radian = (degree * Math.PI) / 180;
      return radian >= -0.46153862656807704 ? radian : -0.46153862656807704;
    },

    drawSpeedo(speed, gear, rpm, topSpeed, c) {
      var ctx = c.getContext('2d');
      ctx.globalAlpha = 1;
      c.width = 500;
      c.height = 500;

      //Rescale the size
      ctx.scale(1,1);

      var speedGradient = ctx.createLinearGradient(0, 500, 0, 0);
      speedGradient.addColorStop(0, '#00b8fe');
      speedGradient.addColorStop(1, '#41dcf4');

      var rpmGradient = ctx.createLinearGradient(0, 500, 0, 0);
      rpmGradient.addColorStop(0, '#f7b733');
      rpmGradient.addColorStop(1, '#fc4a1a');
      
      if (speed == undefined) {
          return false;
      } else {
          speed = Math.floor(speed);
          rpm = rpm * 10;
      }

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

      ctx.font = "700 70px Open Sans";
      ctx.textAlign = "center";
      ctx.fillText(speed, 250, 260);

      ctx.font = "700 22px Open Sans";
      ctx.fillText("mph", 250, 280);

      if (gear == 0 && speed > 0) {
          ctx.fillStyle = "#999";
          ctx.font = "700 70px Open Sans";
          ctx.fillText('R', 250, 460);

          ctx.fillStyle = "#333";
          ctx.font = "50px Open Sans";
          ctx.fillText('N', 290, 460);
      } else if (gear == 0 && speed == 0) {
          ctx.fillStyle = "#999";
          ctx.font = "700 70px Open Sans";
          ctx.fillText('N', 250, 460);

          ctx.fillStyle = "#333";
          ctx.font = "700 50px Open Sans";
          ctx.fillText('R', 210, 460);

          ctx.font = "700 50px Open Sans";
          ctx.fillText(parseInt(gear) + 1, 290, 460);
      } else if (gear - 1 <= 0) {
          ctx.fillStyle = "#999";
          ctx.font = "700 70px Open Sans";
          ctx.fillText(gear, 250, 460);

          ctx.fillStyle = "#333";
          ctx.font = "50px Open Sans";
          ctx.fillText('R', 210, 460);

          ctx.font = "700 50px Open Sans";
          ctx.fillText(parseInt(gear) + 1, 290, 460);
      } else {
          ctx.font = "700 70px Open Sans";
          ctx.fillStyle = "#999";
          ctx.fillText(gear, 250, 460);

          ctx.font = "700 50px Open Sans";
          ctx.fillStyle = "#333";
          ctx.fillText(gear - 1, 210, 460);
          if (parseInt(gear) + 1 < 7) {
              ctx.font = "700 50px Open Sans";
              ctx.fillText(parseInt(gear) + 1, 290, 460);
          }
      }

      ctx.fillStyle = "#FFF";
      for (var i = 10; i <= Math.ceil(topSpeed / 20) * 20; i += 10) {
          this.drawMiniNeedle(this.calculateSpeedAngle(i / topSpeed, 83.07888, 34.3775, ctx) * Math.PI, i % 20 == 0 ? 3 : 1, i%20 == 0 ? i : '', ctx);
          
          if(i<=100) { 
              this.drawMiniNeedle(this.calculateSpeedAngle(i / 47, 0, 22.9183, ctx) * Math.PI, i % 20 == 0 ? 3 : 1, i % 20 == 0 ? i / 10 : '', ctx);
          }
      }

      ctx.beginPath();
      ctx.strokeStyle = "#41dcf4";
      ctx.lineWidth = 25;
      ctx.shadowBlur = 10;
      ctx.shadowColor = "#00c6ff";

      ctx.strokeStyle = speedGradient;
      ctx.arc(250, 250, 228, .6 * Math.PI, this.calculateSpeedAngle(speed / topSpeed, 83.07888, 34.3775) * Math.PI, ctx);
      ctx.stroke();
      ctx.beginPath();
      ctx.lineWidth = 25;
      ctx.strokeStyle = rpmGradient;
      ctx.shadowBlur = 10;
      ctx.shadowColor = "#f7b733";

      ctx.arc(250, 250, 228, .4 * Math.PI, this.calculateRPMAngle(rpm / 4.7, 0, 22.9183) * Math.PI, true, ctx);
      ctx.stroke();
      ctx.shadowBlur = 0;


      ctx.strokeStyle = '#41dcf4';
      this.speedNeedle(this.calculateSpeedAngle(speed / topSpeed, 83.07888, 34.3775, ctx) * Math.PI, ctx);

      ctx.strokeStyle = rpmGradient;
      this.rpmNeedle(this.calculateRPMAngle(rpm / 4.7, 0, 22.9183, ctx) * Math.PI, ctx);

      ctx.strokeStyle = "#000";
    },

    setSpeed (draw, c) {
      let speedM = 0;
      let rpm = 0;
      let gear = 0;
      setInterval(function(){
      console.log(msg)
      let speedM = parseInt(msg);
      draw(speedM, gear, rpm, 100, c);

      }, 40);
    },

    debug (txt) {
    console.log(txt)
    }
  },

  mounted() {
    var c = document.getElementById("canvasId")
    this.setSpeed(this.drawSpeedo, c)
  },
}
</script>

<style scoped>
  * {
    background: black;
    font-family: 'Open Sans', sans-serif;
  }
  canvas {
    margin: 0 auto;
    align-self: right;
    display: block;
    opacity: 100%;
    height: 240px;
    width: 50%;
    display: flex;
  }

</style>
