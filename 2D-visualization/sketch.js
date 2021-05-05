var table;
var dataX;
var dataY;
var dataR;
var num;
var Circles = [];

function preload(){
  table = loadTable('2d-uniform-title.csv', 'csv','header')
}

function setup() {
  createCanvas(800, 800);
  background(255);
  
  num = table.getRowCount();
  dataX = table.getColumn('Xcoordination');
  dataY = table.getColumn('Ycoordination');
  dataR = table.getColumn('radius');
  for(let i = 0; i < num; i++){
    let c = new Circle(dataX[i], dataY[i], dataR[i], 120, 120, 120)
    Circles.push(c);
  }
}

function draw() {
  background(255);
  for(let j = 0; j < Circles.length; j++){
    if(Circles[j].r >= 2){
      Circles[j].show()
    } 
  }
  noFill()
  strokeWeight(5)
  rect(0, 0, 800, 800)
}

class Circle {
  constructor(x, y, r, a, b, c) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.a = a;
    this.b = b;
    this.c = c;
  }

  show() {
    stroke(0);
    strokeWeight(2);
    fill(this.a, this.b, this.c);
    ellipse(this.x, this.y, this.r * 2, this.r * 2);
  }
}
