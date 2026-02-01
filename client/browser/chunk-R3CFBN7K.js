import{a as Ae,b as ze}from"./chunk-YXO7NP6B.js";import{d as Te,f as Ie}from"./chunk-2Q77SCRP.js";import{b as je}from"./chunk-2EKU6FZ4.js";import{b as Re}from"./chunk-FVGKTF52.js";import{a as He}from"./chunk-DGOXWP7O.js";import{a as Ue}from"./chunk-B2CXB3HZ.js";import{b as $e,c as Le}from"./chunk-EG54LRXD.js";import{$a as xe,$b as ce,Bb as F,Bc as Me,Cb as m,Db as Y,Eb as J,Ec as te,Fb as be,Gb as Ce,Gc as Se,Hb as X,Ia as ve,Ib as q,Ic as De,Jc as Ee,Kc as I,La as r,Mb as we,Nb as W,Ob as Z,P as N,Pb as b,Pe as Ne,Q as V,Qb as s,Qe as Ve,Rb as D,Rd as Fe,Re as Be,S as B,Sb as E,Sd as k,Tc as Pe,U as g,Vd as H,Xb as L,Xd as ne,Ya as T,Z as O,Za as j,_ as M,a as ae,ab as A,b as le,bb as z,cb as K,ec as G,fc as ke,gc as ee,ia as P,ib as R,ja as fe,la as he,lb as C,ma as S,mb as w,nb as de,ob as se,pb as u,pe as U,qb as a,qe as Q,rb as l,rc as Oe,re as _,sb as h,se as ie,wb as _e,xb as ye,zb as $}from"./chunk-ESYVRVYB.js";var Qe=`
    .p-tag {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: dt('tag.primary.background');
        color: dt('tag.primary.color');
        font-size: dt('tag.font.size');
        font-weight: dt('tag.font.weight');
        padding: dt('tag.padding');
        border-radius: dt('tag.border.radius');
        gap: dt('tag.gap');
    }

    .p-tag-icon {
        font-size: dt('tag.icon.size');
        width: dt('tag.icon.size');
        height: dt('tag.icon.size');
    }

    .p-tag-rounded {
        border-radius: dt('tag.rounded.border.radius');
    }

    .p-tag-success {
        background: dt('tag.success.background');
        color: dt('tag.success.color');
    }

    .p-tag-info {
        background: dt('tag.info.background');
        color: dt('tag.info.color');
    }

    .p-tag-warn {
        background: dt('tag.warn.background');
        color: dt('tag.warn.color');
    }

    .p-tag-danger {
        background: dt('tag.danger.background');
        color: dt('tag.danger.color');
    }

    .p-tag-secondary {
        background: dt('tag.secondary.background');
        color: dt('tag.secondary.color');
    }

    .p-tag-contrast {
        background: dt('tag.contrast.background');
        color: dt('tag.contrast.color');
    }
`;var lt=["icon"],dt=["*"];function st(e,i){if(e&1&&h(0,"span",4),e&2){let t=m(2);b(t.cx("icon")),u("ngClass",t.icon)("pBind",t.ptm("icon"))}}function ct(e,i){if(e&1&&(_e(0),K(1,st,1,4,"span",3),ye()),e&2){let t=m();r(),u("ngIf",t.icon)}}function pt(e,i){}function ut(e,i){e&1&&K(0,pt,0,0,"ng-template")}function mt(e,i){if(e&1&&(a(0,"span",2),K(1,ut,1,0,null,5),l()),e&2){let t=m();b(t.cx("icon")),u("pBind",t.ptm("icon")),r(),u("ngTemplateOutlet",t.iconTemplate||t._iconTemplate)}}var gt={root:({instance:e})=>["p-tag p-component",{"p-tag-info":e.severity==="info","p-tag-success":e.severity==="success","p-tag-warn":e.severity==="warn","p-tag-danger":e.severity==="danger","p-tag-secondary":e.severity==="secondary","p-tag-contrast":e.severity==="contrast","p-tag-rounded":e.rounded}],icon:"p-tag-icon",label:"p-tag-label"},Ke=(()=>{class e extends H{name="tag";style=Qe;classes=gt;static \u0275fac=(()=>{let t;return function(n){return(t||(t=S(e)))(n||e)}})();static \u0275prov=N({token:e,factory:e.\u0275fac})}return e})();var Xe=new B("TAG_INSTANCE"),pe=(()=>{class e extends Q{$pcTag=g(Xe,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=g(_,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;severity;value;icon;rounded;iconTemplate;templates;_iconTemplate;_componentStyle=g(Ke);onAfterContentInit(){this.templates?.forEach(t=>{switch(t.getType()){case"icon":this._iconTemplate=t.template;break}})}get dataP(){return this.cn({rounded:this.rounded,[this.severity]:this.severity})}static \u0275fac=(()=>{let t;return function(n){return(t||(t=S(e)))(n||e)}})();static \u0275cmp=T({type:e,selectors:[["p-tag"]],contentQueries:function(o,n,d){if(o&1&&be(d,lt,4)(d,Fe,4),o&2){let c;X(c=q())&&(n.iconTemplate=c.first),X(c=q())&&(n.templates=c)}},hostVars:3,hostBindings:function(o,n){o&2&&(R("data-p",n.dataP),b(n.cn(n.cx("root"),n.styleClass)))},inputs:{styleClass:"styleClass",severity:"severity",value:"value",icon:"icon",rounded:[2,"rounded","rounded",Oe]},features:[L([Ke,{provide:Xe,useExisting:e},{provide:U,useExisting:e}]),A([_]),z],ngContentSelectors:dt,decls:5,vars:6,consts:[[4,"ngIf"],[3,"class","pBind",4,"ngIf"],[3,"pBind"],[3,"class","ngClass","pBind",4,"ngIf"],[3,"ngClass","pBind"],[4,"ngTemplateOutlet"]],template:function(o,n){o&1&&(Y(),J(0),K(1,ct,2,1,"ng-container",0)(2,mt,2,4,"span",1),a(3,"span",2),s(4),l()),o&2&&(r(),u("ngIf",!n.iconTemplate&&!n._iconTemplate),r(),u("ngIf",n.iconTemplate||n._iconTemplate),r(),b(n.cx("label")),u("pBind",n.ptm("label")),r(),D(n.value))},dependencies:[I,te,Se,De,k,_],encapsulation:2,changeDetection:0})}return e})(),We=(()=>{class e{static \u0275fac=function(o){return new(o||e)};static \u0275mod=j({type:e});static \u0275inj=V({imports:[pe,k,k]})}return e})();var re=class e{statusMap={packing:"\u0110ang \u0111\xF3ng g\xF3i",packed:"\u0110\xF3ng g\xF3i xong",shipping:"\u0110ang v\u1EADn chuy\u1EC3n",closed:"Ho\xE0n th\xE0nh",cancelled:"\u0110\xE3 h\u1EE7y",pending:"Ch\u1EDD x\u1EED l\xFD",timeout:"H\u1EBFt gi\u1EDD (Timeout)"};transform(i){if(!i)return"Kh\xF4ng x\xE1c \u0111\u1ECBnh";let t=i.toLowerCase();return this.statusMap[t]||i}static \u0275fac=function(t){return new(t||e)};static \u0275pipe=xe({name:"orderStatus",type:e,pure:!0})};var Ge=`
    .p-divider-horizontal {
        display: flex;
        width: 100%;
        position: relative;
        align-items: center;
        margin: dt('divider.horizontal.margin');
        padding: dt('divider.horizontal.padding');
    }

    .p-divider-horizontal:before {
        position: absolute;
        display: block;
        inset-block-start: 50%;
        inset-inline-start: 0;
        width: 100%;
        content: '';
        border-block-start: 1px solid dt('divider.border.color');
    }

    .p-divider-horizontal .p-divider-content {
        padding: dt('divider.horizontal.content.padding');
    }

    .p-divider-vertical {
        min-height: 100%;
        display: flex;
        position: relative;
        justify-content: center;
        margin: dt('divider.vertical.margin');
        padding: dt('divider.vertical.padding');
    }

    .p-divider-vertical:before {
        position: absolute;
        display: block;
        inset-block-start: 0;
        inset-inline-start: 50%;
        height: 100%;
        content: '';
        border-inline-start: 1px solid dt('divider.border.color');
    }

    .p-divider.p-divider-vertical .p-divider-content {
        padding: dt('divider.vertical.content.padding');
    }

    .p-divider-content {
        z-index: 1;
        background: dt('divider.content.background');
        color: dt('divider.content.color');
    }

    .p-divider-solid.p-divider-horizontal:before {
        border-block-start-style: solid;
    }

    .p-divider-solid.p-divider-vertical:before {
        border-inline-start-style: solid;
    }

    .p-divider-dashed.p-divider-horizontal:before {
        border-block-start-style: dashed;
    }

    .p-divider-dashed.p-divider-vertical:before {
        border-inline-start-style: dashed;
    }

    .p-divider-dotted.p-divider-horizontal:before {
        border-block-start-style: dotted;
    }

    .p-divider-dotted.p-divider-vertical:before {
        border-inline-start-style: dotted;
    }

    .p-divider-left:dir(rtl),
    .p-divider-right:dir(rtl) {
        flex-direction: row-reverse;
    }
`;var ht=["*"],vt={root:({instance:e})=>({justifyContent:e.layout==="horizontal"?e.align==="center"||e.align==null?"center":e.align==="left"?"flex-start":e.align==="right"?"flex-end":null:null,alignItems:e.layout==="vertical"?e.align==="center"||e.align==null?"center":e.align==="top"?"flex-start":e.align==="bottom"?"flex-end":null:null})},xt={root:({instance:e})=>["p-divider p-component","p-divider-"+e.layout,"p-divider-"+e.type,{"p-divider-left":e.layout==="horizontal"&&(!e.align||e.align==="left")},{"p-divider-center":e.layout==="horizontal"&&e.align==="center"},{"p-divider-right":e.layout==="horizontal"&&e.align==="right"},{"p-divider-top":e.layout==="vertical"&&e.align==="top"},{"p-divider-center":e.layout==="vertical"&&(!e.align||e.align==="center")},{"p-divider-bottom":e.layout==="vertical"&&e.align==="bottom"}],content:"p-divider-content"},Ye=(()=>{class e extends H{name="divider";style=Ge;classes=xt;inlineStyles=vt;static \u0275fac=(()=>{let t;return function(n){return(t||(t=S(e)))(n||e)}})();static \u0275prov=N({token:e,factory:e.\u0275fac})}return e})();var Je=new B("DIVIDER_INSTANCE"),_t=(()=>{class e extends Q{$pcDivider=g(Je,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=g(_,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;layout="horizontal";type="solid";align;_componentStyle=g(Ye);get dataP(){return this.cn({[this.align]:this.align,[this.layout]:this.layout,[this.type]:this.type})}static \u0275fac=(()=>{let t;return function(n){return(t||(t=S(e)))(n||e)}})();static \u0275cmp=T({type:e,selectors:[["p-divider"]],hostAttrs:["role","separator"],hostVars:6,hostBindings:function(o,n){o&2&&(R("aria-orientation",n.layout)("data-p",n.dataP),Z(n.sx("root")),b(n.cn(n.cx("root"),n.styleClass)))},inputs:{styleClass:"styleClass",layout:"layout",type:"type",align:"align"},features:[L([Ye,{provide:Je,useExisting:e},{provide:U,useExisting:e}]),A([_]),z],ngContentSelectors:ht,decls:2,vars:3,consts:[[3,"pBind"]],template:function(o,n){o&1&&(Y(),a(0,"div",0),J(1),l()),o&2&&(b(n.cx("content")),u("pBind",n.ptm("content")))},dependencies:[I,k,ie,_],encapsulation:2,changeDetection:0})}return e})(),Ze=(()=>{class e{static \u0275fac=function(o){return new(o||e)};static \u0275mod=j({type:e});static \u0275inj=V({imports:[_t,ie,ie]})}return e})();var et=`
    .p-skeleton {
        display: block;
        overflow: hidden;
        background: dt('skeleton.background');
        border-radius: dt('skeleton.border.radius');
    }

    .p-skeleton::after {
        content: '';
        animation: p-skeleton-animation 1.2s infinite;
        height: 100%;
        left: 0;
        position: absolute;
        right: 0;
        top: 0;
        transform: translateX(-100%);
        z-index: 1;
        background: linear-gradient(90deg, rgba(255, 255, 255, 0), dt('skeleton.animation.background'), rgba(255, 255, 255, 0));
    }

    [dir='rtl'] .p-skeleton::after {
        animation-name: p-skeleton-animation-rtl;
    }

    .p-skeleton-circle {
        border-radius: 50%;
    }

    .p-skeleton-animation-none::after {
        animation: none;
    }

    @keyframes p-skeleton-animation {
        from {
            transform: translateX(-100%);
        }
        to {
            transform: translateX(100%);
        }
    }

    @keyframes p-skeleton-animation-rtl {
        from {
            transform: translateX(100%);
        }
        to {
            transform: translateX(-100%);
        }
    }
`;var yt={root:{position:"relative"}},bt={root:({instance:e})=>["p-skeleton p-component",{"p-skeleton-circle":e.shape==="circle","p-skeleton-animation-none":e.animation==="none"}]},tt=(()=>{class e extends H{name="skeleton";style=et;classes=bt;inlineStyles=yt;static \u0275fac=(()=>{let t;return function(n){return(t||(t=S(e)))(n||e)}})();static \u0275prov=N({token:e,factory:e.\u0275fac})}return e})();var nt=new B("SKELETON_INSTANCE"),ue=(()=>{class e extends Q{$pcSkeleton=g(nt,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=g(_,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;shape="rectangle";animation="wave";borderRadius;size;width="100%";height="1rem";_componentStyle=g(tt);get containerStyle(){let t=this._componentStyle?.inlineStyles.root,o;return this.$unstyled()||(this.size?o=le(ae({},t),{width:this.size,height:this.size,borderRadius:this.borderRadius}):o=le(ae({},t),{width:this.width,height:this.height,borderRadius:this.borderRadius})),o}get dataP(){return this.cn({[this.shape]:this.shape})}static \u0275fac=(()=>{let t;return function(n){return(t||(t=S(e)))(n||e)}})();static \u0275cmp=T({type:e,selectors:[["p-skeleton"]],hostVars:6,hostBindings:function(o,n){o&2&&(R("aria-hidden",!0)("data-p",n.dataP),Z(n.containerStyle),b(n.cn(n.cx("root"),n.styleClass)))},inputs:{styleClass:"styleClass",shape:"shape",animation:"animation",borderRadius:"borderRadius",size:"size",width:"width",height:"height"},features:[L([tt,{provide:nt,useExisting:e},{provide:U,useExisting:e}]),A([_]),z],decls:0,vars:0,template:function(o,n){},dependencies:[I,k],encapsulation:2,changeDetection:0})}return e})(),it=(()=>{class e{static \u0275fac=function(o){return new(o||e)};static \u0275mod=j({type:e});static \u0275inj=V({imports:[ue,k,k]})}return e})();var wt=["videoPlayer"],kt=(e,i,t)=>({"bg-white shadow-2 border-primary":e,"surface-0 border-transparent text-500 hover:surface-200":i,"opacity-70":t}),Ot=(e,i,t)=>({"bg-green-50 border-green-200 text-green-600":e,"bg-red-50 border-red-200 text-red-600":i,"bg-blue-50 border-blue-200 text-blue-600":t}),rt=(e,i)=>i.id;function Mt(e,i){if(e&1){let t=$();a(0,"div",2)(1,"p-button",5),F("click",function(){O(t);let n=m();return M(n.goBack())}),l(),a(2,"div")(3,"h2",6),s(4,"Chi ti\u1EBFt \u0111\u01A1n h\xE0ng"),l(),a(5,"span",7),s(6,"M\xE3: "),a(7,"strong",8),s(8),l()()()()}if(e&2){let t,o=m();r(),u("rounded",!0)("text",!0),r(7),D((t=o.selectedOrder())==null?null:t.code)}}function St(e,i){e&1&&(a(0,"div",3),h(1,"p-skeleton",9)(2,"p-skeleton",10),l())}function Dt(e,i){if(e&1){let t=$();a(0,"video",33,0),F("play",function(){O(t);let n=m(2);return M(n.onVideoPlay())})("pause",function(){O(t);let n=m(2);return M(n.onVideoPause())})("ended",function(){O(t);let n=m(2);return M(n.onVideoEnded())}),l()}if(e&2){let t=m(2);u("src",t.getFullUrl(t.selectedOrder().path_video),ve)}}function Et(e,i){e&1&&(a(0,"div",14),h(1,"i",34),a(2,"span"),s(3,"Kh\xF4ng c\xF3 video"),l()())}function Pt(e,i){e&1&&h(0,"div",45)}function Tt(e,i){e&1&&(a(0,"div",46),h(1,"i",47),l())}function It(e,i){if(e&1){let t=$();a(0,"div",37),F("click",function(){let n=O(t).$implicit,d=m(3);return M(d.handleItemClick(n))}),a(1,"div",38),h(2,"i",39),l(),a(3,"div",40)(4,"span",41),s(5),l(),a(6,"div",42)(7,"span",43),s(8),l(),a(9,"span",44),s(10),G(11,"date"),l()()(),C(12,Pt,1,0,"div",45),l(),C(13,Tt,2,0,"div",46)}if(e&2){let t,o,n,d=i.$implicit,c=i.$index,v=i.$count,y=m(3);u("ngClass",ce(14,kt,((t=y.selectedOrder())==null?null:t.id)===d.id,((t=y.selectedOrder())==null?null:t.id)!==d.id,((t=y.selectedOrder())==null?null:t.id)!==d.id&&!d.parent_id)),r(),u("ngClass",d.parent_id?"bg-orange-100 text-orange-600":"bg-blue-50 text-blue-600"),r(),u("ngClass",d.parent_id?"pi-replay":"pi-box"),r(2),W("text-900",((o=y.selectedOrder())==null?null:o.id)===d.id),r(),E(" ",d.code," "),r(2),u("ngClass",d.parent_id?"text-orange-600":"text-blue-600"),r(),E(" ",d.parent_id?"Ho\xE0n/\u0110\xF3ng l\u1EA1i":"\u0110\u01A1n g\u1ED1c"," "),r(2),E("\u2022 ",ee(11,11,d.created_at,"HH:mm")),r(2),w(((n=y.selectedOrder())==null?null:n.id)===d.id?12:-1),r(),w(c!==v-1?13:-1)}}function Ft(e,i){if(e&1&&(a(0,"div",25)(1,"div",35)(2,"span",36),s(3,"Quy tr\xECnh:"),l(),de(4,It,14,18,null,null,rt),l()()),e&2){let t=m(2);r(4),se(t.orderList().slice().reverse())}}function Nt(e,i){e&1&&(a(0,"span",57),h(1,"i",65),s(2," \u0110\xF3ng l\u1EA1i "),l())}function Vt(e,i){if(e&1&&(a(0,"div",63),h(1,"i",66),a(2,"span",67),s(3),l()()),e&2){let t=m().$implicit;r(3),D(t.note)}}function Bt(e,i){e&1&&(a(0,"div",64),h(1,"div",68)(2,"div",68)(3,"div",68),l())}function jt(e,i){if(e&1){let t=$();a(0,"div",48),F("click",function(){let n=O(t).$implicit,d=m(2);return M(d.handleItemClick(n))}),a(1,"div",49)(2,"div",50),h(3,"div",51)(4,"i",52),l(),a(5,"div",53)(6,"div",54)(7,"div",55)(8,"span",56),s(9),l(),C(10,Nt,3,0,"span",57),l(),a(11,"div",58),h(12,"i",59),a(13,"span",60),s(14),l()()(),a(15,"div",61)(16,"span"),h(17,"i",62),s(18),G(19,"date"),l(),a(20,"span"),s(21),l()()()(),C(22,Vt,4,1,"div",63),C(23,Bt,4,0,"div",64),l()}if(e&2){let t,o,n,d,c,v,y,f,me,ge,p=i.$implicit,x=m(2);W("bg-blue-50",((t=x.selectedOrder())==null?null:t.id)===p.id)("border-blue-500",((o=x.selectedOrder())==null?null:o.id)===p.id)("surface-card",((n=x.selectedOrder())==null?null:n.id)!==p.id)("border-transparent",((d=x.selectedOrder())==null?null:d.id)!==p.id)("shadow-1",((c=x.selectedOrder())==null?null:c.id)!==p.id),r(2),we("background-image","url("+x.getFullUrl(p.path_avatar)+")"),r(2),W("pi-pause",((v=x.selectedOrder())==null?null:v.id)===p.id&&x.isPlaying())("pi-play",((y=x.selectedOrder())==null?null:y.id)!==p.id||!x.isPlaying())("text-2xl",((f=x.selectedOrder())==null?null:f.id)===p.id),r(4),W("text-primary",((me=x.selectedOrder())==null?null:me.id)===p.id),r(),E(" ",p.code," "),r(),w(p.parent_id?10:-1),r(),u("ngClass",ce(33,Ot,p.status==="packed",p.status==="cancelled",p.status==="processing")),r(),b(x.getStatusIcon(p.status)),r(2),D(p.status),r(4),D(ee(19,30,p.created_at,"HH:mm dd/MM")),r(3),E("#",p.id),r(),w(p.note?22:-1),r(),w(((ge=x.selectedOrder())==null?null:ge.id)===p.id&&x.isPlaying()?23:-1)}}function At(e,i){if(e&1){let t=$();a(0,"div",4)(1,"div",11)(2,"div",12),C(3,Dt,2,1,"video",13)(4,Et,4,0,"div",14),l(),a(5,"div",15)(6,"div",16),h(7,"p-avatar",17),a(8,"div")(9,"div",18),s(10),l(),a(11,"div",19),s(12),G(13,"date"),l()()(),a(14,"div",20)(15,"div",21)(16,"button",22),F("click",function(n){O(t);let d=m();return M(d.downloadVideo(d.selectedOrder(),n))}),l(),h(17,"p-tag",23),G(18,"orderStatus"),l(),a(19,"div",24),s(20),l()()(),C(21,Ft,6,0,"div",25),l(),a(22,"div",26)(23,"div",27)(24,"div",21)(25,"span"),s(26),l(),a(27,"i",28),F("click",function(){O(t);let n=m();return M(n.downloadAllVideos())}),l()(),a(28,"span",29),s(29),l()(),a(30,"div",30)(31,"div",31),de(32,jt,24,37,"div",32,rt),l()()()()}if(e&2){let t,o,n,d,c,v,y,f=m();r(3),w((t=f.selectedOrder())!=null&&t.path_video?3:4),r(4),u("image",f.getFullUrl((o=f.selectedOrder())==null?null:o.path_avatar)),r(3),E("NV: ",((n=f.selectedOrder())==null?null:n.packer_name)||"#"+((n=f.selectedOrder())==null?null:n.user_id)),r(2),D(ee(13,10,(d=f.selectedOrder())==null?null:d.closed_at,"HH:mm dd/MM/yyyy")),r(5),u("value",ke(18,13,(c=f.selectedOrder())==null?null:c.status))("severity",f.getSeverity((v=f.selectedOrder())==null?null:v.status)),r(3),E("Cam: ",(y=f.selectedOrder())==null?null:y.camera_id),r(),w(f.orderList().length>0?21:-1),r(5),E("L\u1ECBch s\u1EED (",f.orderList().length,")"),r(3),D(f.durationString()),r(3),se(f.orderList())}}var ot=class e{inputCode=null;isDialogMode=!1;videoPlayer;route=g(Te);router=g(Ie);orderService=g(He);location=g(Me);http=g(Pe);settingsService=g(Ue);loading=P(!0);isDownloading=P(!1);orderList=P([]);selectedOrder=P(null);isPlaying=P(!1);durationString=P("");aspectRatio=P("16 / 9");constructor(){fe(()=>{let i=this.selectedOrder();i&&this.calculateDuration(i.start_at,i.closed_at)})}ngOnInit(){if(this.settingsService.getSettings().subscribe({next:i=>{let t=Number(i.camera_width),o=Number(i.camera_height);!isNaN(t)&&!isNaN(o)&&t>0&&o>0&&this.aspectRatio.set(`${t} / ${o}`)},error:i=>console.warn("Kh\xF4ng th\u1EC3 t\u1EA3i settings, d\xF9ng t\u1EC9 l\u1EC7 m\u1EB7c \u0111\u1ECBnh.",i)}),this.inputCode)this.fetchOrders(this.inputCode);else{let i=this.route.snapshot.paramMap.get("code");i&&this.fetchOrders(i)}}ngOnChanges(i){i.inputCode&&!i.inputCode.firstChange&&this.inputCode&&this.fetchOrders(this.inputCode)}fetchOrders(i){this.loading.set(!0),this.orderService.getOrders({code:i,page:1,page_size:100}).subscribe({next:t=>{let o=t.data||{},n=o.items||[];!n.length&&Array.isArray(o)?n=o:!n.length&&o.data&&Array.isArray(o.data)&&(n=o.data),this.orderList.set(n);let d=this.route.snapshot.queryParamMap.get("playId"),c=null;if(d&&n.length>0){let v=Number(d);c=n.find(y=>y.id===v)}!c&&n.length>0&&(c=n[0]),c&&this.selectOrder(c,!0),this.loading.set(!1)},error:t=>{console.error("Order Detail API Error:",t),this.orderList.set([]),this.loading.set(!1)}})}handleItemClick(i){this.selectedOrder()?.id===i.id?this.toggleVideoState():this.selectOrder(i,!0)}selectOrder(i,t=!1){this.selectedOrder.set(i),this.isPlaying.set(!1),t&&this.videoPlayer&&setTimeout(()=>{let o=this.videoPlayer.nativeElement;o.load(),o.play().catch(()=>{})},100)}toggleVideoState(){if(!this.videoPlayer)return;let i=this.videoPlayer.nativeElement;i.paused?i.play():i.pause()}onVideoPlay(){this.isPlaying.set(!0)}onVideoPause(){this.isPlaying.set(!1)}onVideoEnded(){this.isPlaying.set(!1)}downloadVideo(i,t){if(t&&t.stopPropagation(),!i?.path_video)return;this.isDownloading.set(!0);let o=this.getFullUrl(i.path_video),n=`${i.code}_${i.id}.mp4`;this.http.get(o,{responseType:"blob"}).subscribe({next:d=>{let c=URL.createObjectURL(d),v=document.createElement("a");v.href=c,v.download=n,document.body.appendChild(v),v.click(),document.body.removeChild(v),URL.revokeObjectURL(c),this.isDownloading.set(!1)},error:d=>{console.error("L\u1ED7i khi t\u1EA3i video:",d),this.isDownloading.set(!1),window.open(o,"_blank")}})}downloadAllVideos(){let i=this.orderList();if(!i||i.length===0||!confirm(`T\u1EA3i xu\u1ED1ng ${i.length} video?`))return;let t=0;i.forEach(o=>{o.path_video&&(setTimeout(()=>{this.downloadVideo(o)},t),t+=1500)})}getFullUrl(i){if(!i)return"";if(i.startsWith("http"))return i;let t=ne.apiUrl.endsWith("/")?ne.apiUrl.slice(0,-1):ne.apiUrl,o=i.startsWith("/")?i:`/${i}`;return`${t}${o}`}calculateDuration(i,t){if(!i||!t){this.durationString.set("--:--");return}let o=Math.floor((new Date(t).getTime()-new Date(i).getTime())/1e3),n=Math.floor(o/60),d=o%60;this.durationString.set(`${n}p ${d}s`)}getStatusIcon(i){switch(i?.toLowerCase()){case"packed":return"pi pi-check-circle";case"cancelled":return"pi pi-times-circle";case"processing":return"pi pi-spin pi-spinner";default:return"pi pi-info-circle"}}getSeverity(i){switch(i?.toLowerCase()){case"packed":return"success";case"cancelled":return"danger";case"processing":return"info";default:return"warn"}}goBack(){this.isDialogMode||(window.history.length>1?this.location.back():this.router.navigate(["/"]))}static \u0275fac=function(t){return new(t||e)};static \u0275cmp=T({type:e,selectors:[["app-order-detail"]],viewQuery:function(t,o){if(t&1&&Ce(wt,5),t&2){let n;X(n=q())&&(o.videoPlayer=n.first)}},inputs:{inputCode:"inputCode",isDialogMode:"isDialogMode"},features:[he],decls:4,vars:2,consts:[["videoPlayer",""],[1,"detail-wrapper","flex","flex-column","h-full","overflow-hidden","bg-white"],[1,"flex-none","flex","align-items-center","gap-3","p-3","border-bottom-1","surface-border"],[1,"flex-grow-1","p-3","flex","flex-column","gap-3"],[1,"flex","flex-column","lg:flex-row","min-h-0"],["icon","pi pi-arrow-left",3,"click","rounded","text"],[1,"m-0","font-bold","text-lg"],[1,"text-500","text-sm"],[1,"text-primary"],["height","300px","styleClass","w-full border-round"],["height","100px","styleClass","w-full border-round"],[1,"lg:w-9","flex","flex-column","bg-black-alpha-90","relative","overflow-hidden"],[1,"video-area","flex","align-items-center","justify-content-center","relative"],["controls","","autoplay","",1,"w-full","h-full",2,"max-height","100%","object-fit","contain",3,"src"],[1,"text-white-alpha-60","flex","flex-column","align-items-center"],[1,"info-bar","flex-none","p-3","surface-0","border-top-1","surface-border","flex","justify-content-between","align-items-center"],[1,"flex","align-items-center","gap-3"],["shape","circle","size","large","styleClass","border-1 surface-border",3,"image"],[1,"font-bold","text-900","line-height-2"],[1,"text-sm","text-500"],[1,"flex","flex-column","align-items-end","gap-1"],[1,"flex","align-items-center","gap-2"],["pButton","","icon","pi pi-download","pTooltip","T\u1EA3i video n\xE0y","tooltipPosition","left",1,"p-button-rounded","p-button-text","p-button-secondary","w-2rem","h-2rem",3,"click"],[3,"value","severity"],[1,"text-xs","text-500"],[1,"timeline-container","w-full","px-3","pt-4","pb-3","surface-50","border-top-1","surface-border","overflow-x-auto","custom-scrollbar"],[1,"flex-none","h-20rem","lg:h-auto","lg:w-3","surface-50","border-left-1","surface-border","flex","flex-column"],[1,"p-3","font-bold","text-700","border-bottom-1","surface-border","flex","justify-content-between","align-items-center"],["pTooltip","T\u1EA3i t\u1EA5t c\u1EA3 video",1,"pi","pi-download","text-primary","cursor-pointer","hover:text-primary-700","transition-colors",3,"click"],[1,"text-sm","font-normal","text-primary"],[1,"flex-grow-1","overflow-y-auto","custom-scrollbar"],[1,"flex","flex-column","p-2","gap-2","list-xxx"],[1,"p-2","border-round","border-1","transition-colors","transition-duration-150","flex","flex-column","gap-2","cursor-pointer","group",3,"bg-blue-50","border-blue-500","surface-card","border-transparent","shadow-1"],["controls","","autoplay","",1,"w-full","h-full",2,"max-height","100%","object-fit","contain",3,"play","pause","ended","src"],[1,"pi","pi-video-slash","text-5xl","mb-2"],[1,"flex","align-items-center","gap-2",2,"min-width","max-content"],[1,"text-xs","font-bold","text-500","uppercase","mr-2","flex-shrink-0"],[1,"timeline-node","relative","flex","align-items-center","gap-2","p-2","border-round-xl","cursor-pointer","transition-all","transition-duration-200","border-1",3,"click","ngClass"],[1,"w-2rem","h-2rem","border-circle","flex","align-items-center","justify-content-center","flex-shrink-0",3,"ngClass"],[1,"pi","text-sm",3,"ngClass"],[1,"flex","flex-column","justify-content-center"],[1,"text-xs","font-bold","white-space-nowrap"],[1,"flex","align-items-center","gap-1","white-space-nowrap"],[1,"text-[10px]","font-medium",3,"ngClass"],[1,"text-[10px]","text-400"],[1,"active-indicator"],[1,"flex","align-items-center","justify-content-center","px-1"],[1,"pi","pi-arrow-right","text-300","text-xs"],[1,"p-2","border-round","border-1","transition-colors","transition-duration-150","flex","flex-column","gap-2","cursor-pointer","group",3,"click"],[1,"flex","gap-3","align-items-start","list-item"],[1,"relative","w-4rem","h-3rem","border-round","overflow-hidden","flex-shrink-0","flex","align-items-center","justify-content-center","bg-cover","bg-center","shadow-1","mt-1"],[1,"absolute","top-0","left-0","w-full","h-full","bg-black-alpha-40"],[1,"pi","text-white","text-xl","relative","z-1","transition-all"],[1,"flex","flex-column","flex-grow-1","min-w-0"],[1,"flex","justify-content-between","align-items-start","mb-1"],[1,"flex","flex-column"],[1,"font-bold","text-sm","text-900"],[1,"text-xs","text-orange-500","font-medium"],[1,"flex","align-items-center","gap-1","px-2","py-1","border-round","border-1",3,"ngClass"],[1,"text-xs"],[1,"text-xs","font-bold","uppercase"],[1,"text-xs","text-500","flex","justify-content-between","align-items-center","mt-1","flex"],[1,"pi","pi-clock","mr-1"],[1,"w-full","flex","align-items-center","gap-2","text-xs","text-700","p-2","flex",2,"padding","0!important"],[1,"playing-bars","flex","gap-1","align-items-end","h-4px","w-full","justify-content-center","mt-1"],[1,"pi","pi-replay","text-[10px]"],[1,"pi","pi-info-circle","text-orange-400","mt-1","flex-shrink-0"],[1,"line-height-2",2,"word-break","break-word"],[1,"bar"]],template:function(t,o){t&1&&(a(0,"div",1),C(1,Mt,9,3,"div",2),C(2,St,3,0,"div",3)(3,At,34,15,"div",4),l()),t&2&&(r(),w(o.isDialogMode?-1:1),r(),w(o.loading()?2:3))},dependencies:[I,te,Be,Ne,Ve,We,pe,je,ze,Ae,Ze,it,ue,Re,Le,$e,Ee,re],styles:['@charset "UTF-8";[_nghost-%COMP%]{display:block;height:100vh;overflow:hidden}.detail-wrapper[_ngcontent-%COMP%]{height:100%;display:flex;flex-direction:column;background-color:#f8fafc}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar{width:6px;height:6px}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar-track{background:transparent}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:4px}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar-thumb:hover{background:#94a3b8}.list-xxx[_ngcontent-%COMP%]{flex-grow:1}.video-area[_ngcontent-%COMP%]{flex:1 1 auto;min-height:0;width:100%;background-color:#000;position:relative;display:flex;align-items:center;justify-content:center;overflow:hidden}.video-area[_ngcontent-%COMP%]   video[_ngcontent-%COMP%]{outline:none;width:100%;height:100%;object-fit:contain}.info-bar[_ngcontent-%COMP%]{background-color:#fff;box-shadow:0 1px 2px #0000000d;z-index:2;flex:0 0 auto}.timeline-container[_ngcontent-%COMP%]{background-color:#f1f5f9;box-shadow:inset 0 2px 4px #0000000f;white-space:nowrap;flex:0 0 auto;max-height:150px;overflow-y:auto}.timeline-node[_ngcontent-%COMP%]{-webkit-user-select:none;user-select:none;min-width:160px;background-color:#fff;transition:all .2s ease-in-out;border:1px solid transparent}.timeline-node.opacity-70[_ngcontent-%COMP%]{opacity:.7}.timeline-node.opacity-70[_ngcontent-%COMP%]:hover{opacity:1;transform:translateY(-2px);box-shadow:0 4px 6px -1px #0000001a}.timeline-node.border-primary[_ngcontent-%COMP%]{border-color:var(--primary-color)!important;background-color:#eff6ff;box-shadow:0 0 0 1px var(--primary-color)}.timeline-node.border-primary[_ngcontent-%COMP%]   .active-indicator[_ngcontent-%COMP%]{position:absolute;top:-6px;left:50%;transform:translate(-50%);border-left:6px solid transparent;border-right:6px solid transparent;border-bottom:6px solid var(--primary-color);z-index:10}.group[_ngcontent-%COMP%]:hover{background-color:#f8fafc;border-color:#cbd5e1!important}.group.bg-blue-50[_ngcontent-%COMP%]{background-color:#eff6ff!important;border-color:var(--primary-color)!important}.rotate-90[_ngcontent-%COMP%]{transform:rotate(90deg)}.playing-bars[_ngcontent-%COMP%]{height:12px;display:flex;align-items:flex-end;gap:2px}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]{width:4px;background-color:var(--primary-color);animation:_ngcontent-%COMP%_sound .5s ease-in-out infinite alternate;border-radius:2px}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]:nth-child(1){height:6px;animation-duration:.4s}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]:nth-child(2){height:10px;animation-duration:.5s}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]:nth-child(3){height:8px;animation-duration:.6s}@keyframes _ngcontent-%COMP%_sound{0%{height:4px;opacity:.6}to{height:100%;opacity:1}}@media(max-width:991px){[_nghost-%COMP%]{height:auto;overflow:auto}.detail-wrapper[_ngcontent-%COMP%]{overflow-y:visible!important}.flex-grow-1.lg\\:flex-row[_ngcontent-%COMP%]{flex-direction:column!important}.video-area[_ngcontent-%COMP%]{height:40vh!important;min-height:250px;flex:0 0 auto}.lg\\:w-9[_ngcontent-%COMP%]{width:100%!important;flex:none!important}.lg\\:w-3[_ngcontent-%COMP%]{width:100%!important;height:auto!important;min-height:400px;border-left:none!important;border-top:1px solid #e2e8f0}}.p-dialog-title[_ngcontent-%COMP%]{color:#1e293b!important}.align-items-center[_ngcontent-%COMP%]{align-items:center}']})};export{pe as a,We as b,it as c,re as d,ot as e};
