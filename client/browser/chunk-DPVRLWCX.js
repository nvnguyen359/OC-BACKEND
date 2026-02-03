import{b as Et}from"./chunk-W7NCV7QP.js";import{b as It,c as zt}from"./chunk-Y6IHSAR2.js";import{d as ut,f as gt}from"./chunk-FMY5LH6L.js";import{b as Dt,c as kt,d as St}from"./chunk-GUACCTIK.js";import{$ as te,$a as lt,Ab as ye,Bb as F,Cb as d,Cc as dt,Db as oe,De as Pe,Eb as K,Fb as Ce,Fc as ae,Fe as yt,Gb as we,Hb as k,Hc as ue,He as Ct,Ia as be,Ib as z,Ic as ct,Id as de,Ie as wt,Jc as ke,Kc as pt,La as r,Lb as fe,Lc as R,Le as ge,Mb as Te,Nb as he,Ob as le,P as Q,Pb as x,Pc as ve,Q as A,Qb as v,Qe as Tt,Rb as V,Re as Be,S as Z,Sb as J,Sd as Se,Se as Mt,Td as D,U as m,Uc as mt,Ud as Ue,Wd as W,Xc as _t,Ya as S,Yb as q,Yd as Oe,Z as C,Za as H,Zc as je,_ as w,_a as rt,_c as $e,a as X,ab as U,ac as Re,b as Ae,ba as tt,bb as O,cb as g,cd as Xe,dd as Qe,ea as Y,fa as it,fc as xe,fd as ft,gc as st,gd as ht,hc as Me,ia as N,ib as E,ic as se,ja as nt,kc as Ee,kd as Ze,la as ot,lb as B,ma as M,mb as L,md as xt,nb as Ne,nc as Ie,ob as He,pb as l,pd as vt,qb as s,qd as ze,qe as G,rb as c,re as j,sa as at,sb as b,sc as I,se as y,tb as ce,tc as De,te as Fe,ub as pe,vb as me,wb as ie,we as bt,xb as ne,xe as qe,yb as _e,yd as Ye,ye as We,zb as P}from"./chunk-T55JMWX5.js";var Ot=`
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
`;var oi=["icon"],ai=["*"];function ri(t,o){if(t&1&&b(0,"span",4),t&2){let e=d(2);x(e.cx("icon")),l("ngClass",e.icon)("pBind",e.ptm("icon"))}}function li(t,o){if(t&1&&(ie(0),g(1,ri,1,4,"span",3),ne()),t&2){let e=d();r(),l("ngIf",e.icon)}}function si(t,o){}function di(t,o){t&1&&g(0,si,0,0,"ng-template")}function ci(t,o){if(t&1&&(s(0,"span",2),g(1,di,1,0,null,5),c()),t&2){let e=d();x(e.cx("icon")),l("pBind",e.ptm("icon")),r(),l("ngTemplateOutlet",e.iconTemplate||e._iconTemplate)}}var pi={root:({instance:t})=>["p-tag p-component",{"p-tag-info":t.severity==="info","p-tag-success":t.severity==="success","p-tag-warn":t.severity==="warn","p-tag-danger":t.severity==="danger","p-tag-secondary":t.severity==="secondary","p-tag-contrast":t.severity==="contrast","p-tag-rounded":t.rounded}],icon:"p-tag-icon",label:"p-tag-label"},Ft=(()=>{class t extends W{name="tag";style=Ot;classes=pi;static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275prov=Q({token:t,factory:t.\u0275fac})}return t})();var Pt=new Z("TAG_INSTANCE"),Ke=(()=>{class t extends j{$pcTag=m(Pt,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=m(y,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;severity;value;icon;rounded;iconTemplate;templates;_iconTemplate;_componentStyle=m(Ft);onAfterContentInit(){this.templates?.forEach(e=>{switch(e.getType()){case"icon":this._iconTemplate=e.template;break}})}get dataP(){return this.cn({rounded:this.rounded,[this.severity]:this.severity})}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275cmp=S({type:t,selectors:[["p-tag"]],contentQueries:function(n,i,a){if(n&1&&Ce(a,oi,4)(a,Se,4),n&2){let p;k(p=z())&&(i.iconTemplate=p.first),k(p=z())&&(i.templates=p)}},hostVars:3,hostBindings:function(n,i){n&2&&(E("data-p",i.dataP),x(i.cn(i.cx("root"),i.styleClass)))},inputs:{styleClass:"styleClass",severity:"severity",value:"value",icon:"icon",rounded:[2,"rounded","rounded",I]},features:[q([Ft,{provide:Pt,useExisting:t},{provide:G,useExisting:t}]),U([y]),O],ngContentSelectors:ai,decls:5,vars:6,consts:[[4,"ngIf"],[3,"class","pBind",4,"ngIf"],[3,"pBind"],[3,"class","ngClass","pBind",4,"ngIf"],[3,"ngClass","pBind"],[4,"ngTemplateOutlet"]],template:function(n,i){n&1&&(oe(),K(0),g(1,li,2,1,"ng-container",0)(2,ci,2,4,"span",1),s(3,"span",2),v(4),c()),n&2&&(r(),l("ngIf",!i.iconTemplate&&!i._iconTemplate),r(),l("ngIf",i.iconTemplate||i._iconTemplate),r(),x(i.cx("label")),l("pBind",i.ptm("label")),r(),V(i.value))},dependencies:[R,ae,ue,ke,D,y],encapsulation:2,changeDetection:0})}return t})(),Bt=(()=>{class t{static \u0275fac=function(n){return new(n||t)};static \u0275mod=H({type:t});static \u0275inj=A({imports:[Ke,D,D]})}return t})();var Lt=`
    .p-avatar {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: dt('avatar.width');
        height: dt('avatar.height');
        font-size: dt('avatar.font.size');
        background: dt('avatar.background');
        color: dt('avatar.color');
        border-radius: dt('avatar.border.radius');
    }

    .p-avatar-image {
        background: transparent;
    }

    .p-avatar-circle {
        border-radius: 50%;
    }

    .p-avatar-circle img {
        border-radius: 50%;
    }

    .p-avatar-icon {
        font-size: dt('avatar.icon.size');
        width: dt('avatar.icon.size');
        height: dt('avatar.icon.size');
    }

    .p-avatar img {
        width: 100%;
        height: 100%;
    }

    .p-avatar-lg {
        width: dt('avatar.lg.width');
        height: dt('avatar.lg.width');
        font-size: dt('avatar.lg.font.size');
    }

    .p-avatar-lg .p-avatar-icon {
        font-size: dt('avatar.lg.icon.size');
        width: dt('avatar.lg.icon.size');
        height: dt('avatar.lg.icon.size');
    }

    .p-avatar-xl {
        width: dt('avatar.xl.width');
        height: dt('avatar.xl.width');
        font-size: dt('avatar.xl.font.size');
    }

    .p-avatar-xl .p-avatar-icon {
        font-size: dt('avatar.xl.icon.size');
        width: dt('avatar.xl.icon.size');
        height: dt('avatar.xl.icon.size');
    }

    .p-avatar-group {
        display: flex;
        align-items: center;
    }

    .p-avatar-group .p-avatar + .p-avatar {
        margin-inline-start: dt('avatar.group.offset');
    }

    .p-avatar-group .p-avatar {
        border: 2px solid dt('avatar.group.border.color');
    }

    .p-avatar-group .p-avatar-lg + .p-avatar-lg {
        margin-inline-start: dt('avatar.lg.group.offset');
    }

    .p-avatar-group .p-avatar-xl + .p-avatar-xl {
        margin-inline-start: dt('avatar.xl.group.offset');
    }
`;var ui=["*"];function gi(t,o){if(t&1&&(s(0,"span",3),v(1),c()),t&2){let e=d();x(e.cx("label")),l("pBind",e.ptm("label")),E("data-p",e.dataP),r(),V(e.label)}}function _i(t,o){if(t&1&&b(0,"span",5),t&2){let e=d(2);x(e.icon),l("pBind",e.ptm("icon"))("ngClass",e.cx("icon")),E("data-p",e.dataP)}}function fi(t,o){if(t&1&&g(0,_i,1,5,"span",4),t&2){let e=d(),n=fe(5);l("ngIf",e.icon)("ngIfElse",n)}}function hi(t,o){if(t&1){let e=P();s(0,"img",7),F("error",function(i){C(e);let a=d(2);return w(a.imageError(i))}),c()}if(t&2){let e=d(2);l("pBind",e.ptm("image"))("src",e.image,be),E("aria-label",e.ariaLabel)("data-p",e.dataP)}}function xi(t,o){if(t&1&&g(0,hi,1,4,"img",6),t&2){let e=d();l("ngIf",e.image)}}var vi={root:({instance:t})=>["p-avatar p-component",{"p-avatar-image":t.image!=null,"p-avatar-circle":t.shape==="circle","p-avatar-lg":t.size==="large","p-avatar-xl":t.size==="xlarge"}],label:"p-avatar-label",icon:"p-avatar-icon"},Vt=(()=>{class t extends W{name="avatar";style=Lt;classes=vi;static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275prov=Q({token:t,factory:t.\u0275fac})}return t})();var At=new Z("AVATAR_INSTANCE"),Je=(()=>{class t extends j{$pcAvatar=m(At,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=m(y,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}label;icon;image;size="normal";shape="square";styleClass;ariaLabel;ariaLabelledBy;onImageError=new Y;_componentStyle=m(Vt);imageError(e){this.onImageError.emit(e)}get dataP(){return this.cn({[this.shape]:this.shape,[this.size]:this.size})}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275cmp=S({type:t,selectors:[["p-avatar"]],hostVars:5,hostBindings:function(n,i){n&2&&(E("aria-label",i.ariaLabel)("aria-labelledby",i.ariaLabelledBy)("data-p",i.dataP),x(i.cn(i.cx("root"),i.styleClass)))},inputs:{label:"label",icon:"icon",image:"image",size:"size",shape:"shape",styleClass:"styleClass",ariaLabel:"ariaLabel",ariaLabelledBy:"ariaLabelledBy"},outputs:{onImageError:"onImageError"},features:[q([Vt,{provide:At,useExisting:t},{provide:G,useExisting:t}]),U([y]),O],ngContentSelectors:ui,decls:6,vars:2,consts:[["iconTemplate",""],["imageTemplate",""],[3,"pBind","class",4,"ngIf","ngIfElse"],[3,"pBind"],[3,"pBind","class","ngClass",4,"ngIf","ngIfElse"],[3,"pBind","ngClass"],[3,"pBind","src","error",4,"ngIf"],[3,"error","pBind","src"]],template:function(n,i){if(n&1&&(oe(),K(0),g(1,gi,2,5,"span",2)(2,fi,1,2,"ng-template",null,0,se)(4,xi,1,1,"ng-template",null,1,se)),n&2){let a=fe(3);r(),l("ngIf",i.label)("ngIfElse",a)}},dependencies:[R,ae,ue,D,y],encapsulation:2,changeDetection:0})}return t})(),Nt=(()=>{class t{static \u0275fac=function(n){return new(n||t)};static \u0275mod=H({type:t});static \u0275inj=A({imports:[Je,D,D]})}return t})();var Ve=class t{statusMap={packing:"\u0110ang \u0111\xF3ng g\xF3i",packed:"\u0110\xF3ng g\xF3i xong",shipping:"\u0110ang v\u1EADn chuy\u1EC3n",closed:"Ho\xE0n th\xE0nh",cancelled:"\u0110\xE3 h\u1EE7y",pending:"Ch\u1EDD x\u1EED l\xFD",timeout:"H\u1EBFt gi\u1EDD (Timeout)"};transform(o){if(!o)return"Kh\xF4ng x\xE1c \u0111\u1ECBnh";let e=o.toLowerCase();return this.statusMap[e]||o}static \u0275fac=function(e){return new(e||t)};static \u0275pipe=lt({name:"orderStatus",type:t,pure:!0})};var yi=["data-p-icon","window-maximize"],Ht=(()=>{class t extends Pe{pathId;onInit(){this.pathId="url(#"+de()+")"}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275cmp=S({type:t,selectors:[["","data-p-icon","window-maximize"]],features:[O],attrs:yi,decls:5,vars:2,consts:[["fill-rule","evenodd","clip-rule","evenodd","d","M7 14H11.8C12.3835 14 12.9431 13.7682 13.3556 13.3556C13.7682 12.9431 14 12.3835 14 11.8V2.2C14 1.61652 13.7682 1.05694 13.3556 0.644365C12.9431 0.231785 12.3835 0 11.8 0H2.2C1.61652 0 1.05694 0.231785 0.644365 0.644365C0.231785 1.05694 0 1.61652 0 2.2V7C0 7.15913 0.063214 7.31174 0.175736 7.42426C0.288258 7.53679 0.44087 7.6 0.6 7.6C0.75913 7.6 0.911742 7.53679 1.02426 7.42426C1.13679 7.31174 1.2 7.15913 1.2 7V2.2C1.2 1.93478 1.30536 1.68043 1.49289 1.49289C1.68043 1.30536 1.93478 1.2 2.2 1.2H11.8C12.0652 1.2 12.3196 1.30536 12.5071 1.49289C12.6946 1.68043 12.8 1.93478 12.8 2.2V11.8C12.8 12.0652 12.6946 12.3196 12.5071 12.5071C12.3196 12.6946 12.0652 12.8 11.8 12.8H7C6.84087 12.8 6.68826 12.8632 6.57574 12.9757C6.46321 13.0883 6.4 13.2409 6.4 13.4C6.4 13.5591 6.46321 13.7117 6.57574 13.8243C6.68826 13.9368 6.84087 14 7 14ZM9.77805 7.42192C9.89013 7.534 10.0415 7.59788 10.2 7.59995C10.3585 7.59788 10.5099 7.534 10.622 7.42192C10.7341 7.30985 10.798 7.15844 10.8 6.99995V3.94242C10.8066 3.90505 10.8096 3.86689 10.8089 3.82843C10.8079 3.77159 10.7988 3.7157 10.7824 3.6623C10.756 3.55552 10.701 3.45698 10.622 3.37798C10.5099 3.2659 10.3585 3.20202 10.2 3.19995H7.00002C6.84089 3.19995 6.68828 3.26317 6.57576 3.37569C6.46324 3.48821 6.40002 3.64082 6.40002 3.79995C6.40002 3.95908 6.46324 4.11169 6.57576 4.22422C6.68828 4.33674 6.84089 4.39995 7.00002 4.39995H8.80006L6.19997 7.00005C6.10158 7.11005 6.04718 7.25246 6.04718 7.40005C6.04718 7.54763 6.10158 7.69004 6.19997 7.80005C6.30202 7.91645 6.44561 7.98824 6.59997 8.00005C6.75432 7.98824 6.89791 7.91645 6.99997 7.80005L9.60002 5.26841V6.99995C9.6021 7.15844 9.66598 7.30985 9.77805 7.42192ZM1.4 14H3.8C4.17066 13.9979 4.52553 13.8498 4.78763 13.5877C5.04973 13.3256 5.1979 12.9707 5.2 12.6V10.2C5.1979 9.82939 5.04973 9.47452 4.78763 9.21242C4.52553 8.95032 4.17066 8.80215 3.8 8.80005H1.4C1.02934 8.80215 0.674468 8.95032 0.412371 9.21242C0.150274 9.47452 0.00210008 9.82939 0 10.2V12.6C0.00210008 12.9707 0.150274 13.3256 0.412371 13.5877C0.674468 13.8498 1.02934 13.9979 1.4 14ZM1.25858 10.0586C1.29609 10.0211 1.34696 10 1.4 10H3.8C3.85304 10 3.90391 10.0211 3.94142 10.0586C3.97893 10.0961 4 10.147 4 10.2V12.6C4 12.6531 3.97893 12.704 3.94142 12.7415C3.90391 12.779 3.85304 12.8 3.8 12.8H1.4C1.34696 12.8 1.29609 12.779 1.25858 12.7415C1.22107 12.704 1.2 12.6531 1.2 12.6V10.2C1.2 10.147 1.22107 10.0961 1.25858 10.0586Z","fill","currentColor"],[3,"id"],["width","14","height","14","fill","white"]],template:function(n,i){n&1&&(te(),ce(0,"g"),me(1,"path",0),pe(),ce(2,"defs")(3,"clipPath",1),me(4,"rect",2),pe()()),n&2&&(E("clip-path",i.pathId),r(3),ye("id",i.pathId))},encapsulation:2})}return t})();var Ci=["data-p-icon","window-minimize"],Rt=(()=>{class t extends Pe{pathId;onInit(){this.pathId="url(#"+de()+")"}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275cmp=S({type:t,selectors:[["","data-p-icon","window-minimize"]],features:[O],attrs:Ci,decls:5,vars:2,consts:[["fill-rule","evenodd","clip-rule","evenodd","d","M11.8 0H2.2C1.61652 0 1.05694 0.231785 0.644365 0.644365C0.231785 1.05694 0 1.61652 0 2.2V7C0 7.15913 0.063214 7.31174 0.175736 7.42426C0.288258 7.53679 0.44087 7.6 0.6 7.6C0.75913 7.6 0.911742 7.53679 1.02426 7.42426C1.13679 7.31174 1.2 7.15913 1.2 7V2.2C1.2 1.93478 1.30536 1.68043 1.49289 1.49289C1.68043 1.30536 1.93478 1.2 2.2 1.2H11.8C12.0652 1.2 12.3196 1.30536 12.5071 1.49289C12.6946 1.68043 12.8 1.93478 12.8 2.2V11.8C12.8 12.0652 12.6946 12.3196 12.5071 12.5071C12.3196 12.6946 12.0652 12.8 11.8 12.8H7C6.84087 12.8 6.68826 12.8632 6.57574 12.9757C6.46321 13.0883 6.4 13.2409 6.4 13.4C6.4 13.5591 6.46321 13.7117 6.57574 13.8243C6.68826 13.9368 6.84087 14 7 14H11.8C12.3835 14 12.9431 13.7682 13.3556 13.3556C13.7682 12.9431 14 12.3835 14 11.8V2.2C14 1.61652 13.7682 1.05694 13.3556 0.644365C12.9431 0.231785 12.3835 0 11.8 0ZM6.368 7.952C6.44137 7.98326 6.52025 7.99958 6.6 8H9.8C9.95913 8 10.1117 7.93678 10.2243 7.82426C10.3368 7.71174 10.4 7.55913 10.4 7.4C10.4 7.24087 10.3368 7.08826 10.2243 6.97574C10.1117 6.86321 9.95913 6.8 9.8 6.8H8.048L10.624 4.224C10.73 4.11026 10.7877 3.95982 10.7849 3.80438C10.7822 3.64894 10.7192 3.50063 10.6093 3.3907C10.4994 3.28077 10.3511 3.2178 10.1956 3.21506C10.0402 3.21232 9.88974 3.27002 9.776 3.376L7.2 5.952V4.2C7.2 4.04087 7.13679 3.88826 7.02426 3.77574C6.91174 3.66321 6.75913 3.6 6.6 3.6C6.44087 3.6 6.28826 3.66321 6.17574 3.77574C6.06321 3.88826 6 4.04087 6 4.2V7.4C6.00042 7.47975 6.01674 7.55862 6.048 7.632C6.07656 7.70442 6.11971 7.7702 6.17475 7.82524C6.2298 7.88029 6.29558 7.92344 6.368 7.952ZM1.4 8.80005H3.8C4.17066 8.80215 4.52553 8.95032 4.78763 9.21242C5.04973 9.47452 5.1979 9.82939 5.2 10.2V12.6C5.1979 12.9707 5.04973 13.3256 4.78763 13.5877C4.52553 13.8498 4.17066 13.9979 3.8 14H1.4C1.02934 13.9979 0.674468 13.8498 0.412371 13.5877C0.150274 13.3256 0.00210008 12.9707 0 12.6V10.2C0.00210008 9.82939 0.150274 9.47452 0.412371 9.21242C0.674468 8.95032 1.02934 8.80215 1.4 8.80005ZM3.94142 12.7415C3.97893 12.704 4 12.6531 4 12.6V10.2C4 10.147 3.97893 10.0961 3.94142 10.0586C3.90391 10.0211 3.85304 10 3.8 10H1.4C1.34696 10 1.29609 10.0211 1.25858 10.0586C1.22107 10.0961 1.2 10.147 1.2 10.2V12.6C1.2 12.6531 1.22107 12.704 1.25858 12.7415C1.29609 12.779 1.34696 12.8 1.4 12.8H3.8C3.85304 12.8 3.90391 12.779 3.94142 12.7415Z","fill","currentColor"],[3,"id"],["width","14","height","14","fill","white"]],template:function(n,i){n&1&&(te(),ce(0,"g"),me(1,"path",0),pe(),ce(2,"defs")(3,"clipPath",1),me(4,"rect",2),pe()()),n&2&&(E("clip-path",i.pathId),r(3),ye("id",i.pathId))},encapsulation:2})}return t})();var jt=`
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
`;var wi=["*"],Ti={root:({instance:t})=>({justifyContent:t.layout==="horizontal"?t.align==="center"||t.align==null?"center":t.align==="left"?"flex-start":t.align==="right"?"flex-end":null:null,alignItems:t.layout==="vertical"?t.align==="center"||t.align==null?"center":t.align==="top"?"flex-start":t.align==="bottom"?"flex-end":null:null})},Mi={root:({instance:t})=>["p-divider p-component","p-divider-"+t.layout,"p-divider-"+t.type,{"p-divider-left":t.layout==="horizontal"&&(!t.align||t.align==="left")},{"p-divider-center":t.layout==="horizontal"&&t.align==="center"},{"p-divider-right":t.layout==="horizontal"&&t.align==="right"},{"p-divider-top":t.layout==="vertical"&&t.align==="top"},{"p-divider-center":t.layout==="vertical"&&(!t.align||t.align==="center")},{"p-divider-bottom":t.layout==="vertical"&&t.align==="bottom"}],content:"p-divider-content"},$t=(()=>{class t extends W{name="divider";style=jt;classes=Mi;inlineStyles=Ti;static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275prov=Q({token:t,factory:t.\u0275fac})}return t})();var Xt=new Z("DIVIDER_INSTANCE"),Ei=(()=>{class t extends j{$pcDivider=m(Xt,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=m(y,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;layout="horizontal";type="solid";align;_componentStyle=m($t);get dataP(){return this.cn({[this.align]:this.align,[this.layout]:this.layout,[this.type]:this.type})}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275cmp=S({type:t,selectors:[["p-divider"]],hostAttrs:["role","separator"],hostVars:6,hostBindings:function(n,i){n&2&&(E("aria-orientation",i.layout)("data-p",i.dataP),le(i.sx("root")),x(i.cn(i.cx("root"),i.styleClass)))},inputs:{styleClass:"styleClass",layout:"layout",type:"type",align:"align"},features:[q([$t,{provide:Xt,useExisting:t},{provide:G,useExisting:t}]),U([y]),O],ngContentSelectors:wi,decls:2,vars:3,consts:[[3,"pBind"]],template:function(n,i){n&1&&(oe(),s(0,"div",0),K(1),c()),n&2&&(x(i.cx("content")),l("pBind",i.ptm("content")))},dependencies:[R,D,Fe,y],encapsulation:2,changeDetection:0})}return t})(),Qt=(()=>{class t{static \u0275fac=function(n){return new(n||t)};static \u0275mod=H({type:t});static \u0275inj=A({imports:[Ei,Fe,Fe]})}return t})();var Zt=`
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
`;var Ii={root:{position:"relative"}},Di={root:({instance:t})=>["p-skeleton p-component",{"p-skeleton-circle":t.shape==="circle","p-skeleton-animation-none":t.animation==="none"}]},Yt=(()=>{class t extends W{name="skeleton";style=Zt;classes=Di;inlineStyles=Ii;static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275prov=Q({token:t,factory:t.\u0275fac})}return t})();var Ut=new Z("SKELETON_INSTANCE"),et=(()=>{class t extends j{$pcSkeleton=m(Ut,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=m(y,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;shape="rectangle";animation="wave";borderRadius;size;width="100%";height="1rem";_componentStyle=m(Yt);get containerStyle(){let e=this._componentStyle?.inlineStyles.root,n;return this.$unstyled()||(this.size?n=Ae(X({},e),{width:this.size,height:this.size,borderRadius:this.borderRadius}):n=Ae(X({},e),{width:this.width,height:this.height,borderRadius:this.borderRadius})),n}get dataP(){return this.cn({[this.shape]:this.shape})}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275cmp=S({type:t,selectors:[["p-skeleton"]],hostVars:6,hostBindings:function(n,i){n&2&&(E("aria-hidden",!0)("data-p",i.dataP),le(i.containerStyle),x(i.cn(i.cx("root"),i.styleClass)))},inputs:{styleClass:"styleClass",shape:"shape",animation:"animation",borderRadius:"borderRadius",size:"size",width:"width",height:"height"},features:[q([Yt,{provide:Ut,useExisting:t},{provide:G,useExisting:t}]),U([y]),O],decls:0,vars:0,template:function(n,i){},dependencies:[R,D],encapsulation:2,changeDetection:0})}return t})(),qt=(()=>{class t{static \u0275fac=function(n){return new(n||t)};static \u0275mod=H({type:t});static \u0275inj=A({imports:[et,D,D]})}return t})();var zi=["videoPlayer"],Si=(t,o,e)=>({"bg-white shadow-2 border-primary":t,"surface-0 border-transparent text-500 hover:surface-200":o,"opacity-70":e}),Oi=(t,o,e)=>({"bg-green-50 border-green-200 text-green-600":t,"bg-red-50 border-red-200 text-red-600":o,"bg-blue-50 border-blue-200 text-blue-600":e}),Gt=(t,o)=>o.id;function Fi(t,o){if(t&1){let e=P();s(0,"div",2)(1,"p-button",5),F("click",function(){C(e);let i=d();return w(i.goBack())}),c(),s(2,"div")(3,"h2",6),v(4,"Chi ti\u1EBFt \u0111\u01A1n h\xE0ng"),c(),s(5,"span",7),v(6,"M\xE3: "),s(7,"strong",8),v(8),c()()()()}if(t&2){let e,n=d();r(),l("rounded",!0)("text",!0),r(7),V((e=n.selectedOrder())==null?null:e.code)}}function Pi(t,o){t&1&&(s(0,"div",3),b(1,"p-skeleton",9)(2,"p-skeleton",10),c())}function Bi(t,o){if(t&1){let e=P();s(0,"video",33,0),F("play",function(){C(e);let i=d(2);return w(i.onVideoPlay())})("pause",function(){C(e);let i=d(2);return w(i.onVideoPause())})("ended",function(){C(e);let i=d(2);return w(i.onVideoEnded())}),c()}if(t&2){let e=d(2);l("src",e.getFullUrl(e.selectedOrder().path_video),be)}}function Li(t,o){t&1&&(s(0,"div",14),b(1,"i",34),s(2,"span"),v(3,"Kh\xF4ng c\xF3 video"),c()())}function Vi(t,o){t&1&&b(0,"div",45)}function Ai(t,o){t&1&&(s(0,"div",46),b(1,"i",47),c())}function Ni(t,o){if(t&1){let e=P();s(0,"div",37),F("click",function(){let i=C(e).$implicit,a=d(3);return w(a.handleItemClick(i))}),s(1,"div",38),b(2,"i",39),c(),s(3,"div",40)(4,"span",41),v(5),c(),s(6,"div",42)(7,"span",43),v(8),c(),s(9,"span",44),v(10),xe(11,"date"),c()()(),B(12,Vi,1,0,"div",45),c(),B(13,Ai,2,0,"div",46)}if(t&2){let e,n,i,a=o.$implicit,p=o.$index,h=o.$count,f=d(3);l("ngClass",Re(14,Si,((e=f.selectedOrder())==null?null:e.id)===a.id,((e=f.selectedOrder())==null?null:e.id)!==a.id,((e=f.selectedOrder())==null?null:e.id)!==a.id&&!a.parent_id)),r(),l("ngClass",a.parent_id?"bg-orange-100 text-orange-600":"bg-blue-50 text-blue-600"),r(),l("ngClass",a.parent_id?"pi-replay":"pi-box"),r(2),he("text-900",((n=f.selectedOrder())==null?null:n.id)===a.id),r(),J(" ",a.code," "),r(2),l("ngClass",a.parent_id?"text-orange-600":"text-blue-600"),r(),J(" ",a.parent_id?"Ho\xE0n/\u0110\xF3ng l\u1EA1i":"\u0110\u01A1n g\u1ED1c"," "),r(2),J("\u2022 ",Me(11,11,a.created_at,"HH:mm")),r(2),L(((i=f.selectedOrder())==null?null:i.id)===a.id?12:-1),r(),L(p!==h-1?13:-1)}}function Hi(t,o){if(t&1&&(s(0,"div",25)(1,"div",35)(2,"span",36),v(3,"Quy tr\xECnh:"),c(),Ne(4,Ni,14,18,null,null,Gt),c()()),t&2){let e=d(2);r(4),He(e.orderList().slice().reverse())}}function Ri(t,o){t&1&&(s(0,"span",57),b(1,"i",65),v(2," \u0110\xF3ng l\u1EA1i "),c())}function ji(t,o){if(t&1&&(s(0,"div",63),b(1,"i",66),s(2,"span",67),v(3),c()()),t&2){let e=d().$implicit;r(3),V(e.note)}}function $i(t,o){t&1&&(s(0,"div",64),b(1,"div",68)(2,"div",68)(3,"div",68),c())}function Xi(t,o){if(t&1){let e=P();s(0,"div",48),F("click",function(){let i=C(e).$implicit,a=d(2);return w(a.handleItemClick(i))}),s(1,"div",49)(2,"div",50),b(3,"div",51)(4,"i",52),c(),s(5,"div",53)(6,"div",54)(7,"div",55)(8,"span",56),v(9),c(),B(10,Ri,3,0,"span",57),c(),s(11,"div",58),b(12,"i",59),s(13,"span",60),v(14),c()()(),s(15,"div",61)(16,"span"),b(17,"i",62),v(18),xe(19,"date"),c(),s(20,"span"),v(21),c()()()(),B(22,ji,4,1,"div",63),B(23,$i,4,0,"div",64),c()}if(t&2){let e,n,i,a,p,h,f,_,re,$,u=o.$implicit,T=d(2);he("bg-blue-50",((e=T.selectedOrder())==null?null:e.id)===u.id)("border-blue-500",((n=T.selectedOrder())==null?null:n.id)===u.id)("surface-card",((i=T.selectedOrder())==null?null:i.id)!==u.id)("border-transparent",((a=T.selectedOrder())==null?null:a.id)!==u.id)("shadow-1",((p=T.selectedOrder())==null?null:p.id)!==u.id),r(2),Te("background-image","url("+T.getFullUrl(u.path_avatar)+")"),r(2),he("pi-pause",((h=T.selectedOrder())==null?null:h.id)===u.id&&T.isPlaying())("pi-play",((f=T.selectedOrder())==null?null:f.id)!==u.id||!T.isPlaying())("text-2xl",((_=T.selectedOrder())==null?null:_.id)===u.id),r(4),he("text-primary",((re=T.selectedOrder())==null?null:re.id)===u.id),r(),J(" ",u.code," "),r(),L(u.parent_id?10:-1),r(),l("ngClass",Re(33,Oi,u.status==="packed",u.status==="cancelled",u.status==="processing")),r(),x(T.getStatusIcon(u.status)),r(2),V(u.status),r(4),V(Me(19,30,u.created_at,"HH:mm dd/MM")),r(3),J("#",u.id),r(),L(u.note?22:-1),r(),L((($=T.selectedOrder())==null?null:$.id)===u.id&&T.isPlaying()?23:-1)}}function Qi(t,o){if(t&1){let e=P();s(0,"div",4)(1,"div",11)(2,"div",12),B(3,Bi,2,1,"video",13)(4,Li,4,0,"div",14),c(),s(5,"div",15)(6,"div",16),b(7,"p-avatar",17),s(8,"div")(9,"div",18),v(10),c(),s(11,"div",19),v(12),xe(13,"date"),c()()(),s(14,"div",20)(15,"div",21)(16,"button",22),F("click",function(i){C(e);let a=d();return w(a.downloadVideo(a.selectedOrder(),i))}),c(),b(17,"p-tag",23),xe(18,"orderStatus"),c(),s(19,"div",24),v(20),c()()(),B(21,Hi,6,0,"div",25),c(),s(22,"div",26)(23,"div",27)(24,"div",21)(25,"span"),v(26),c(),s(27,"i",28),F("click",function(){C(e);let i=d();return w(i.downloadAllVideos())}),c()(),s(28,"span",29),v(29),c()(),s(30,"div",30)(31,"div",31),Ne(32,Xi,24,37,"div",32,Gt),c()()()()}if(t&2){let e,n,i,a,p,h,f,_=d();r(3),L((e=_.selectedOrder())!=null&&e.path_video?3:4),r(4),l("image",_.getFullUrl((n=_.selectedOrder())==null?null:n.path_avatar)),r(3),J("NV: ",((i=_.selectedOrder())==null?null:i.packer_name)||"#"+((i=_.selectedOrder())==null?null:i.user_id)),r(2),V(Me(13,10,(a=_.selectedOrder())==null?null:a.closed_at,"HH:mm dd/MM/yyyy")),r(5),l("value",st(18,13,(p=_.selectedOrder())==null?null:p.status))("severity",_.getSeverity((h=_.selectedOrder())==null?null:h.status)),r(3),J("Cam: ",(f=_.selectedOrder())==null?null:f.camera_id),r(),L(_.orderList().length>0?21:-1),r(5),J("L\u1ECBch s\u1EED (",_.orderList().length,")"),r(3),V(_.durationString()),r(3),He(_.orderList())}}var Wt=class t{inputCode=null;isDialogMode=!1;videoPlayer;route=m(ut);router=m(gt);orderService=m(zt);location=m(dt);http=m(mt);settingsService=m(St);loading=N(!0);isDownloading=N(!1);orderList=N([]);selectedOrder=N(null);isPlaying=N(!1);durationString=N("");aspectRatio=N("16 / 9");constructor(){nt(()=>{let o=this.selectedOrder();o&&this.calculateDuration(o.start_at,o.closed_at)})}ngOnInit(){if(this.settingsService.getSettings().subscribe({next:o=>{let e=Number(o.camera_width),n=Number(o.camera_height);!isNaN(e)&&!isNaN(n)&&e>0&&n>0&&this.aspectRatio.set(`${e} / ${n}`)},error:o=>console.warn("Kh\xF4ng th\u1EC3 t\u1EA3i settings, d\xF9ng t\u1EC9 l\u1EC7 m\u1EB7c \u0111\u1ECBnh.",o)}),this.inputCode)this.fetchOrders(this.inputCode);else{let o=this.route.snapshot.paramMap.get("code");o&&this.fetchOrders(o)}}ngOnChanges(o){o.inputCode&&!o.inputCode.firstChange&&this.inputCode&&this.fetchOrders(this.inputCode)}fetchOrders(o){this.loading.set(!0),this.orderService.getOrders({code:o,page:1,page_size:100}).subscribe({next:e=>{let n=e.data||{},i=n.items||[];!i.length&&Array.isArray(n)?i=n:!i.length&&n.data&&Array.isArray(n.data)&&(i=n.data);let a=[];i.forEach(f=>{a.push(f),f.history_logs&&Array.isArray(f.history_logs)&&a.push(...f.history_logs)}),a.sort((f,_)=>new Date(_.created_at).getTime()-new Date(f.created_at).getTime()),this.orderList.set(a);let p=this.route.snapshot.queryParamMap.get("playId"),h=null;if(p&&a.length>0){let f=Number(p);h=a.find(_=>_.id===f)}!h&&a.length>0&&(h=a[0]),h&&this.selectOrder(h,!0),this.loading.set(!1)},error:e=>{console.error("Order Detail API Error:",e),this.orderList.set([]),this.loading.set(!1)}})}handleItemClick(o){this.selectedOrder()?.id===o.id?this.toggleVideoState():this.selectOrder(o,!0)}selectOrder(o,e=!1){this.selectedOrder.set(o),this.isPlaying.set(!1),e&&this.videoPlayer&&setTimeout(()=>{let n=this.videoPlayer.nativeElement;n.load(),n.play().catch(()=>{})},100)}toggleVideoState(){if(!this.videoPlayer)return;let o=this.videoPlayer.nativeElement;o.paused?o.play():o.pause()}onVideoPlay(){this.isPlaying.set(!0)}onVideoPause(){this.isPlaying.set(!1)}onVideoEnded(){this.isPlaying.set(!1)}downloadVideo(o,e){if(e&&e.stopPropagation(),!o?.path_video)return;this.isDownloading.set(!0);let n=this.getFullUrl(o.path_video),i=`${o.code}_${o.id}.mp4`;this.http.get(n,{responseType:"blob"}).subscribe({next:a=>{let p=URL.createObjectURL(a),h=document.createElement("a");h.href=p,h.download=i,document.body.appendChild(h),h.click(),document.body.removeChild(h),URL.revokeObjectURL(p),this.isDownloading.set(!1)},error:a=>{console.error("L\u1ED7i khi t\u1EA3i video:",a),this.isDownloading.set(!1),window.open(n,"_blank")}})}downloadAllVideos(){let o=this.orderList();if(!o||o.length===0||!confirm(`T\u1EA3i xu\u1ED1ng ${o.length} video?`))return;let e=0;o.forEach(n=>{n.path_video&&(setTimeout(()=>{this.downloadVideo(n)},e),e+=1500)})}getFullUrl(o){if(!o)return"";if(o.startsWith("http"))return o;let e=Oe.apiUrl.endsWith("/")?Oe.apiUrl.slice(0,-1):Oe.apiUrl,n=o.startsWith("/")?o:`/${o}`;return`${e}${n}`}calculateDuration(o,e){if(!o||!e){this.durationString.set("--:--");return}let n=Math.floor((new Date(e).getTime()-new Date(o).getTime())/1e3),i=Math.floor(n/60),a=n%60;this.durationString.set(`${i}p ${a}s`)}getStatusIcon(o){switch(o?.toLowerCase()){case"packed":return"pi pi-check-circle";case"cancelled":return"pi pi-times-circle";case"processing":return"pi pi-spin pi-spinner";default:return"pi pi-info-circle"}}getSeverity(o){switch(o?.toLowerCase()){case"packed":return"success";case"cancelled":return"danger";case"processing":return"info";default:return"warn"}}goBack(){this.isDialogMode||(window.history.length>1?this.location.back():this.router.navigate(["/"]))}static \u0275fac=function(e){return new(e||t)};static \u0275cmp=S({type:t,selectors:[["app-order-detail"]],viewQuery:function(e,n){if(e&1&&we(zi,5),e&2){let i;k(i=z())&&(n.videoPlayer=i.first)}},inputs:{inputCode:"inputCode",isDialogMode:"isDialogMode"},features:[ot],decls:4,vars:2,consts:[["videoPlayer",""],[1,"detail-wrapper","flex","flex-column","h-full","overflow-hidden","bg-white"],[1,"flex-none","flex","align-items-center","gap-3","p-3","border-bottom-1","surface-border"],[1,"flex-grow-1","p-3","flex","flex-column","gap-3"],[1,"flex","flex-column","lg:flex-row","min-h-0"],["icon","pi pi-arrow-left",3,"click","rounded","text"],[1,"m-0","font-bold","text-lg"],[1,"text-500","text-sm"],[1,"text-primary"],["height","300px","styleClass","w-full border-round"],["height","100px","styleClass","w-full border-round"],[1,"lg:w-9","flex","flex-column","bg-black-alpha-90","relative","overflow-hidden"],[1,"video-area","flex","align-items-center","justify-content-center","relative"],["controls","","autoplay","",1,"w-full","h-full",2,"max-height","100%","object-fit","contain",3,"src"],[1,"text-white-alpha-60","flex","flex-column","align-items-center"],[1,"info-bar","flex-none","p-3","surface-0","border-top-1","surface-border","flex","justify-content-between","align-items-center"],[1,"flex","align-items-center","gap-3"],["shape","circle","size","large","styleClass","border-1 surface-border",3,"image"],[1,"font-bold","text-900","line-height-2"],[1,"text-sm","text-500"],[1,"flex","flex-column","align-items-end","gap-1"],[1,"flex","align-items-center","gap-2"],["pButton","","icon","pi pi-download","pTooltip","T\u1EA3i video n\xE0y","tooltipPosition","left",1,"p-button-rounded","p-button-text","p-button-secondary","w-2rem","h-2rem",3,"click"],[3,"value","severity"],[1,"text-xs","text-500"],[1,"timeline-container","w-full","px-3","pt-4","pb-3","surface-50","border-top-1","surface-border","overflow-x-auto","custom-scrollbar"],[1,"flex-none","h-20rem","lg:h-auto","lg:w-3","surface-50","border-left-1","surface-border","flex","flex-column"],[1,"p-3","font-bold","text-700","border-bottom-1","surface-border","flex","justify-content-between","align-items-center"],["pTooltip","T\u1EA3i t\u1EA5t c\u1EA3 video",1,"pi","pi-download","text-primary","cursor-pointer","hover:text-primary-700","transition-colors",3,"click"],[1,"text-sm","font-normal","text-primary"],[1,"flex-grow-1","overflow-y-auto","custom-scrollbar"],[1,"flex","flex-column","p-2","gap-2","list-xxx"],[1,"p-2","border-round","border-1","transition-colors","transition-duration-150","flex","flex-column","gap-2","cursor-pointer","group",3,"bg-blue-50","border-blue-500","surface-card","border-transparent","shadow-1"],["controls","","autoplay","",1,"w-full","h-full",2,"max-height","100%","object-fit","contain",3,"play","pause","ended","src"],[1,"pi","pi-video-slash","text-5xl","mb-2"],[1,"flex","align-items-center","gap-2",2,"min-width","max-content"],[1,"text-xs","font-bold","text-500","uppercase","mr-2","flex-shrink-0"],[1,"timeline-node","relative","flex","align-items-center","gap-2","p-2","border-round-xl","cursor-pointer","transition-all","transition-duration-200","border-1",3,"click","ngClass"],[1,"w-2rem","h-2rem","border-circle","flex","align-items-center","justify-content-center","flex-shrink-0",3,"ngClass"],[1,"pi","text-sm",3,"ngClass"],[1,"flex","flex-column","justify-content-center"],[1,"text-xs","font-bold","white-space-nowrap"],[1,"flex","align-items-center","gap-1","white-space-nowrap"],[1,"text-[10px]","font-medium",3,"ngClass"],[1,"text-[10px]","text-400"],[1,"active-indicator"],[1,"flex","align-items-center","justify-content-center","px-1"],[1,"pi","pi-arrow-right","text-300","text-xs"],[1,"p-2","border-round","border-1","transition-colors","transition-duration-150","flex","flex-column","gap-2","cursor-pointer","group",3,"click"],[1,"flex","gap-3","align-items-start","list-item"],[1,"relative","w-4rem","h-3rem","border-round","overflow-hidden","flex-shrink-0","flex","align-items-center","justify-content-center","bg-cover","bg-center","shadow-1","mt-1"],[1,"absolute","top-0","left-0","w-full","h-full","bg-black-alpha-40"],[1,"pi","text-white","text-xl","relative","z-1","transition-all"],[1,"flex","flex-column","flex-grow-1","min-w-0"],[1,"flex","justify-content-between","align-items-start","mb-1"],[1,"flex","flex-column"],[1,"font-bold","text-sm","text-900"],[1,"text-xs","text-orange-500","font-medium"],[1,"flex","align-items-center","gap-1","px-2","py-1","border-round","border-1",3,"ngClass"],[1,"text-xs"],[1,"text-xs","font-bold","uppercase"],[1,"text-xs","text-500","flex","justify-content-between","align-items-center","mt-1","flex"],[1,"pi","pi-clock","mr-1"],[1,"w-full","flex","align-items-center","gap-2","text-xs","text-700","p-2","flex",2,"padding","0!important"],[1,"playing-bars","flex","gap-1","align-items-end","h-4px","w-full","justify-content-center","mt-1"],[1,"pi","pi-replay","text-[10px]"],[1,"pi","pi-info-circle","text-orange-400","mt-1","flex-shrink-0"],[1,"line-height-2",2,"word-break","break-word"],[1,"bar"]],template:function(e,n){e&1&&(s(0,"div",1),B(1,Fi,9,3,"div",2),B(2,Pi,3,0,"div",3)(3,Qi,34,15,"div",4),c()),e&2&&(r(),L(n.isDialogMode?-1:1),r(),L(n.loading()?2:3))},dependencies:[R,ae,Mt,Tt,Be,Bt,Ke,Et,Nt,Je,Qt,qt,et,It,kt,Dt,pt,Ve],styles:['@charset "UTF-8";[_nghost-%COMP%]{display:block;height:100vh;overflow:hidden}.detail-wrapper[_ngcontent-%COMP%]{height:100%;display:flex;flex-direction:column;background-color:#f8fafc}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar{width:6px;height:6px}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar-track{background:transparent}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:4px}.custom-scrollbar[_ngcontent-%COMP%]::-webkit-scrollbar-thumb:hover{background:#94a3b8}.list-xxx[_ngcontent-%COMP%]{flex-grow:1}.video-area[_ngcontent-%COMP%]{flex:1 1 auto;min-height:0;width:100%;background-color:#000;position:relative;display:flex;align-items:center;justify-content:center;overflow:hidden}.video-area[_ngcontent-%COMP%]   video[_ngcontent-%COMP%]{outline:none;width:100%;height:100%;object-fit:contain}.info-bar[_ngcontent-%COMP%]{background-color:#fff;box-shadow:0 1px 2px #0000000d;z-index:2;flex:0 0 auto}.timeline-container[_ngcontent-%COMP%]{background-color:#f1f5f9;box-shadow:inset 0 2px 4px #0000000f;white-space:nowrap;flex:0 0 auto;max-height:150px;overflow-y:auto}.timeline-node[_ngcontent-%COMP%]{-webkit-user-select:none;user-select:none;min-width:160px;background-color:#fff;transition:all .2s ease-in-out;border:1px solid transparent}.timeline-node.opacity-70[_ngcontent-%COMP%]{opacity:.7}.timeline-node.opacity-70[_ngcontent-%COMP%]:hover{opacity:1;transform:translateY(-2px);box-shadow:0 4px 6px -1px #0000001a}.timeline-node.border-primary[_ngcontent-%COMP%]{border-color:var(--primary-color)!important;background-color:#eff6ff;box-shadow:0 0 0 1px var(--primary-color)}.timeline-node.border-primary[_ngcontent-%COMP%]   .active-indicator[_ngcontent-%COMP%]{position:absolute;top:-6px;left:50%;transform:translate(-50%);border-left:6px solid transparent;border-right:6px solid transparent;border-bottom:6px solid var(--primary-color);z-index:10}.group[_ngcontent-%COMP%]:hover{background-color:#f8fafc;border-color:#cbd5e1!important}.group.bg-blue-50[_ngcontent-%COMP%]{background-color:#eff6ff!important;border-color:var(--primary-color)!important}.playing-bars[_ngcontent-%COMP%]{height:12px;display:flex;align-items:flex-end;gap:2px}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]{width:4px;background-color:var(--primary-color);animation:_ngcontent-%COMP%_sound .5s ease-in-out infinite alternate;border-radius:2px}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]:nth-child(1){height:6px;animation-duration:.4s}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]:nth-child(2){height:10px;animation-duration:.5s}.playing-bars[_ngcontent-%COMP%]   .bar[_ngcontent-%COMP%]:nth-child(3){height:8px;animation-duration:.6s}@keyframes _ngcontent-%COMP%_sound{0%{height:4px;opacity:.6}to{height:100%;opacity:1}}@media(max-width:991px){[_nghost-%COMP%]{height:100vh!important;overflow:hidden!important}.detail-wrapper[_ngcontent-%COMP%]{overflow-y:hidden!important}.flex-grow-1.lg\\:flex-row[_ngcontent-%COMP%]{flex-direction:column!important;height:100%;overflow:hidden}.video-area[_ngcontent-%COMP%]{height:35vh!important;min-height:200px;flex:0 0 auto!important}.lg\\:w-9[_ngcontent-%COMP%]{width:100%!important;flex:0 0 auto!important;height:auto!important;display:flex;flex-direction:column}.lg\\:w-3[_ngcontent-%COMP%]{width:100%!important;flex:1 1 auto!important;min-height:0!important;height:auto!important;border-left:none!important;border-top:1px solid #e2e8f0;display:flex!important;flex-direction:column!important;overflow:hidden!important}}.p-dialog-title[_ngcontent-%COMP%]{color:#1e293b!important}.align-items-center[_ngcontent-%COMP%]{align-items:center}']})};var Kt=(()=>{class t extends j{pFocusTrapDisabled=!1;platformId=m(at);document=m(tt);firstHiddenFocusableElement;lastHiddenFocusableElement;onInit(){ve(this.platformId)&&!this.pFocusTrapDisabled&&!this.firstHiddenFocusableElement&&!this.lastHiddenFocusableElement&&this.createHiddenFocusableElements()}onChanges(e){e.pFocusTrapDisabled&&ve(this.platformId)&&(e.pFocusTrapDisabled.currentValue?this.removeHiddenFocusableElements():this.createHiddenFocusableElements())}removeHiddenFocusableElements(){this.firstHiddenFocusableElement&&this.firstHiddenFocusableElement.parentNode&&this.firstHiddenFocusableElement.parentNode.removeChild(this.firstHiddenFocusableElement),this.lastHiddenFocusableElement&&this.lastHiddenFocusableElement.parentNode&&this.lastHiddenFocusableElement.parentNode.removeChild(this.lastHiddenFocusableElement)}getComputedSelector(e){return`:not(.p-hidden-focusable):not([data-p-hidden-focusable="true"])${e??""}`}createHiddenFocusableElements(){let n=i=>ht("span",{class:"p-hidden-accessible p-hidden-focusable",tabindex:"0",role:"presentation","aria-hidden":!0,"data-p-hidden-accessible":!0,"data-p-hidden-focusable":!0,onFocus:i?.bind(this)});this.firstHiddenFocusableElement=n(this.onFirstHiddenElementFocus),this.lastHiddenFocusableElement=n(this.onLastHiddenElementFocus),this.firstHiddenFocusableElement.setAttribute("data-pc-section","firstfocusableelement"),this.lastHiddenFocusableElement.setAttribute("data-pc-section","lastfocusableelement"),this.el.nativeElement.prepend(this.firstHiddenFocusableElement),this.el.nativeElement.append(this.lastHiddenFocusableElement)}onFirstHiddenElementFocus(e){let{currentTarget:n,relatedTarget:i}=e,a=i===this.lastHiddenFocusableElement||!this.el.nativeElement?.contains(i)?xt(n.parentElement,":not(.p-hidden-focusable)"):this.lastHiddenFocusableElement;Ze(a)}onLastHiddenElementFocus(e){let{currentTarget:n,relatedTarget:i}=e,a=i===this.firstHiddenFocusableElement||!this.el.nativeElement?.contains(i)?vt(n.parentElement,":not(.p-hidden-focusable)"):this.firstHiddenFocusableElement;Ze(a)}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275dir=rt({type:t,selectors:[["","pFocusTrap",""]],inputs:{pFocusTrapDisabled:[2,"pFocusTrapDisabled","pFocusTrapDisabled",I]},features:[O]})}return t})(),Pa=(()=>{class t{static \u0275fac=function(n){return new(n||t)};static \u0275mod=H({type:t});static \u0275inj=A({})}return t})();var Jt=`
    .p-dialog {
        max-height: 90%;
        transform: scale(1);
        border-radius: dt('dialog.border.radius');
        box-shadow: dt('dialog.shadow');
        background: dt('dialog.background');
        border: 1px solid dt('dialog.border.color');
        color: dt('dialog.color');
        will-change: transform;
    }

    .p-dialog-content {
        overflow-y: auto;
        padding: dt('dialog.content.padding');
    }

    .p-dialog-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
        padding: dt('dialog.header.padding');
    }

    .p-dialog-title {
        font-weight: dt('dialog.title.font.weight');
        font-size: dt('dialog.title.font.size');
    }

    .p-dialog-footer {
        flex-shrink: 0;
        padding: dt('dialog.footer.padding');
        display: flex;
        justify-content: flex-end;
        gap: dt('dialog.footer.gap');
    }

    .p-dialog-header-actions {
        display: flex;
        align-items: center;
        gap: dt('dialog.header.gap');
    }

    .p-dialog-top .p-dialog,
    .p-dialog-bottom .p-dialog,
    .p-dialog-left .p-dialog,
    .p-dialog-right .p-dialog,
    .p-dialog-topleft .p-dialog,
    .p-dialog-topright .p-dialog,
    .p-dialog-bottomleft .p-dialog,
    .p-dialog-bottomright .p-dialog {
        margin: 1rem;
    }

    .p-dialog-maximized {
        width: 100vw !important;
        height: 100vh !important;
        top: 0px !important;
        left: 0px !important;
        max-height: 100%;
        height: 100%;
        border-radius: 0;
    }

    .p-dialog-maximized .p-dialog-content {
        flex-grow: 1;
    }

    .p-dialog .p-resizable-handle {
        position: absolute;
        font-size: 0.1px;
        display: block;
        cursor: se-resize;
        width: 12px;
        height: 12px;
        right: 1px;
        bottom: 1px;
    }

    .p-dialog-enter-active {
        animation: p-animate-dialog-enter 300ms cubic-bezier(.19,1,.22,1);
    }

    .p-dialog-leave-active {
        animation: p-animate-dialog-leave 300ms cubic-bezier(.19,1,.22,1);
    }

    @keyframes p-animate-dialog-enter {
        from {
            opacity: 0;
            transform: scale(0.93);
        }
    }

    @keyframes p-animate-dialog-leave {
        to {
            opacity: 0;
            transform: scale(0.93);
        }
    }
`;var Zi=["header"],ei=["content"],ti=["footer"],Yi=["closeicon"],Ui=["maximizeicon"],qi=["minimizeicon"],Wi=["headless"],Gi=["titlebar"],Ki=["*",[["p-footer"]]],Ji=["*","p-footer"];function en(t,o){t&1&&_e(0)}function tn(t,o){if(t&1&&(ie(0),g(1,en,1,0,"ng-container",11),ne()),t&2){let e=d(3);r(),l("ngTemplateOutlet",e._headlessTemplate||e.headlessTemplate||e.headlessT)}}function nn(t,o){if(t&1){let e=P();s(0,"div",16),F("mousedown",function(i){C(e);let a=d(4);return w(a.initResize(i))}),c()}if(t&2){let e=d(4);x(e.cx("resizeHandle")),Te("z-index",90),l("pBind",e.ptm("resizeHandle"))}}function on(t,o){if(t&1&&(s(0,"span",20),v(1),c()),t&2){let e=d(5);x(e.cx("title")),l("id",e.ariaLabelledBy)("pBind",e.ptm("title")),r(),V(e.header)}}function an(t,o){t&1&&_e(0)}function rn(t,o){if(t&1&&b(0,"span",24),t&2){let e=d(7);l("ngClass",e.maximized?e.minimizeIcon:e.maximizeIcon)}}function ln(t,o){t&1&&(te(),b(0,"svg",27))}function sn(t,o){t&1&&(te(),b(0,"svg",28))}function dn(t,o){if(t&1&&(ie(0),g(1,ln,1,0,"svg",25)(2,sn,1,0,"svg",26),ne()),t&2){let e=d(7);r(),l("ngIf",!e.maximized&&!e._maximizeiconTemplate&&!e.maximizeIconTemplate&&!e.maximizeIconT),r(),l("ngIf",e.maximized&&!e._minimizeiconTemplate&&!e.minimizeIconTemplate&&!e.minimizeIconT)}}function cn(t,o){}function pn(t,o){t&1&&g(0,cn,0,0,"ng-template")}function mn(t,o){if(t&1&&(ie(0),g(1,pn,1,0,null,11),ne()),t&2){let e=d(7);r(),l("ngTemplateOutlet",e._maximizeiconTemplate||e.maximizeIconTemplate||e.maximizeIconT)}}function un(t,o){}function gn(t,o){t&1&&g(0,un,0,0,"ng-template")}function _n(t,o){if(t&1&&(ie(0),g(1,gn,1,0,null,11),ne()),t&2){let e=d(7);r(),l("ngTemplateOutlet",e._minimizeiconTemplate||e.minimizeIconTemplate||e.minimizeIconT)}}function fn(t,o){if(t&1&&g(0,rn,1,1,"span",22)(1,dn,3,2,"ng-container",23)(2,mn,2,1,"ng-container",23)(3,_n,2,1,"ng-container",23),t&2){let e=d(6);l("ngIf",e.maximizeIcon&&!e._maximizeiconTemplate&&!e._minimizeiconTemplate),r(),l("ngIf",!e.maximizeIcon&&!(e.maximizeButtonProps!=null&&e.maximizeButtonProps.icon)),r(),l("ngIf",!e.maximized),r(),l("ngIf",e.maximized)}}function hn(t,o){if(t&1){let e=P();s(0,"p-button",21),F("onClick",function(){C(e);let i=d(5);return w(i.maximize())})("keydown.enter",function(){C(e);let i=d(5);return w(i.maximize())}),g(1,fn,4,4,"ng-template",null,4,se),c()}if(t&2){let e=d(5);l("pt",e.ptm("pcMaximizeButton"))("styleClass",e.cx("pcMaximizeButton"))("ariaLabel",e.maximized?e.minimizeLabel:e.maximizeLabel)("tabindex",e.maximizable?"0":"-1")("buttonProps",e.maximizeButtonProps)("unstyled",e.unstyled()),E("data-pc-group-section","headericon")}}function xn(t,o){if(t&1&&b(0,"span"),t&2){let e=d(8);x(e.closeIcon)}}function vn(t,o){t&1&&(te(),b(0,"svg",31))}function bn(t,o){if(t&1&&(ie(0),g(1,xn,1,2,"span",29)(2,vn,1,0,"svg",30),ne()),t&2){let e=d(7);r(),l("ngIf",e.closeIcon),r(),l("ngIf",!e.closeIcon)}}function yn(t,o){}function Cn(t,o){t&1&&g(0,yn,0,0,"ng-template")}function wn(t,o){if(t&1&&(s(0,"span"),g(1,Cn,1,0,null,11),c()),t&2){let e=d(7);r(),l("ngTemplateOutlet",e._closeiconTemplate||e.closeIconTemplate||e.closeIconT)}}function Tn(t,o){if(t&1&&g(0,bn,3,2,"ng-container",23)(1,wn,2,1,"span",23),t&2){let e=d(6);l("ngIf",!e._closeiconTemplate&&!e.closeIconTemplate&&!e.closeIconT&&!(e.closeButtonProps!=null&&e.closeButtonProps.icon)),r(),l("ngIf",e._closeiconTemplate||e.closeIconTemplate||e.closeIconT)}}function Mn(t,o){if(t&1){let e=P();s(0,"p-button",21),F("onClick",function(i){C(e);let a=d(5);return w(a.close(i))})("keydown.enter",function(i){C(e);let a=d(5);return w(a.close(i))}),g(1,Tn,2,2,"ng-template",null,4,se),c()}if(t&2){let e=d(5);l("pt",e.ptm("pcCloseButton"))("styleClass",e.cx("pcCloseButton"))("ariaLabel",e.closeAriaLabel)("tabindex",e.closeTabindex)("buttonProps",e.closeButtonProps)("unstyled",e.unstyled()),E("data-pc-group-section","headericon")}}function En(t,o){if(t&1){let e=P();s(0,"div",16,3),F("mousedown",function(i){C(e);let a=d(4);return w(a.initDrag(i))}),g(2,on,2,5,"span",17)(3,an,1,0,"ng-container",11),s(4,"div",18),g(5,hn,3,7,"p-button",19)(6,Mn,3,7,"p-button",19),c()()}if(t&2){let e=d(4);x(e.cx("header")),l("pBind",e.ptm("header")),r(2),l("ngIf",!e._headerTemplate&&!e.headerTemplate&&!e.headerT),r(),l("ngTemplateOutlet",e._headerTemplate||e.headerTemplate||e.headerT),r(),x(e.cx("headerActions")),l("pBind",e.ptm("headerActions")),r(),l("ngIf",e.maximizable),r(),l("ngIf",e.closable)}}function In(t,o){t&1&&_e(0)}function Dn(t,o){t&1&&_e(0)}function kn(t,o){if(t&1&&(s(0,"div",18,5),K(2,1),g(3,Dn,1,0,"ng-container",11),c()),t&2){let e=d(4);x(e.cx("footer")),l("pBind",e.ptm("footer")),r(3),l("ngTemplateOutlet",e._footerTemplate||e.footerTemplate||e.footerT)}}function zn(t,o){if(t&1&&(g(0,nn,1,5,"div",12)(1,En,7,10,"div",13),s(2,"div",14,2),K(4),g(5,In,1,0,"ng-container",11),c(),g(6,kn,4,4,"div",15)),t&2){let e=d(3);l("ngIf",e.resizable),r(),l("ngIf",e.showHeader),r(),x(e.cn(e.cx("content"),e.contentStyleClass)),l("ngStyle",e.contentStyle)("pBind",e.ptm("content")),r(3),l("ngTemplateOutlet",e._contentTemplate||e.contentTemplate||e.contentT),r(),l("ngIf",e._footerTemplate||e.footerTemplate||e.footerT)}}function Sn(t,o){if(t&1){let e=P();s(0,"div",9,0),F("pMotionOnBeforeEnter",function(i){C(e);let a=d(2);return w(a.onBeforeEnter(i))})("pMotionOnAfterEnter",function(i){C(e);let a=d(2);return w(a.onAfterEnter(i))})("pMotionOnBeforeLeave",function(i){C(e);let a=d(2);return w(a.onBeforeLeave(i))})("pMotionOnAfterLeave",function(i){C(e);let a=d(2);return w(a.onAfterLeave(i))}),g(2,tn,2,1,"ng-container",10)(3,zn,7,8,"ng-template",null,1,se),c()}if(t&2){let e=fe(4),n=d(2);le(n.sx("root")),x(n.cn(n.cx("root"),n.styleClass)),l("ngStyle",n.style)("pBind",n.ptm("root"))("pFocusTrapDisabled",n.focusTrap===!1)("pMotion",n.visible)("pMotionAppear",!0)("pMotionName","p-dialog")("pMotionOptions",n.computedMotionOptions()),E("role",n.role)("aria-labelledby",n.ariaLabelledBy)("aria-modal",!0)("data-p",n.dataP),r(2),l("ngIf",n._headlessTemplate||n.headlessTemplate||n.headlessT)("ngIfElse",e)}}function On(t,o){if(t&1){let e=P();s(0,"div",7),F("pMotionOnAfterLeave",function(){C(e);let i=d();return w(i.onMaskAfterLeave())}),B(1,Sn,5,17,"div",8),c()}if(t&2){let e=d();le(e.sx("mask")),x(e.cn(e.cx("mask"),e.maskStyleClass)),l("ngStyle",e.maskStyle)("pBind",e.ptm("mask"))("pMotion",e.maskVisible)("pMotionAppear",!0)("pMotionEnterActiveClass",e.modal?"p-overlay-mask-enter-active":"")("pMotionLeaveActiveClass",e.modal?"p-overlay-mask-leave-active":"")("pMotionOptions",e.computedMaskMotionOptions()),E("data-p-scrollblocker-active",e.modal||e.blockScroll)("data-p",e.dataP),r(),L(e.renderDialog()?1:-1)}}var Fn={mask:({instance:t})=>({position:"fixed",height:"100%",width:"100%",left:0,top:0,display:"flex",justifyContent:t.position==="left"||t.position==="topleft"||t.position==="bottomleft"?"flex-start":t.position==="right"||t.position==="topright"||t.position==="bottomright"?"flex-end":"center",alignItems:t.position==="top"||t.position==="topleft"||t.position==="topright"?"flex-start":t.position==="bottom"||t.position==="bottomleft"||t.position==="bottomright"?"flex-end":"center",pointerEvents:t.modal?"auto":"none"}),root:{display:"flex",flexDirection:"column",pointerEvents:"auto"}},Pn={mask:({instance:t})=>{let e=["left","right","top","topleft","topright","bottom","bottomleft","bottomright"].find(n=>n===t.position);return["p-dialog-mask",{"p-overlay-mask":t.modal},e?`p-dialog-${e}`:""]},root:({instance:t})=>["p-dialog p-component",{"p-dialog-maximized":t.maximizable&&t.maximized}],header:"p-dialog-header",title:"p-dialog-title",resizeHandle:"p-resizable-handle",headerActions:"p-dialog-header-actions",pcMaximizeButton:"p-dialog-maximize-button",pcCloseButton:"p-dialog-close-button",content:()=>["p-dialog-content"],footer:"p-dialog-footer"},ii=(()=>{class t extends W{name="dialog";style=Jt;classes=Pn;inlineStyles=Fn;static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275prov=Q({token:t,factory:t.\u0275fac})}return t})();var ni=new Z("DIALOG_INSTANCE"),Bn=(()=>{class t extends j{hostName="";$pcDialog=m(ni,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=m(y,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptm("host"))}header;draggable=!0;resizable=!0;contentStyle;contentStyleClass;modal=!1;closeOnEscape=!0;dismissableMask=!1;rtl=!1;closable=!0;breakpoints;styleClass;maskStyleClass;maskStyle;showHeader=!0;blockScroll=!1;autoZIndex=!0;baseZIndex=0;minX=0;minY=0;focusOnShow=!0;maximizable=!1;keepInViewport=!0;focusTrap=!0;transitionOptions="150ms cubic-bezier(0, 0, 0.2, 1)";maskMotionOptions=Ie(void 0);computedMaskMotionOptions=Ee(()=>X(X({},this.ptm("maskMotion")),this.maskMotionOptions()));motionOptions=Ie(void 0);computedMotionOptions=Ee(()=>X(X({},this.ptm("motion")),this.motionOptions()));closeIcon;closeAriaLabel;closeTabindex="0";minimizeIcon;maximizeIcon;closeButtonProps={severity:"secondary",variant:"text",rounded:!0};maximizeButtonProps={severity:"secondary",variant:"text",rounded:!0};get visible(){return this._visible}set visible(e){this._visible=e,this._visible&&!this.maskVisible&&(this.maskVisible=!0,this.renderMask.set(!0),this.renderDialog.set(!0))}get style(){return this._style}set style(e){e&&(this._style=X({},e),this.originalStyle=e)}position;role="dialog";appendTo=Ie(void 0);onShow=new Y;onHide=new Y;visibleChange=new Y;onResizeInit=new Y;onResizeEnd=new Y;onDragEnd=new Y;onMaximize=new Y;headerViewChild;contentViewChild;footerViewChild;headerTemplate;contentTemplate;footerTemplate;closeIconTemplate;maximizeIconTemplate;minimizeIconTemplate;headlessTemplate;_headerTemplate;_contentTemplate;_footerTemplate;_closeiconTemplate;_maximizeiconTemplate;_minimizeiconTemplate;_headlessTemplate;$appendTo=Ee(()=>this.appendTo()||this.config.overlayAppendTo());renderMask=N(!1);renderDialog=N(!1);_visible=!1;maskVisible;container=N(null);wrapper;dragging;ariaLabelledBy=this.getAriaLabelledBy();documentDragListener;documentDragEndListener;resizing;documentResizeListener;documentResizeEndListener;documentEscapeListener;maskClickListener;lastPageX;lastPageY;preventVisibleChangePropagation;maximized;preMaximizeContentHeight;preMaximizeContainerWidth;preMaximizeContainerHeight;preMaximizePageX;preMaximizePageY;id=de("pn_id_");_style={};originalStyle;transformOptions="scale(0.7)";styleElement;window;_componentStyle=m(ii);headerT;contentT;footerT;closeIconT;maximizeIconT;minimizeIconT;headlessT;zIndexForLayering;get maximizeLabel(){return this.config.getTranslation(Ue.ARIA).maximizeLabel}get minimizeLabel(){return this.config.getTranslation(Ue.ARIA).minimizeLabel}zone=m(it);get maskClass(){let n=["left","right","top","topleft","topright","bottom","bottomleft","bottomright"].find(i=>i===this.position);return{"p-dialog-mask":!0,"p-overlay-mask":this.modal||this.dismissableMask,[`p-dialog-${n}`]:n}}onInit(){this.breakpoints&&this.createStyle()}templates;onAfterContentInit(){this.templates?.forEach(e=>{switch(e.getType()){case"header":this.headerT=e.template;break;case"content":this.contentT=e.template;break;case"footer":this.footerT=e.template;break;case"closeicon":this.closeIconT=e.template;break;case"maximizeicon":this.maximizeIconT=e.template;break;case"minimizeicon":this.minimizeIconT=e.template;break;case"headless":this.headlessT=e.template;break;default:this.contentT=e.template;break}})}getAriaLabelledBy(){return this.header!==null?de("pn_id_")+"_header":null}parseDurationToMilliseconds(e){let n=/([\d\.]+)(ms|s)\b/g,i=0,a;for(;(a=n.exec(e))!==null;){let p=parseFloat(a[1]),h=a[2];h==="ms"?i+=p:h==="s"&&(i+=p*1e3)}if(i!==0)return i}_focus(e){if(e){let n=this.parseDurationToMilliseconds(this.transitionOptions),i=bt.getFocusableElements(e);if(i&&i.length>0)return this.zone.runOutsideAngular(()=>{setTimeout(()=>i[0].focus(),n||5)}),!0}return!1}focus(e=this.contentViewChild?.nativeElement){let n=this._focus(e);n||(n=this._focus(this.footerViewChild?.nativeElement),n||(n=this._focus(this.headerViewChild?.nativeElement),n||this._focus(this.contentViewChild?.nativeElement)))}close(e){this.visible=!1,this.visibleChange.emit(this.visible),e.preventDefault()}enableModality(){this.closable&&this.dismissableMask&&(this.maskClickListener=this.renderer.listen(this.wrapper,"mousedown",e=>{this.wrapper&&this.wrapper.isSameNode(e.target)&&this.close(e)})),this.modal&&qe()}disableModality(){if(this.wrapper){this.dismissableMask&&this.unbindMaskClickListener();let e=document.querySelectorAll('[data-p-scrollblocker-active="true"]');this.modal&&e&&e.length==1&&We(),this.cd.destroyed||this.cd.detectChanges()}}maximize(){this.maximized=!this.maximized,!this.modal&&!this.blockScroll&&(this.maximized?qe():We()),this.onMaximize.emit({maximized:this.maximized})}unbindMaskClickListener(){this.maskClickListener&&(this.maskClickListener(),this.maskClickListener=null)}moveOnTop(){this.autoZIndex?(ge.set("modal",this.container(),this.baseZIndex+this.config.zIndex.modal),this.wrapper.style.zIndex=String(parseInt(this.container().style.zIndex,10)-1)):this.zIndexForLayering=ge.generateZIndex("modal",(this.baseZIndex??0)+this.config.zIndex.modal)}createStyle(){if(ve(this.platformId)&&!this.styleElement&&!this.$unstyled()){this.styleElement=this.renderer.createElement("style"),this.styleElement.type="text/css",Ye(this.styleElement,"nonce",this.config?.csp()?.nonce),this.renderer.appendChild(this.document.head,this.styleElement);let e="";for(let n in this.breakpoints)e+=`
                        @media screen and (max-width: ${n}) {
                            .p-dialog[${this.id}]:not(.p-dialog-maximized) {
                                width: ${this.breakpoints[n]} !important;
                            }
                        }
                    `;this.renderer.setProperty(this.styleElement,"innerHTML",e),Ye(this.styleElement,"nonce",this.config?.csp()?.nonce)}}initDrag(e){e.target.closest("div")?.getAttribute("data-pc-section")!=="headeractions"&&this.draggable&&(this.dragging=!0,this.lastPageX=e.pageX,this.lastPageY=e.pageY,this.container().style.margin="0",this.document.body.setAttribute("data-p-unselectable-text","true"),!this.$unstyled()&&Xe(this.document.body,{"user-select":"none"}))}onDrag(e){if(this.dragging&&this.container()){let n=Qe(this.container()),i=ze(this.container()),a=e.pageX-this.lastPageX,p=e.pageY-this.lastPageY,h=this.container().getBoundingClientRect(),f=getComputedStyle(this.container()),_=parseFloat(f.marginLeft),re=parseFloat(f.marginTop),$=h.left+a-_,u=h.top+p-re,T=$e();this.container().style.position="fixed",this.keepInViewport?($>=this.minX&&$+n<T.width&&(this._style.left=`${$}px`,this.lastPageX=e.pageX,this.container().style.left=`${$}px`),u>=this.minY&&u+i<T.height&&(this._style.top=`${u}px`,this.lastPageY=e.pageY,this.container().style.top=`${u}px`)):(this.lastPageX=e.pageX,this.container().style.left=`${$}px`,this.lastPageY=e.pageY,this.container().style.top=`${u}px`)}}endDrag(e){this.dragging&&(this.dragging=!1,this.document.body.removeAttribute("data-p-unselectable-text"),!this.$unstyled()&&(this.document.body.style["user-select"]=""),this.cd.detectChanges(),this.onDragEnd.emit(e))}resetPosition(){this.container().style.position="",this.container().style.left="",this.container().style.top="",this.container().style.margin=""}center(){this.resetPosition()}initResize(e){this.resizable&&(this.resizing=!0,this.lastPageX=e.pageX,this.lastPageY=e.pageY,this.document.body.setAttribute("data-p-unselectable-text","true"),!this.$unstyled()&&Xe(this.document.body,{"user-select":"none"}),this.onResizeInit.emit(e))}onResize(e){if(this.resizing){let n=e.pageX-this.lastPageX,i=e.pageY-this.lastPageY,a=Qe(this.container()),p=ze(this.container()),h=ze(this.contentViewChild?.nativeElement),f=a+n,_=p+i,re=this.container().style.minWidth,$=this.container().style.minHeight,u=this.container().getBoundingClientRect(),T=$e();(!parseInt(this.container().style.top)||!parseInt(this.container().style.left))&&(f+=n,_+=i),(!re||f>parseInt(re))&&u.left+f<T.width&&(this._style.width=f+"px",this.container().style.width=this._style.width),(!$||_>parseInt($))&&u.top+_<T.height&&(this.contentViewChild.nativeElement.style.height=h+_-p+"px",this._style.height&&(this._style.height=_+"px",this.container().style.height=this._style.height)),this.lastPageX=e.pageX,this.lastPageY=e.pageY}}resizeEnd(e){this.resizing&&(this.resizing=!1,this.document.body.removeAttribute("data-p-unselectable-text"),!this.$unstyled()&&(this.document.body.style["user-select"]=""),this.onResizeEnd.emit(e))}bindGlobalListeners(){this.draggable&&(this.bindDocumentDragListener(),this.bindDocumentDragEndListener()),this.resizable&&this.bindDocumentResizeListeners(),this.closeOnEscape&&this.closable&&this.bindDocumentEscapeListener()}unbindGlobalListeners(){this.unbindDocumentDragListener(),this.unbindDocumentDragEndListener(),this.unbindDocumentResizeListeners(),this.unbindDocumentEscapeListener()}bindDocumentDragListener(){this.documentDragListener||this.zone.runOutsideAngular(()=>{this.documentDragListener=this.renderer.listen(this.document.defaultView,"mousemove",this.onDrag.bind(this))})}unbindDocumentDragListener(){this.documentDragListener&&(this.documentDragListener(),this.documentDragListener=null)}bindDocumentDragEndListener(){this.documentDragEndListener||this.zone.runOutsideAngular(()=>{this.documentDragEndListener=this.renderer.listen(this.document.defaultView,"mouseup",this.endDrag.bind(this))})}unbindDocumentDragEndListener(){this.documentDragEndListener&&(this.documentDragEndListener(),this.documentDragEndListener=null)}bindDocumentResizeListeners(){!this.documentResizeListener&&!this.documentResizeEndListener&&this.zone.runOutsideAngular(()=>{this.documentResizeListener=this.renderer.listen(this.document.defaultView,"mousemove",this.onResize.bind(this)),this.documentResizeEndListener=this.renderer.listen(this.document.defaultView,"mouseup",this.resizeEnd.bind(this))})}unbindDocumentResizeListeners(){this.documentResizeListener&&this.documentResizeEndListener&&(this.documentResizeListener(),this.documentResizeEndListener(),this.documentResizeListener=null,this.documentResizeEndListener=null)}bindDocumentEscapeListener(){let e=this.el?this.el.nativeElement.ownerDocument:"document";this.documentEscapeListener=this.renderer.listen(e,"keydown",n=>{if(n.key=="Escape"){let i=this.container();if(!i)return;let a=ge.getCurrent();(parseInt(i.style.zIndex)==a||this.zIndexForLayering==a)&&this.close(n)}})}unbindDocumentEscapeListener(){this.documentEscapeListener&&(this.documentEscapeListener(),this.documentEscapeListener=null)}appendContainer(){this.$appendTo()!=="self"&&ft(this.document.body,this.wrapper)}restoreAppend(){this.container()&&this.$appendTo()!=="self"&&this.renderer.appendChild(this.el.nativeElement,this.wrapper)}onBeforeEnter(e){this.container.set(e.element),this.wrapper=this.container()?.parentElement,this.$attrSelector&&this.container()?.setAttribute(this.$attrSelector,""),this.appendContainer(),this.moveOnTop(),this.bindGlobalListeners(),this.container()?.setAttribute(this.id,""),this.modal&&this.enableModality()}onAfterEnter(){this.focusOnShow&&this.focus(),this.onShow.emit({})}onBeforeLeave(){this.modal&&(this.maskVisible=!1)}onAfterLeave(){this.onContainerDestroy(),this.renderDialog.set(!1),this.modal?this.renderMask.set(!1):this.maskVisible=!1,this.onHide.emit({}),this.cd.markForCheck()}onMaskAfterLeave(){this.renderDialog()||this.renderMask.set(!1)}onContainerDestroy(){this.unbindGlobalListeners(),this.dragging=!1,this.maximized&&(je(this.document.body,"p-overflow-hidden"),this.document.body.style.removeProperty("--scrollbar-width"),this.maximized=!1),this.modal&&this.disableModality(),this.blockScroll&&_t(this.document.body,"p-overflow-hidden")&&je(this.document.body,"p-overflow-hidden"),this.container()&&this.autoZIndex&&ge.clear(this.container()),this.zIndexForLayering&&ge.revertZIndex(this.zIndexForLayering),this.container.set(null),this.wrapper=null,this._style=this.originalStyle?X({},this.originalStyle):{}}destroyStyle(){this.styleElement&&(this.renderer.removeChild(this.document.head,this.styleElement),this.styleElement=null)}onDestroy(){this.container()&&(this.restoreAppend(),this.onContainerDestroy()),this.destroyStyle()}get dataP(){return this.cn({maximized:this.maximized,modal:this.modal})}static \u0275fac=(()=>{let e;return function(i){return(e||(e=M(t)))(i||t)}})();static \u0275cmp=S({type:t,selectors:[["p-dialog"]],contentQueries:function(n,i,a){if(n&1&&Ce(a,Zi,4)(a,ei,4)(a,ti,4)(a,Yi,4)(a,Ui,4)(a,qi,4)(a,Wi,4)(a,Se,4),n&2){let p;k(p=z())&&(i._headerTemplate=p.first),k(p=z())&&(i._contentTemplate=p.first),k(p=z())&&(i._footerTemplate=p.first),k(p=z())&&(i._closeiconTemplate=p.first),k(p=z())&&(i._maximizeiconTemplate=p.first),k(p=z())&&(i._minimizeiconTemplate=p.first),k(p=z())&&(i._headlessTemplate=p.first),k(p=z())&&(i.templates=p)}},viewQuery:function(n,i){if(n&1&&we(Gi,5)(ei,5)(ti,5),n&2){let a;k(a=z())&&(i.headerViewChild=a.first),k(a=z())&&(i.contentViewChild=a.first),k(a=z())&&(i.footerViewChild=a.first)}},inputs:{hostName:"hostName",header:"header",draggable:[2,"draggable","draggable",I],resizable:[2,"resizable","resizable",I],contentStyle:"contentStyle",contentStyleClass:"contentStyleClass",modal:[2,"modal","modal",I],closeOnEscape:[2,"closeOnEscape","closeOnEscape",I],dismissableMask:[2,"dismissableMask","dismissableMask",I],rtl:[2,"rtl","rtl",I],closable:[2,"closable","closable",I],breakpoints:"breakpoints",styleClass:"styleClass",maskStyleClass:"maskStyleClass",maskStyle:"maskStyle",showHeader:[2,"showHeader","showHeader",I],blockScroll:[2,"blockScroll","blockScroll",I],autoZIndex:[2,"autoZIndex","autoZIndex",I],baseZIndex:[2,"baseZIndex","baseZIndex",De],minX:[2,"minX","minX",De],minY:[2,"minY","minY",De],focusOnShow:[2,"focusOnShow","focusOnShow",I],maximizable:[2,"maximizable","maximizable",I],keepInViewport:[2,"keepInViewport","keepInViewport",I],focusTrap:[2,"focusTrap","focusTrap",I],transitionOptions:"transitionOptions",maskMotionOptions:[1,"maskMotionOptions"],motionOptions:[1,"motionOptions"],closeIcon:"closeIcon",closeAriaLabel:"closeAriaLabel",closeTabindex:"closeTabindex",minimizeIcon:"minimizeIcon",maximizeIcon:"maximizeIcon",closeButtonProps:"closeButtonProps",maximizeButtonProps:"maximizeButtonProps",visible:"visible",style:"style",position:"position",role:"role",appendTo:[1,"appendTo"],headerTemplate:[0,"content","headerTemplate"],contentTemplate:"contentTemplate",footerTemplate:"footerTemplate",closeIconTemplate:"closeIconTemplate",maximizeIconTemplate:"maximizeIconTemplate",minimizeIconTemplate:"minimizeIconTemplate",headlessTemplate:"headlessTemplate"},outputs:{onShow:"onShow",onHide:"onHide",visibleChange:"visibleChange",onResizeInit:"onResizeInit",onResizeEnd:"onResizeEnd",onDragEnd:"onDragEnd",onMaximize:"onMaximize"},features:[q([ii,{provide:ni,useExisting:t},{provide:G,useExisting:t}]),U([y]),O],ngContentSelectors:Ji,decls:1,vars:1,consts:[["container",""],["notHeadless",""],["content",""],["titlebar",""],["icon",""],["footer",""],[3,"class","style","ngStyle","pBind","pMotion","pMotionAppear","pMotionEnterActiveClass","pMotionLeaveActiveClass","pMotionOptions"],[3,"pMotionOnAfterLeave","ngStyle","pBind","pMotion","pMotionAppear","pMotionEnterActiveClass","pMotionLeaveActiveClass","pMotionOptions"],["pFocusTrap","",3,"class","style","ngStyle","pBind","pFocusTrapDisabled","pMotion","pMotionAppear","pMotionName","pMotionOptions"],["pFocusTrap","",3,"pMotionOnBeforeEnter","pMotionOnAfterEnter","pMotionOnBeforeLeave","pMotionOnAfterLeave","ngStyle","pBind","pFocusTrapDisabled","pMotion","pMotionAppear","pMotionName","pMotionOptions"],[4,"ngIf","ngIfElse"],[4,"ngTemplateOutlet"],[3,"class","pBind","z-index","mousedown",4,"ngIf"],[3,"class","pBind","mousedown",4,"ngIf"],[3,"ngStyle","pBind"],[3,"class","pBind",4,"ngIf"],[3,"mousedown","pBind"],[3,"id","class","pBind",4,"ngIf"],[3,"pBind"],[3,"pt","styleClass","ariaLabel","tabindex","buttonProps","unstyled","onClick","keydown.enter",4,"ngIf"],[3,"id","pBind"],[3,"onClick","keydown.enter","pt","styleClass","ariaLabel","tabindex","buttonProps","unstyled"],[3,"ngClass",4,"ngIf"],[4,"ngIf"],[3,"ngClass"],["data-p-icon","window-maximize",4,"ngIf"],["data-p-icon","window-minimize",4,"ngIf"],["data-p-icon","window-maximize"],["data-p-icon","window-minimize"],[3,"class",4,"ngIf"],["data-p-icon","times",4,"ngIf"],["data-p-icon","times"]],template:function(n,i){n&1&&(oe(Ki),B(0,On,2,14,"div",6)),n&2&&L(i.renderMask()?0:-1)},dependencies:[R,ae,ue,ke,ct,Be,Kt,yt,Ht,Rt,D,y,wt,Ct],encapsulation:2,changeDetection:0})}return t})(),sr=(()=>{class t{static \u0275fac=function(n){return new(n||t)};static \u0275mod=H({type:t});static \u0275inj=A({imports:[Bn,D,D]})}return t})();export{Ke as a,Bt as b,Nt as c,qt as d,Ve as e,Wt as f,Kt as g,Pa as h,Bn as i,sr as j};
