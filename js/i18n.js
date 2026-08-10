const I18N={};
I18N.ru={
  onboard_hint:"Введите авторский ник. Он будет проставлен в PDF-отчётах как подтверждение авторства. Сменить ник можно не чаще раза в 7 дней.",
  your_nick:"Ваш ник",enter:"Войти в студию",create_dossier:"Создать досье",my_dossiers:"МОИ ДОСЬЕ",
  no_dossiers:"Пока нет сохранённых досье. Создайте первое.",change_lang:"Сменить язык",settings:"Настройки",
  canvas_bg:"Выбор фона холста",user_nick:"Ник пользователя",interface_lang:"Язык интерфейса",
  save:"Сохранить",choose_lang:"Выберите язык",delete_dossier:"Удалить досье",pin_dossier:"Закрепить досье",
  change_status:"Изменить статус",st_work:"В работе",st_done:"Завершённый",st_closed:"Закрыт",
  add_block:"Добавить блок",links_title:"СВЯЗИ",link_type:"Выберите тип связи",red_thread:"Красная нить",
  no_arrow:"Без стрелки",arrow:"Стрелка",with_arrow:"С наконечником",link_style:"Выберите стиль (для стрелки)",
  solid:"Сплошная",dashed:"Пунктирная",dotted:"Битая",link_color:"Выберите цвет связи",
  cur_color:"Текущий цвет",create_link:"Создайте связь",link_hint:"Нажмите на первую точку блока, затем на вторую точку другого блока. Связь будет создана между ними.",
  start_link:"Начать соединение",table_size:"Размер таблицы",place_table:"Разместить таблицу",
  pick_color:"Выбор цвета (RGB)",link_signature:"ПОДПИСЬ СВЯЗИ",enter_signature:"Введите подпись для связи",
  delete_link:"Удалить связь",save_signature:"Сохранить подпись",confirm:"Подтверждение",confirm_yes:"Подтвердить",
  save_exit:"Сохраниться и выйти",dossier_label:"Досье:",mode_label:"Режим:",
  status_label:"Статус:",id_label:"ID:",nick_label:"Ник:",stat_events:"События",stat_links:"Связи",
  stat_subjects:"Субъекты",stat_objects:"Объекты",stat_analytics:"Аналитика",stat_trust:"Доверие",
  stat_warn:"Предупреждения",tab_blocks:"БЛОКИ",tab_links:"СВЯЗИ",tab_tables:"ТАБЛИЦЫ",
  enter_dossier_name:"Введите название досье",cancel:"Отмена",create:"Создать"
};
I18N.en={
  onboard_hint:"Enter your author nick. It will be stamped on PDF reports as proof of authorship. You can change it no more than once every 7 days.",
  your_nick:"Your nick",enter:"Enter the studio",create_dossier:"Create dossier",my_dossiers:"MY DOSSIERS",
  no_dossiers:"No saved dossiers yet. Create your first one.",change_lang:"Change language",settings:"Settings",
  canvas_bg:"Canvas background",user_nick:"User nick",interface_lang:"Interface language",
  save:"Save",choose_lang:"Choose language",delete_dossier:"Delete dossier",pin_dossier:"Pin dossier",
  change_status:"Change status",st_work:"In progress",st_done:"Completed",st_closed:"Closed",
  add_block:"Add block",links_title:"LINKS",link_type:"Choose link type",red_thread:"Red thread",
  no_arrow:"No arrow",arrow:"Arrow",with_arrow:"With arrowhead",link_style:"Choose style (for arrow)",
  solid:"Solid",dashed:"Dashed",dotted:"Dotted",link_color:"Choose link color",
  cur_color:"Current color",create_link:"Create link",link_hint:"Tap the first point on a block, then the second point on another block. The link will be created between them.",
  start_link:"Start linking",table_size:"Table size",place_table:"Place table",
  pick_color:"Pick color (RGB)",link_signature:"LINK SIGNATURE",enter_signature:"Enter signature for the link",
  delete_link:"Delete link",save_signature:"Save signature",confirm:"Confirmation",confirm_yes:"Confirm",
  save_exit:"Save & exit",dossier_label:"Dossier:",mode_label:"Mode:",
  status_label:"Status:",id_label:"ID:",nick_label:"Nick:",stat_events:"Events",stat_links:"Links",
  stat_subjects:"Subjects",stat_objects:"Objects",stat_analytics:"Analytics",stat_trust:"Trust",
  stat_warn:"Warnings",tab_blocks:"BLOCKS",tab_links:"LINKS",tab_tables:"TABLES",
  enter_dossier_name:"Enter dossier name",cancel:"Cancel",create:"Create"
};
const LANGS=[{c:"ru",n:"Русский"},{c:"en",n:"English"}];
let CUR=localStorage.getItem("son_lang")||"ru";
function t(k){const o=I18N[CUR];if(o&&o[k]!=null)return o[k];const e=I18N.en;return (e&&e[k]!=null)?e[k]:k;}
function applyI18n(){
  document.querySelectorAll("[data-i18n]").forEach(el=>{el.textContent=t(el.getAttribute("data-i18n"));});
  document.documentElement.lang=CUR;
}
function buildLangUI(){
  const sel=document.getElementById("set-lang");
  if(sel)sel.innerHTML=LANGS.map(l=>`<option value="${l.c}"${l.c===CUR?" selected":""}>${l.n}</option>`).join("");
}
function setLang(c){CUR=c;localStorage.setItem("son_lang",c);applyI18n();buildLangUI();}
window.I18N_={t,applyI18n,setLang,buildLangUI,getCur:()=>CUR,LANGS};
applyI18n();buildLangUI();
