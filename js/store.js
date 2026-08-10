const Store=(function(){
const K={user:"son_user",dos:"son_dossiers",cur:"son_cur",bg:"son_bg"};
const NICK_COOLDOWN=7*24*3600*1000;
const rd=(k,d)=>{try{const v=localStorage.getItem(k);return v==null?d:JSON.parse(v);}catch(e){return d;}};
const wr=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}};
const rid=()=> "SID-"+Math.random().toString(36).slice(2,8).toUpperCase()+"-"+Date.now().toString(36).slice(-4).toUpperCase();
const did=()=> "D-"+Date.now().toString(36).toUpperCase()+"-"+Math.random().toString(36).slice(2,6).toUpperCase();

function getUser(){let u=rd(K.user,null);if(!u||!u.id){u={id:rid(),nick:"",nickChangedAt:0};wr(K.user,u);}return u;}
function saveUser(u){wr(K.user,u);}
function canChangeNick(){const u=getUser();return (Date.now()-(u.nickChangedAt||0))>=NICK_COOLDOWN;}
function daysUntilNick(){const u=getUser();const ms=NICK_COOLDOWN-(Date.now()-(u.nickChangedAt||0));return ms<=0?0:Math.ceil(ms/(24*3600*1000));}
function setNick(n){const u=getUser();if(!canChangeNick())return false;u.nick=n;u.nickChangedAt=Date.now();saveUser(u);return true;}
function forceFirstNick(n){const u=getUser();u.nick=n;if(!u.nickChangedAt)u.nickChangedAt=Date.now();saveUser(u);}

function all(){return rd(K.dos,[]);}
function saveAll(a){wr(K.dos,a);}
function get(id){return all().find(d=>d.id===id)||null;}
function list(){return all().slice().sort((a,b)=>(b.pinned?1:0)-(a.pinned?1:0)||(b.updated||0)-(a.updated||0));}
function create(name){
  const a=all(); const d={id:did(),name:(name&&name.trim())||"Без названия",
    status:"work",pinned:false,updated:Date.now(),
    canvas:{blocks:[],links:[],tables:[],view:{x:0,y:0,scale:1},bg:getBg()}};
  a.push(d); saveAll(a); setCur(d.id); return d;
}
function update(id,patch){const a=all();const i=a.findIndex(d=>d.id===id);if(i<0)return null;
  a[i]=Object.assign(a[i],patch,{updated:Date.now()}); saveAll(a); return a[i];}
function saveCanvas(id,canvas){return update(id,{canvas});}
function setStatus(id,st){return update(id,{status:st});}
function togglePin(id){const d=get(id);if(!d)return null;return update(id,{pinned:!d.pinned});}
function remove(id){saveAll(all().filter(d=>d.id!==id));if(getCur()===id)setCur(null);}

function getCur(){return rd(K.cur,null);}
function setCur(id){wr(K.cur,id);}
function getBg(){const v=rd(K.bg,null);return (v==null)?0:v;}
function setBg(i){wr(K.bg,i);}

return {getUser,saveUser,canChangeNick,daysUntilNick,setNick,forceFirstNick,
  all,get,list,create,update,saveCanvas,setStatus,togglePin,remove,
  getCur,setCur,getBg,setBg};
})();
window.Store=Store;
