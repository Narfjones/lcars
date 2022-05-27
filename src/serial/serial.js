import { SerialPort } from 'serialport'

const serialport = new SerialPort({ path: 'COM8', baudRate: 9600 })
let Readline = SerialPort.parsers.Readline;
let parser = new Readline();
serialport.pipe(parser);

serialport.on('open', showPortOpen);    // called when the serial port opens
serialport.on('close', showPortClose);  // called when the serial port closes
serialport.on('error', showError); // called when there's an error with the serial port
parser.on('data', readSerialData);  // called when there's new data incoming
var speedVal;
var rpmVal;

export function getSpeed(){
    info_lst = line.split("|");
    speedVal = parseInt(info_lst[0]);
    console.log(speed, rpm)
    return speedVal, rpmVal
}

export function getRpm(){
    info_lst = line.split("|");
    rpmVal = parseInt(info_lst[1])
    console.log(speed, rpm)
    return speedVal, rpmVal
}