const BCOLORS={gold:'#FFD700',green:'#37e07a',red:'#ff3b46',blue:'#36b6ff'};
let _buid=1;const _bid=()=>'B-'+Date.now().toString(36).toUpperCase()+'-'+(_buid++);
function addBlock(type,color){
  const r=stage.getBoundingClientRect(),c=SON.toWorld(r.left+r.width/2,r.top+r.height/2);
  const b={id:_bid(),type:type,x:c[0]-90,y:c[1]-40,color:color||BCOLORS[type]||'#FFD700',text:'',data:{}};
  SON.model.blocks.push(b);render(b);SON.renderLinks();SON.save();toast(t('block_added'));return b;
}
function anchor(bid,side){
  const b=SON.model.blocks.find(x=>x.id===bid);if(!b||!b._el)return null;
  const w=b._el.offsetWidth,h=b._el.offsetHeight;
  return[b.x+(side==='l'?0:side==='r'?w:w/2),b.y+(side==='t'?0:side==='b'?h:h/2)];
}
function bodyHtml(b){
  switch(b.type){
    case 'loc':return '<div class="loc-map"><span class="loc-pin">📍</span></div><div class="loc-coord">'+(b.data.coord||'55.75, 37.61')+'</div>';
    case 'aud':return '<div class="cassette"><span class="reel"></span><span class="reel"></span></div><div class="eq">'+Array(16).fill('<i></i>').join('')+'</div><div class="player"><button class="play">▶</button><div class="pbar"><i></i></div><span class="ptime">00:00</span></div>';
    case 'photo':return '<div class="photo-frame"><img src="'+(b.data.src||'')+'" alt="" style="'+(b.data.src?'':'display:none;height:84px;background:#222')+'"></div>';
    case 'video':return '<div class="vid-frame"><div class="vid-poster">▶</div></div>';
    default:return '<textarea class="blk-text" placeholder="…">'+(b.text||'')+'</textarea>';
  }
}
function render(b){
  const el=document.createElement('div');el.className='blk';el.style.left=b.x+'px';el.style.top=b.y+'px';el.style.setProperty('--neon',b.color);
  b._el=el;el.innerHTML='<button class="blk-x">✕</button>'+(b.type==='photo'||b.type==='video'?'<button class="blk-edit">✏</button>':'')+
    '<div class="blk-head"><span class="blk-ico">T</span><span class="blk-title">'+(b.type==='loc'?'Локация':b.type==='aud'?'Аудио':b.type==='photo'?'Фото':b.type==='video'?'Видео':'Текст')+'</span></div>'+
    '<div class="blk-body">'+bodyHtml(b)+'</div>'+
    '<span class="conn t" data-side="t"></span><span class="conn b" data-side="b"></span><span class="conn l" data-side="l"></span><span class="conn r" data-side="r"></span>';
  SON.blocksEl.appendChild(el);
  wireBlock(el,b);
  return el;
}
function wireBlock(el,b){
  el.querySelector('.blk-x').onclick=ev=>{
    ev.stopPropagation();
    confirmDlg(t('confirm_del_block'),()=>{SON.model.blocks=SON.model.blocks.filter(x=>x.id!==b.id);SON.model.links=SON.model.links.filter(l=>l.a!==b.id&&l.b!==b.id);el.remove();SON.renderLinks();SON.save();});
  };
  const ed=el.querySelector('.blk-edit');if(ed)ed.onclick=ev=>{ev.stopPropagation();toast('edit');};
  const ta=el.querySelector('.blk-text');if(ta)ta.oninput=()=>{b.text=ta.value;SON.save();};
  el.querySelectorAll('.conn').forEach(c=>{c.addEventListener('pointerdown',ev=>ev.stopPropagation());c.onclick=ev=>{ev.stopPropagation();if(SON.onConn)SON.onConn(b.id,c.dataset.side);};});
  let d=null;el.addEventListener('pointerdown',e=>{
    if(e.target.closest('textarea,input,.conn,.blk-x,.blk-edit,.player,video,audio,button'))return;
    e.stopPropagation();d={px:e.clientX,py:e.clientY,bx:b.x,by:b.y};el.setPointerCapture(e.pointerId);el.classList.add('dragging');
  });
  el.addEventListener('pointermove',e=>{
    if(!d)return;const s=SON.view.scale;b.x=d.bx+(e.clientX-d.px)/s;b.y=d.by+(e.clientY-d.py)/s;el.style.left=b.x+'px';el.style.top=b.y+'px';SON.renderLinks();
  });
  el.addEventListener('pointerup',()=>{if(d){d=null;el.classList.remove('dragging');SON.save();}});
}
window.Blocks={render,anchor,addBlock};
