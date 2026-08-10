const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
let _tt;
function toast(m){const e=$("#toast");if(!e)return;e.textContent=m;e.classList.add("show");clearTimeout(_tt);_tt=setTimeout(()=>e.classList.remove("show"),1900);}
function showScreen(id){const a=document.querySelector(".screen.active");if(a&&a.id==="screen-canvas"&&id!=="canvas"&&window.__canvasLeave)window.__canvasLeave();$$(".screen").forEach(s=>s.classList.toggle("active",s.id==="screen-"+id));if(id==="canvas"&&window.__canvasEnter)window.__canvasEnter();}
function openModal(id){const m=$("#"+id);if(!m)return;m.classList.add("open");const i=m.querySelector("input");if(i)setTimeout(()=>i.focus(),60);}
function closeModal(m){if(typeof m==="string")m=$("#"+m);if(m)m.classList.remove("open");}
function closeAllModals(){$$(".modal.open").forEach(m=>m.classList.remove("open"));}
const ST={work:"st_work",done:"st_done",closed:"st_closed"};
function stTxt(s){return t(ST[s]||"st_work");}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}

function renderHome(){
  const list=Store.list(),ul=$("#dossier-list"),em=$("#dossier-empty");
  em.classList.toggle("hidden",list.length>0);
  ul.innerHTML=list.map(d=>`<li class="dossier-item${d.pinned?" pinned":""}" data-id="${d.id}">
    ${d.pinned?'<span class="di-pin">📌</span>':''}<span class="di-name">${esc(d.name)}</span>
    <span class="di-status ${d.status}">${stTxt(d.status)}</span>
    <button class="di-dots" data-dots="${d.id}">⋮</button>
  </li>`).join("");
}

let menuId=null;
function doOnboard(){
  const v=$("#onboard-nick").value.trim();if(!v){toast(t("toast_nick_empty"));return;}
  Store.forceFirstNick(v);showScreen("home");renderHome();
}
function doCreate(){
  const v=$("#create-name").value.trim();const d=Store.create(v);closeModal("m-create");openCanvas(d.id);
}
function openCanvas(id){
  Store.setCur(id);showScreen("canvas");fillCanvasMeta(id);if(window.__renderCanvas)window.__renderCanvas(id);
}
function fillCanvasMeta(id){
  const d=Store.get(id);if(!d)return;
  $("#cv-dossier-name").textContent=d.name;
  const p=$("#cv-status-pill");p.className="status-pill "+d.status;p.textContent=stTxt(d.status);
  const u=Store.getUser();$("#cv-user-id").textContent=u.id;$("#cv-user-nick").textContent=u.nick||"—";
}
function openDossierMenu(id){
  menuId=id;const d=Store.get(id);const sp=$("#dm-pin").querySelector("span:last-child");
  if(sp)sp.textContent=d.pinned?t("toast_unpinned"):t("pin_dossier");openModal("m-dossier-menu");
}
let _cf=null;
function confirmDlg(text,fn){$("#cf-text").textContent=text;_cf=fn;openModal("m-confirm");}
function doConfirm(){closeModal("m-confirm");if(_cf){_cf();_cf=null;}}

// Настройки
function fillSettings(){
  const u=Store.getUser(),inp=$("#set-nick"),can=Store.canChangeNick();
  inp.value=u.nick||"";inp.disabled=!can;
  $("#set-nick-hint").textContent=can?t("onboard_hint").split(".")[0]:"🔒 "+t("toast_nick_locked")+" ("+Store.daysUntilNick()+"d)";
  const s=$("#set-lang");if(s)s.value=I18N_.getCur();
}
function tryEditNick(){
  if(!Store.canChangeNick()){toast(t("toast_nick_locked"));return;}
  const inp=$("#set-nick");inp.disabled=false;inp.focus();inp.select();
}
function commitNick(){
  const v=$("#set-nick").value.trim();if(!v){toast(t("toast_nick_empty"));fillSettings();return;}
  if(Store.setNick(v)){toast(t("toast_nick"));if($("#screen-canvas").classList.contains("active"))fillCanvasMeta(Store.getCur());}else toast(t("toast_nick_locked"));fillSettings();
}

// Привязка
document.addEventListener("click",e=>{
  const cl=e.target.closest("[data-close]");if(cl){closeModal(cl.closest(".modal"));return;}
  if(e.target.classList&&e.target.classList.contains("modal")){closeModal(e.target);return;}
  const dots=e.target.closest("[data-dots]");if(dots){openDossierMenu(dots.dataset.dots);return;}
  const st=e.target.closest("[data-status]");if(st){Store.setStatus(menuId,st.dataset.status);closeAllModals();renderHome();toast(t("toast_status"));return;}
  const tb=e.target.closest("[data-panel]");if(tb){const mp={blocks:"m-blocks",links:"m-links",tables:"m-tables"}[tb.dataset.panel];if(mp==="m-blocks")renderBlockPalette();openModal(mp);return;}
  const ad=e.target.closest("[data-add]");if(ad&&window.__addBlock){window.__addBlock(ad.dataset.add);return;}
  const di=e.target.closest(".dossier-item");if(di&&!e.target.closest("[data-dots]")){openCanvas(di.dataset.id);return;}
});
["#onboard-go",doOnboard].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#create-confirm",doCreate].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#cf-ok",doConfirm].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#cv-save-exit",()=>{const id=Store.getCur();if(id){const cs=window.__getCanvasState?window.__getCanvasState():Store.get(id).canvas;Store.saveCanvas(id,cs);}showScreen("home");renderHome();toast(t("toast_saved"));}].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#home-create",()=>{$("#create-name").value="";openModal("m-create");}].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#home-settings",()=>{fillSettings();openModal("m-settings");}].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#set-nick-edit",tryEditNick].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#set-lang-apply",()=>I18N_.setLang($("#set-lang").value)].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#dm-delete",()=>{closeModal("m-dossier-menu");confirmDlg(t("confirm_del_dossier"),()=>{Store.remove(menuId);renderHome();toast(t("toast_deleted"));});}].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#dm-pin",()=>{const d=Store.togglePin(menuId);closeModal("m-dossier-menu");renderHome();toast(d&&d.pinned?t("toast_pinned"):t("toast_unpinned"));}].forEach(([s,f])=>$(s)?.addEventListener("click",f));
["#dm-status",()=>{closeModal("m-dossier-menu");openModal("m-status");}].forEach(([s,f])=>$(s)?.addEventListener("click",f));

// Запуск
document.addEventListener("DOMContentLoaded",()=>{
  const u=Store.getUser();if(u.nick){showScreen("home");renderHome();}else{showScreen("onboard");$("#onboard-idline").textContent="ID: "+u.id;}
});
