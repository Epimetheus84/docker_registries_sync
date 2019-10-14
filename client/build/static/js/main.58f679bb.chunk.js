(this.webpackJsonpclient=this.webpackJsonpclient||[]).push([[0],{105:function(e,t,a){},106:function(e,t,a){"use strict";a.r(t);var n=a(0),s=a.n(n),l=a(8),r=a.n(l),i=(a(81),a(19)),c=a(13),o=a(24),m=a(25),g=a(29),u=a(35),h=a(30),d=a(22),v=a.n(d),f=a(20),p=a(145),E=a(134),y=a(141),b="*",S=function(e){function t(e){var a;return Object(i.a)(this,t),console.log(e),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).state={filteredImages:e.images,selectedRepo:b},a.selectRepo=a.selectRepo.bind(Object(f.a)(a)),a}return Object(g.a)(t,e),Object(c.a)(t,[{key:"selectRepo",value:function(e){var t=e.target.value,a=this.props.images;if(t!==b){var n={};n[t]=a[t],this.setState({filteredImages:n,selectedRepo:t})}else this.setState({filteredImages:a,selectedRepo:b})}},{key:"componentDidUpdate",value:function(e){e.images!==this.props.images&&this.setState({filteredImages:this.props.images})}},{key:"render",value:function(){var e=this.props,t=e.title,a=e.images,n=e.selected,l=e.handleChange,r=this.state,i=r.filteredImages,c=r.selectedRepo;return s.a.createElement(E.a,{className:"form-control"},s.a.createElement(p.a,{shrink:!0},t),s.a.createElement(y.a,{value:c,onChange:this.selectRepo,className:"select-repo"},s.a.createElement("option",{key:b,value:b},"\u0412\u0441\u0435 \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u0438"),Object.keys(a).map((function(e){return s.a.createElement("option",{key:e,value:e},e)}))),s.a.createElement(y.a,{multiple:!0,native:!0,value:n,onChange:l},Object.keys(i).map((function(e){return i[e].map((function(t){var a=e+":"+t;return s.a.createElement("option",{key:a,value:a},a)}))}))))}}]),t}(s.a.Component),C=a(139),R=a(64),D=a.n(R),k=a(44),w=a.n(k),O=a(63),W=a.n(O),j=a(66),_=a.n(j),I=function(e){function t(e){var a;return Object(i.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).state={srcImages:{},dstImages:{},selectedDev:[],selectedProd:[],semWaiting:2},a.getReposData(),a}return Object(g.a)(t,e),Object(c.a)(t,[{key:"getReposData",value:function(){var e=this;v.a.get("http://localhost:8080/api/images/src").then((function(t){var a=t.data;e.setState({srcImages:a,semWaiting:e.state.semWaiting-1})})).catch((function(t){console.log(t),e.setState({semWaiting:e.state.semWaiting-1})})),v.a.get("http://localhost:8080/api/images/dst").then((function(t){var a=t.data;e.setState({dstImages:a,semWaiting:e.state.semWaiting-1})})).catch((function(t){console.log(t),e.setState({semWaiting:e.state.semWaiting-1})}))}},{key:"handleChangeMultiple",value:function(e){for(var t=e.target.options,a=[],n=0,s=t.length;n<s;n+=1)t[n].selected&&a.push(t[n].value);return a}},{key:"moveImage",value:function(e){var t=this,a=this.state,n=a.selectedDev,s=a.selectedProd,l=n,r="dst";s.length>0&&(l=s,r="src"),0===l.length&&alert("Choose image(s)"),this.setState({semWaiting:2}),v.a.post("http://localhost:8080/api/move/to_"+r,{images:l}).then((function(e){t.getReposData()}))}},{key:"removeImage",value:function(){var e=this,t=this.state,a=t.selectedDev,n=t.selectedProd,s=a,l="src";n.length>0&&(s=n,l="dst"),0===s.length&&alert("Choose image(s)"),this.setState({semWaiting:2});var r=0,i=!0,c=!1,o=void 0;try{for(var m,g=function(){var t=m.value;v.a.post("http://localhost:8080/api/remove/"+l,{image:t}).then((function(a){var n=a.data;if("warning"!==n.status)++r===s.length&&e.getReposData();else{console.log(n);var i=n.duplicates.join("\n");!0===window.confirm("\u0412\u043d\u0438\u043c\u0430\u043d\u0438\u0435! \n\u0423\u0434\u0430\u043b\u0438\u0432 \u044d\u0442\u043e\u0442 \u0442\u0435\u0433, \u0432\u044b \u0442\u0430\u043a\u0436\u0435 \u0443\u0434\u0430\u043b\u0438\u0442\u0435 \u0435\u0433\u043e \u0434\u0443\u043f\u043b\u0438\u043a\u0430\u0442\u044b:\n"+i+"\n\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c?")?v.a.post("http://localhost:8080/api/remove/"+l,{image:t,force:1}).then((function(t){++r===s.length&&e.getReposData()})).catch((function(t){console.log(t),++r===s.length&&e.getReposData()})):++r===s.length&&e.getReposData()}})).catch((function(t){console.log(t),++r===s.length&&e.getReposData()}))},u=s[Symbol.iterator]();!(i=(m=u.next()).done);i=!0)g()}catch(h){c=!0,o=h}finally{try{i||null==u.return||u.return()}finally{if(c)throw o}}}},{key:"render",value:function(){var e=this,t=this.state,a=t.srcImages,n=t.dstImages,l=t.selectedDev,r=t.selectedProd,i=t.semWaiting;return console.log(i),s.a.createElement("div",{className:"App"},i>0&&s.a.createElement("div",{className:"preloader"},s.a.createElement("div",{className:"lds-ring"},s.a.createElement("div",null),s.a.createElement("div",null),s.a.createElement("div",null),s.a.createElement("div",null))),s.a.createElement("div",{className:"images-list"},s.a.createElement(S,{images:a,title:"src",selected:l,handleChange:function(t){e.setState({selectedProd:[],selectedDev:e.handleChangeMultiple(t)})}})),s.a.createElement("div",{className:"actions-list"},l.length>0&&s.a.createElement("div",{className:"button-wrapper"},s.a.createElement(C.a,{variant:"contained",color:"primary",onClick:function(){e.moveImage()},endIcon:s.a.createElement(W.a,null)},"\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043d\u0430 prod")),r.length>0&&s.a.createElement("div",{className:"button-wrapper"},s.a.createElement(C.a,{variant:"contained",color:"primary",onClick:function(){e.moveImage()},startIcon:s.a.createElement(w.a,null)},"\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043d\u0430 dev")),s.a.createElement("div",{className:"button-wrapper"},s.a.createElement(C.a,{variant:"contained",color:"secondary",onClick:function(){e.removeImage()},endIcon:s.a.createElement(D.a,null)},"\u0423\u0434\u0430\u043b\u0438\u0442\u044c"))),s.a.createElement("div",{className:"images-list"},s.a.createElement(S,{images:n,title:"dst",selected:r,handleChange:function(t){e.setState({selectedDev:[],selectedProd:e.handleChangeMultiple(t)})}})),s.a.createElement("div",{className:"settings-btn"},s.a.createElement(u.b,{to:"/settings"},s.a.createElement(_.a,null))))}}]),t}(s.a.Component),N=a(143),A=a(142),P=a(140),M=a(144),x=function(e){function t(e){var a;return Object(i.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).state={configs:{},saving:!1},v.a.get("/api/get_settings").then((function(e){a.setState({configs:e.data})})),a}return Object(g.a)(t,e),Object(c.a)(t,[{key:"handleChange",value:function(e,t,a){var n=this.state.configs;a?n[t][a]=e:n[t]=e,this.setState({configs:n})}},{key:"save",value:function(){var e=this;this.setState({saving:!0}),v.a.post("/api/save_settings",this.state.configs).then((function(t){e.setState({saving:!1})})).catch((function(t){e.setState({saving:!1}),alert(t)}))}},{key:"render",value:function(){var e=this,t=this.state.configs;return t.src_registry?s.a.createElement("form",{noValidate:!0,autoComplete:"off",className:"settings-form"},s.a.createElement("h2",null,"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0430\u0446\u0438\u0438"),s.a.createElement(P.a,{row:!0},s.a.createElement(N.a,{fullWidth:!0,id:"src_address",label:"SRC Address",value:t.src_registry.ADDRESS,onChange:function(t){e.handleChange(t.target.value,"src_registry","ADDRESS")},margin:"normal"})),s.a.createElement(P.a,{row:!0},s.a.createElement(N.a,{fullWidth:!0,id:"src_login",label:"SRC Auth username",value:t.src_registry.USERNAME,onChange:function(t){e.handleChange(t.target.value,"src_registry","USERNAME")},margin:"normal"})),s.a.createElement(P.a,{row:!0},s.a.createElement(N.a,{fullWidth:!0,id:"src_password",label:"SRC Password",value:t.src_registry.PASSWORD,onChange:function(t){e.handleChange(t.target.value,"src_registry","PASSWORD")},margin:"normal"})),s.a.createElement(P.a,{row:!0},s.a.createElement(N.a,{fullWidth:!0,id:"dst_address",label:"DST Address",value:t.dst_registry.ADDRESS,onChange:function(t){e.handleChange(t.target.value,"dst_registry","ADDRESS")},margin:"normal"})),s.a.createElement(P.a,{row:!0},s.a.createElement(N.a,{fullWidth:!0,id:"dst_username",label:"DST Auth username",value:t.dst_registry.USERNAME,onChange:function(t){e.handleChange(t.target.value,"dst_registry","USERNAME")},margin:"normal"})),s.a.createElement(P.a,{row:!0},s.a.createElement(N.a,{fullWidth:!0,id:"dst_password",label:"DST Password",value:t.dst_registry.PASSWORD,onChange:function(t){e.handleChange(t.target.value,"dst_registry","PASSWORD")},margin:"normal"})),s.a.createElement(P.a,{row:!0},s.a.createElement(N.a,{fullWidth:!0,id:"prefixes",label:"\u041f\u0440\u0435\u0444\u0438\u043a\u0441\u044b \u0442\u0435\u0433\u043e\u0432 \u0447\u0435\u0440\u0435\u0437 \u0437\u0430\u043f\u044f\u0442\u0443\u044e (\u043e\u0441\u0442\u0430\u0432\u044c\u0442\u0435 \u043f\u043e\u043b\u0435 \u043f\u0443\u0441\u0442\u044b\u043c, \u0435\u0441\u043b\u0438 \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0432\u0441\u0435 \u0442\u0435\u0433\u0438)",value:t.prefixes.join(", "),onChange:function(t){var a=t.target.value;a=a.split(", "),e.handleChange(a,"prefixes")},margin:"normal"})),s.a.createElement(P.a,{row:!0},s.a.createElement(M.a,{control:s.a.createElement(A.a,{checked:t.force_sync,onChange:function(t){e.handleChange(t.target.checked,"force_sync")},value:"force_sync",inputProps:{"aria-label":"primary checkbox"}}),label:"\u0423\u0434\u0430\u043b\u044f\u0442\u044c \u0434\u0443\u0431\u043b\u0438\u0440\u0443\u044e\u0449\u0438\u0435\u0441\u044f \u0442\u0435\u0433\u0438"})),s.a.createElement(C.a,{variant:"contained",color:"primary",onClick:function(){e.save()}},!1===this.state.saving?"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c":"\u0421\u043e\u0445\u0440\u0430\u043d\u044f\u0435\u0442\u0441\u044f..."),s.a.createElement(u.b,{to:"/",className:"return-btn"},s.a.createElement(C.a,{variant:"contained",color:"default",startIcon:s.a.createElement(w.a,null)},"\u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f"))):"Waiting..."}}]),t}(s.a.Component),U=(a(105),function(e){function t(){return Object(i.a)(this,t),Object(o.a)(this,Object(m.a)(t).apply(this,arguments))}return Object(g.a)(t,e),Object(c.a)(t,[{key:"render",value:function(){return s.a.createElement(u.a,null,s.a.createElement(h.c,null,s.a.createElement(h.a,{path:"/settings"},s.a.createElement(x,null)),s.a.createElement(h.a,{path:"/"},s.a.createElement(I,null))))}}]),t}(s.a.Component));Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));r.a.render(s.a.createElement(U,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))},76:function(e,t,a){e.exports=a(106)},81:function(e,t,a){}},[[76,1,2]]]);
//# sourceMappingURL=main.58f679bb.chunk.js.map