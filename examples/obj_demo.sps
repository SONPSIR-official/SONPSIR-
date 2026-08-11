визуал заголовок("Модель из obj")
визуал тема("тёмная")
визуал html_рус("
заголовок2 Кристалл из файла model.obj
блок id='box3d'
")
визуал html("<script src='three.min.js'></script>")
визуал скрипт("
function загрузить_модель(имя,цвет,колбэк){fetch(имя).then(function(r){return r.text();}).then(function(текст){var V=[],F=[];var строки=текст.split(String.fromCharCode(10));for(var i=0;i<строки.length;i++){var ч=строки[i].trim().split(/\s+/);if(ч[0]=='v'){V.push([parseFloat(ч[1]),parseFloat(ч[2]),parseFloat(ч[3])]);}if(ч[0]=='f'){F.push([parseInt(ч[1])-1,parseInt(ч[2])-1,parseInt(ч[3])-1]);}}var pos=new Float32Array(F.length*9);var k=0;for(var f=0;f<F.length;f++){var t=F[f];var p=[V[t[0]],V[t[1]],V[t[2]]];for(var j=0;j<3;j++){pos[k++]=p[j][0];pos[k++]=p[j][1];pos[k++]=p[j][2];}}var g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(pos,3));g.computeVertexNormals();колбэк(new THREE.Mesh(g,new THREE.MeshToonMaterial({color:цвет})));});}
")
визуал скрипт_рус("
пусть мир = сцена_создать('box3d')
пусть гр = группа()
добавить_в(мир, гр)
функция поставить(м)
    добавить_в(гр, м)
конец функции
загрузить_модель('kristal.obj', 'gold', поставить)
функция тик()
    поворот_y(гр, 0.02)
    отрисовать(мир)
    кадр(тик)
конец функции
тик()
")
визуал html("<h3 id='dbg'>загрузка...</h3>")
визуал скрипт("var d=document.getElementById('dbg');d.innerText='THREE: '+(typeof THREE)+' | загрузить_модель: '+(typeof загрузить_модель);fetch('kristal.obj').then(function(r){return r.text();}).then(function(t){d.innerText+=' | байт: '+t.length;});")
визуал скрипт("setTimeout(function(){var d=document.getElementById('dbg');d.innerText += ' | поворот: ' + (typeof window.поворот) + ' ' + window.поворот + ' | canvas: ' + document.getElementsByTagName('canvas').length;},2000);загрузить_модель('kristal.obj','gold',function(m){document.getElementById('dbg').innerText += ' | вершин: ' + m.geometry.attributes.position.count;});")
визуал показать()
