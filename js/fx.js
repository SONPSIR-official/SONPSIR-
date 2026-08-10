const FX=(function(){
const cv=document.getElementById('fx-canvas'),ctx=cv.getContext('2d');
let W=0,H=0,DPR=1,running=false,raf=0,parts=[],pulses=[],pts=[],stars=[];
const BG_PREVIEW=[
"radial-gradient(circle at 50% 40%,#7a6516,transparent 62%),#0a0b10",
"repeating-linear-gradient(0deg,#1a160c 0 7px,#0a0b10 7px 8px),repeating-linear-gradient(90deg,transparent 0 7px,#1a160c 7px 8px)",
"radial-gradient(#ffd700 1px,transparent 2px) 0 0/14px 14px,#0a0b10",
"radial-gradient(#fff 1px,transparent 2px) 0 0/22px 22px,#05060a",
"conic-gradient(from 200deg,#1a160c,#0a0b10,#1a160c)"
];

function resize(){const r=cv.getBoundingClientRect();DPR=Math.min(window.devicePixelRatio||1,2);W=Math.max(1,r.width|0);H=Math.max(1,r.height|0);cv.width=W*DPR;cv.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0);makeParticles();makeStars();}
function makeParticles(){const n=Math.min(90,(W*H/12000)|0);parts=[];for(let i=0;i<n;i++)parts.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.15,vy:-.05-Math.random()*.15,r:.6+Math.random()*1.3,p:Math.random()*6.28,s:.5+Math.random()*1.5});}
function makeStars(){const n=Math.min(220,(W*H/4000)|0);stars=[];for(let i=0;i<n;i++)stars.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.3+.2,a:Math.random()*.6+.15,gold:Math.random()<.15});}
function geo(lon,lat){let mw=W*0.92,mh=mw/2,ox=(W-mw)/2,oy=(H-mh)/2;if(mh>H*0.8){mh=H*0.8;mw=mh*2;ox=(W-mw)/2;oy=(H-mh)/2;}return [ox+(lon+180)/360*mw,oy+(90-lat)/180*mh];}

function drawPlanet(){const cx=W/2,cy=H*0.62,R=Math.min(W,H)*0.28;
ctx.fillStyle='rgba(255,215,0,.10)';ctx.fillRect(0,0,W,H);
ctx.fillStyle='#5a4a12';ctx.beginPath();ctx.arc(cx,cy,R,0,6.283);ctx.fill();
ctx.strokeStyle='rgba(255,215,0,.35)';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(cx,cy,R,0,6.283);ctx.stroke();
}
function drawGrid(){const s=42;ctx.lineWidth=1;
for(let x=0;x<=W;x+=s){ctx.strokeStyle=(x%(s*5)===0)?'rgba(255,215,0,.14)':'rgba(255,215,0,.05)';ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
for(let y=0;y<=H;y+=s){ctx.strokeStyle=(y%(s*5)===0)?'rgba(255,215,0,.14)':'rgba(255,215,0,.05)';ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
}
function drawStars(){
for(const s of stars){ctx.fillStyle=s.gold?`rgba(255,215,0,${s.a})`:`rgba(255,255,255,${s.a})`;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,6.283);ctx.fill();}
for(let i=0;i<6;i++){const x=Math.random()*W,y=Math.random()*H;const gr=ctx.createRadialGradient(x,y,0,x,y,7);gr.addColorStop(0,'rgba(255,232,154,.7)');gr.addColorStop(1,'rgba(255,215,0,0)');ctx.fillStyle=gr;ctx.beginPath();ctx.arc(x,y,7,0,6.283);ctx.fill();}
}
function drawMap(){
const C=[-0.1,51.5,2.3,48.9,13.4,52.5,-3.7,40.4,12.5,41.9,37.6,55.8,30.5,50.5,29,41,18,59.3,23.7,37.98,55.3,25.2,77.2,28.6,72.9,19.1,116.4,39.9,121.5,31.2,139.7,35.7,127,37.6,100.5,13.8,103.8,1.3,106.8,-6.2,67,24.9,51.4,35.7,76.9,43.2,82.9,55,44.4,33.3,31.2,30,3.4,6.5,36.8,-1.3,28,-26.2,-7.6,33.6,38.7,9,3,36.8,18.4,-33.9,10.2,36.8,32.5,15.5,-74,40.7,-118.2,34,-87.6,41.9,-79.4,43.7,-99.1,19.4,-123.1,49.3,-80.2,25.8,-96.8,32.8,-122.4,37.8,-73.6,45.5,-46.6,-23.5,-58.4,-34.6,-43.2,-22.9,-77,-12,-74.1,4.7,-70.7,-33.4,-66.9,10.5,-78.5,-0.2,-68.1,-16.5,-56.2,-34.9,151.2,-33.9,145,-37.8,174.8,-36.8,115.9,-31.9,153,-27.5];
pts=[];for(let i=0;i<C.length;i+=2)pts.push(geo(C[i],C[i+1]));
ctx.strokeStyle='rgba(255,215,0,.06)';ctx.lineWidth=1;
for(let i=0;i<pts.length;i++){let best=-1,bd=1e9;for(let j=0;j<pts.length;j++){if(j===i)continue;const dx=pts[i][0]-pts[j][0],dy=pts[i][1]-pts[j][1],d=dx*dx+dy*dy;if(d<bd){bd=d;best=j;}}if(best>=0){ctx.beginPath();ctx.moveTo(pts[i][0],pts[i][1]);ctx.lineTo(pts[best][0],pts[best][1]);ctx.stroke();}}
for(const p of pts){const gr=ctx.createRadialGradient(p[0],p[1],0,p[0],p[1],5);gr.addColorStop(0,'rgba(255,215,0,.5)');gr.addColorStop(1,'rgba(255,215,0,0)');ctx.fillStyle=gr;ctx.beginPath();ctx.arc(p[0],p[1],5,0,6.283);ctx.fill();ctx.fillStyle='#ffe89a';ctx.beginPath();ctx.arc(p[0],p[1],1.1,0,6.283);ctx.fill();}
}
function drawPulses(){if(!pts||pts.length<2)return;
if(Math.random()<0.02&&pulses.length<4){const a=(Math.random()*pts.length)|0;let b=(Math.random()*pts.length)|0;if(b===a)b=(a+1)%pts.length;pulses.push({a:a,b:b,t:0,sp:.006+Math.random()*.008});}
ctx.save();for(let i=pulses.length-1;i>=0;i--){const P=pulses[i];P.t+=P.sp;if(P.t>=1){pulses.splice(i,1);continue;}
 const A=pts[P.a],B=pts[P.b],mx=(A[0]+B[0])/2,my=(A[1]+B[1])/2-Math.abs(A[0]-B[0])*0.15-20;
 ctx.strokeStyle='rgba(255,215,0,.16)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(A[0],A[1]);ctx.quadraticCurveTo(mx,my,B[0],B[1]);ctx.stroke();
 const t=P.t,u=1-t,ix=u*u*A[0]+2*u*t*mx+t*t*B[0],iy=u*u*A[1]+2*u*t*my+t*t*B[1];
 const gr=ctx.createRadialGradient(ix,iy,0,ix,iy,6);gr.addColorStop(0,'rgba(255,232,154,.9)');gr.addColorStop(1,'rgba(255,215,0,0)');ctx.fillStyle=gr;ctx.beginPath();ctx.arc(ix,iy,6,0,6.283);ctx.fill();}
ctx.restore();}

function draw(){ctx.clearRect(0,0,W,H);
ctx.fillStyle='#0a0b10';ctx.fillRect(0,0,W,H);
const bg=(typeof Store!=='undefined'&&Store.getBg)?Store.getBg():0;
if(bg===0)drawPlanet();else if(bg===1)drawGrid();else if(bg===2)drawMap();else if(bg===3)drawStars();else{const gr=ctx.createConicGradient(200*Math.PI/180,W/2,H/2);gr.addColorStop(0,'#1a160c');gr.addColorStop(.5,'#0a0b10');gr.addColorStop(1,'#1a160c');ctx.fillStyle=gr;ctx.fillRect(0,0,W,H);}
drawParticles();
if(bg===2)drawPulses();
}
function drawParticles(){ctx.save();for(const p of parts){p.x+=p.vx;p.y+=p.vy;p.p+=.02*p.s;if(p.y<-4){p.y=H+4;p.x=Math.random()*W;}if(p.x<-4)p.x=W+4;if(p.x>W+4)p.x=-4;const a=.25+.45*(.5+.5*Math.sin(p.p));ctx.globalAlpha=a;ctx.fillStyle='#ffd700';ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.283);ctx.fill();}ctx.restore();}
function frame(){if(!running)return;draw();raf=requestAnimationFrame(frame);}
function enter(){resize();if(!running){running=true;raf=requestAnimationFrame(frame);}}
function leave(){running=false;if(raf)cancelAnimationFrame(raf);raf=0;}
window.addEventListener('resize',resize);
window.__canvasEnter=enter;window.__canvasLeave=leave;
return {enter,leave,resize};
})();
