let _tuid=1;const _tid=()=>'T-'+Date.now().toString(36).toUpperCase()+'-'+(_tuid++);
function buildPicker(){
  const g=document.getElementById('table-grid');if(!g||g.dataset.built)return;g.dataset.built='1';
  g.style.gridTemplateColumns='repeat(20,1fr)';let h='';for(let i=0;i<400;i++)h+='<div class="tg-cell" data-i="'+i+'"></div>';g.innerHTML=h;
  let st=null,cur=null;const idx=e=>{const c=e.target.closest('.tg-cell');return c?+c.dataset.i:-1;};
  function paint(){if(st==null)return;const a=Math.min(st,cur),b=Math.max(st,cur),r0=a/20|0,r1=b/20|0,c0=a%20,c1=b%20;
    g.querySelectorAll('.tg-cell').forEach(c=>{const i=+c.dataset.i,rr=i/20|0,cc=i%20;c.classList.toggle('on',rr>=Math.min(r0,r1)&&rr<=Math.max(r0,r1)&&cc>=Math.min(c0,c1)&&cc<=Math.max(c0,c1));});}
  g.addEventListener('pointerdown',e=>{const i=idx(e);if(i<0)return;st=i;cur=i;paint();});
  g.addEventListener('pointermove',e=>{if(st==null)return;const i=idx(e);if(i>=0){cur=i;paint();}});
  document.getElementById('table-create').onclick=()=>{
    let R=3,C=3;if(st!=null){const a=Math.min(st,cur),b=Math.max(st,cur);R=Math.abs((b/20|0)-(a/20|0))+1;C=Math.abs((b%20)-(a%20))+1;}
    createTable(R,C);closeModal('m-tables');
  };
}
function createTable(rows,cols){
  const r=stage.getBoundingClientRect(),c=SON.toWorld(r.left+r.width/2,r.top+r.height/2);
  const cells=[],hdr=['ID','Значение','Дата'];for(let j=0;j<cols;j++)cells.push(j<hdr.length?hdr[j]:'');
  const now=new Date().toLocaleDateString();for(let i=1;i<rows;i++)for(let j=0;j<cols;j++)cells.push(j===0?'r'+i:j===2?now:'');
  const tb={id:_tid(),x:c[0]-100,y:c[1]-60,rows:rows,cols:cols,cells:cells};
  SON.model.tables.push(tb);renderTable(tb);SON.save();toast(t('table_added'));
}
function renderTable(tb){
  const el=document.createElement('div');el.className='tbl';el.style.left=tb.x+'px';el.style.top=tb.y+'px';tb._el=el;
  el.innerHTML='<div class="tbl-head"><span class="th-t">TABLE '+tb.rows+'x'+tb.cols+'</span><button class="blk-x">✕</button></div>'+
    '<div class="tbl-grid" style="display:grid;grid-template-columns:repeat('+tb.cols+',minmax(54px,1fr))">'+
    tb.cells.map((v,i)=>'<div class="td'+(i<tb.cols?' mono':'')+'" contenteditable="true" data-ci="'+i+'">'+v+'</div>').join('')+'</div>';
  SON.blocksEl.appendChild(el);
  el.querySelector('.blk-x').onclick=ev=>{
    ev.stopPropagation();el.remove();SON.model.tables=SON.model.tables.filter(x=>x.id!==tb.id);SON.save();
  };
  el.querySelectorAll('.td').forEach(td=>td.oninput=()=>{tb.cells[+td.dataset.ci]=td.textContent;SON.save();});
  let d=null;el.addEventListener('pointerdown',e=>{
    if(e.target.closest('.td,.blk-x'))return;e.stopPropagation();d={px:e.clientX,py:e.clientY,bx:tb.x,by:tb.y};el.setPointerCapture(e.pointerId);el.classList.add('dragging');
  });
  el.addEventListener('pointermove',e=>{
    if(!d)return;const s=SON.view.scale;tb.x=d.bx+(e.clientX-d.px)/s;tb.y=d.by+(e.clientY-d.py)/s;el.style.left=tb.x+'px';el.style.top=tb.y+'px';
  });
  el.addEventListener('pointerup',()=>{if(d){d=null;el.classList.remove('dragging');SON.save();}});
}
document.addEventListener('DOMContentLoaded',buildPicker);
window.Tables={render:renderTable,createTable:createTable};
