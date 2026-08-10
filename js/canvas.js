const stage=document.getElementById('cv-stage');
let world,svg,blocksEl;
function ensureWorld(){
  if(world)return;
  world=document.createElement('div');world.id='cv-world';world.style.cssText='position:absolute;left:0;top:0;width:0;height:0;transform-origin:0 0';
  svg=document.getElementById('cv-links-svg');blocksEl=document.getElementById('cv-blocks');
  stage.appendChild(world);world.appendChild(svg);world.appendChild(blocksEl);
  svg.setAttribute('width','200000');svg.setAttribute('height','200000');
  svg.style.cssText='position:absolute;left:0;top:0;overflow:visible;pointer-events:none';
}
function applyT(){const v=SON.view;world.style.transform='translate('+v.x+'px,'+v.y+'px) scale('+v.scale+')';}
function toWorld(cx,cy){const r=stage.getBoundingClientRect(),v=SON.view;return[(cx-r.left-v.x)/v.scale,(cy-r.top-v.y)/v.scale];}
function centerOn(x,y,a){const r=stage.getBoundingClientRect(),v=SON.view;v.x=r.width/2-x*v.scale;v.y=r.height/2-y*v.scale;if(a){world.style.transition='transform .45s cubic-bezier(.2,.8,.2,1)';applyT();setTimeout(()=>world.style.transition='',480);}else applyT();}
function save(){clearTimeout(save._t);save._t=setTimeout(()=>{if(SON.curId)Store.saveCanvas(SON.curId,getState());},280);}
function getState(){const m=SON.model;return{blocks:m.blocks.map(b=>({id:b.id,type:b.type,x:b.x,y:b.y,color:b.color,text:b.text,data:b.data})),links:m.links.map(l=>Object.assign({},l)),tables:m.tables.map(t=>({id:t.id,x:t.x,y:t.y,cols:t.cols,rows:t.rows,cells:t.cells})),view:SON.view,bg:Store.getBg()};}
function loadModel(d){const c=d.canvas||{};SON.model={blocks:c.blocks||[],links:c.links||[],tables:c.tables||[]};SON.view=(c.view&&c.view.scale)?c.view:{x:0,y:0,scale:1};}
function renderAll(){ensureWorld();blocksEl.innerHTML='';svg.innerHTML='';SON.model.blocks.forEach(b=>Blocks.render(b));SON.model.tables.forEach(t=>Tables.render(t));requestAnimationFrame(renderLinks);}
window.SON={model:null,view:{x:0,y:0,scale:1},curId:null,stage:stage,linkOpts:{type:'thread',style:'solid',color:'#FFD700'},arm:null,onConn:null,save:save,renderAll:renderAll,renderLinks:null,toWorld:toWorld,centerOn:centerOn,addLink:null,removeLink:null,get blocksEl(){return blocksEl;}};
window.__renderCanvas=id=>{const d=Store.get(id);if(!d)return;SON.curId=id;loadModel(d);renderAll();};
window.__getCanvasState=getState;window.__applyBg=i=>{if(window.FX)FX.applyBg(i);};
window.__autoLayout=()=>{let x=40,y=40,c=0;SON.model.blocks.forEach(b=>{b.x=x;b.y=y;if(b._el){b._el.style.left=x+'px';b._el.style.top=y+'px';}x+=220;if(++c%3===0){x=40;y+=150;}});renderLinks();save();toast(t('toast_autorun'));};
window.__exportPDF=()=>toast(t('toast_pdf'));

// ПАНОРМА И ЗУМ
const _ptrs=new Map();let _pan=null,_pinch=null;
const _dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
stage.addEventListener('pointerdown',e=>{
  if(e.target.closest('.blk,.tbl,.conn,.over-widget,.cv-topbar,.cv-bottombar,.cv-meta,.cv-stats'))return;
  _ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});stage.setPointerCapture(e.pointerId);
  if(_ptrs.size===1)_pan={x:e.clientX,y:e.clientY,vx:SON.view.x,vy:SON.view.y};
  else if(_ptrs.size===2){
    const p=[..._ptrs.values()];_pinch={d:_dist(p[0],p[1]),s:SON.view.scale,cx:(p[0].x+p[1].x)/2,cy:(p[0].y+p[1].y)/2};_pan=null;
  }
});
stage.addEventListener('pointermove',e=>{
  if(!_ptrs.has(e.pointerId))return;
  _ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(_ptrs.size===1&&_pan){
    SON.view.x=_pan.vx+(e.clientX-_pan.x);SON.view.y=_pan.vy+(e.clientY-_pan.y);applyT();
  }else if(_ptrs.size===2&&_pinch){
    const p=[..._ptrs.values()];_zoomAt(_pinch.cx,_pinch.cy,_pinch.s*(_dist(p[0],p[1])/_pinch.d));
  }
});
function _endP(e){_ptrs.delete(e.pointerId);if(_ptrs.size<2)_pinch=null;if(_ptrs.size===0){_pan=null;save();}}
stage.addEventListener('pointerup',_endP);stage.addEventListener('pointercancel',_endP);
stage.addEventListener('wheel',e=>{
  e.preventDefault();_zoomAt(e.clientX,e.clientY,SON.view.scale*(e.deltaY<0?1.12:1/1.12));
},{passive:false});
function _zoomAt(cx,cy,ns){ns=Math.max(.25,Math.min(3,ns));const r=stage.getBoundingClientRect(),v=SON.view,wx=(cx-r.left-v.x)/v.scale,wy=(cy-r.top-v.y)/v.scale;v.scale=ns;v.x=cx-r.left-wx*ns;v.y=cy-r.top-wy*ns;applyT();}
/* == END canvas == */
