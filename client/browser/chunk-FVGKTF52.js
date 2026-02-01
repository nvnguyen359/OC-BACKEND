import{Bb as M,Db as N,Eb as $,Fb as Q,Gb as q,Hb as p,Hd as J,Ib as m,Ic as K,Kc as O,La as h,Oc as Z,P as S,Pb as f,Q as k,Rd as ee,S as A,Sd as _,U as v,Vd as te,Xb as W,Xc as d,Ya as P,Yc as w,Z as l,Za as X,_ as a,ab as Y,bb as x,cb as z,fa as F,ib as D,lb as R,ma as V,mb as I,md as G,pb as u,pe as ie,qb as g,qe as ne,rb as B,re as y,sc as j,se as C,yb as H,zb as U}from"./chunk-ESYVRVYB.js";var oe=`
    .p-scrollpanel-content-container {
        overflow: hidden;
        width: 100%;
        height: 100%;
        position: relative;
        z-index: 1;
        float: left;
    }

    .p-scrollpanel-content {
        height: calc(100% + calc(2 * dt('scrollpanel.bar.size')));
        width: calc(100% + calc(2 * dt('scrollpanel.bar.size')));
        padding-inline: 0 calc(2 * dt('scrollpanel.bar.size'));
        padding-block: 0 calc(2 * dt('scrollpanel.bar.size'));
        position: relative;
        overflow: auto;
        box-sizing: border-box;
        scrollbar-width: none;
    }

    .p-scrollpanel-content::-webkit-scrollbar {
        display: none;
    }

    .p-scrollpanel-bar {
        position: relative;
        border-radius: dt('scrollpanel.bar.border.radius');
        z-index: 2;
        cursor: pointer;
        opacity: 0;
        outline-color: transparent;
        background: dt('scrollpanel.bar.background');
        border: 0 none;
        transition:
            outline-color dt('scrollpanel.transition.duration'),
            opacity dt('scrollpanel.transition.duration');
    }

    .p-scrollpanel-bar:focus-visible {
        box-shadow: dt('scrollpanel.bar.focus.ring.shadow');
        outline: dt('scrollpanel.barfocus.ring.width') dt('scrollpanel.bar.focus.ring.style') dt('scrollpanel.bar.focus.ring.color');
        outline-offset: dt('scrollpanel.barfocus.ring.offset');
    }

    .p-scrollpanel-bar-y {
        width: dt('scrollpanel.bar.size');
        inset-block-start: 0;
    }

    .p-scrollpanel-bar-x {
        height: dt('scrollpanel.bar.size');
        inset-block-end: 0;
    }

    .p-scrollpanel-hidden {
        visibility: hidden;
    }

    .p-scrollpanel:hover .p-scrollpanel-bar,
    .p-scrollpanel:active .p-scrollpanel-bar {
        opacity: 1;
    }

    .p-scrollpanel-grabbed {
        user-select: none;
    }
`;var re=["content"],de=["xBar"],he=["yBar"],ue=["*"];function pe(r,ae){r&1&&$(0)}function me(r,ae){r&1&&H(0)}var fe=`
    ${oe}

    .p-scrollpanel {
        display: block;
    }
`,we={root:"p-scrollpanel p-component",contentContainer:"p-scrollpanel-content-container",content:"p-scrollpanel-content",barX:"p-scrollpanel-bar p-scrollpanel-bar-x",barY:"p-scrollpanel-bar p-scrollpanel-bar-y"},se=(()=>{class r extends te{name="scrollpanel";style=fe;classes=we;static \u0275fac=(()=>{let e;return function(t){return(e||(e=V(r)))(t||r)}})();static \u0275prov=S({token:r,factory:r.\u0275fac})}return r})();var le=new A("SCROLLPANEL_INSTANCE"),be=(()=>{class r extends ne{$pcScrollPanel=v(le,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=v(y,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;step=5;contentViewChild;xBarViewChild;yBarViewChild;contentTemplate;templates;_contentTemplate;scrollYRatio;scrollXRatio;timeoutFrame=e=>setTimeout(e,0);initialized=!1;lastPageY;lastPageX;isXBarClicked=!1;isYBarClicked=!1;lastScrollLeft=0;lastScrollTop=0;orientation="vertical";timer;contentId;windowResizeListener;contentScrollListener;mouseEnterListener;xBarMouseDownListener;yBarMouseDownListener;documentMouseMoveListener;documentMouseUpListener;_componentStyle=v(se);zone=v(F);onInit(){this.contentId=J("pn_id_")+"_content"}onAfterViewInit(){Z(this.platformId)&&this.zone.runOutsideAngular(()=>{this.moveBar(),this.moveBar=this.moveBar.bind(this),this.onXBarMouseDown=this.onXBarMouseDown.bind(this),this.onYBarMouseDown=this.onYBarMouseDown.bind(this),this.onDocumentMouseMove=this.onDocumentMouseMove.bind(this),this.onDocumentMouseUp=this.onDocumentMouseUp.bind(this),this.windowResizeListener=this.renderer.listen(window,"resize",this.moveBar),this.contentScrollListener=this.renderer.listen(this.contentViewChild.nativeElement,"scroll",this.moveBar),this.mouseEnterListener=this.renderer.listen(this.contentViewChild.nativeElement,"mouseenter",this.moveBar),this.xBarMouseDownListener=this.renderer.listen(this.xBarViewChild.nativeElement,"mousedown",this.onXBarMouseDown),this.yBarMouseDownListener=this.renderer.listen(this.yBarViewChild.nativeElement,"mousedown",this.onYBarMouseDown),this.calculateContainerHeight(),this.initialized=!0})}onAfterContentInit(){this.templates.forEach(e=>{switch(e.getType()){case"content":this._contentTemplate=e.template;break;default:this._contentTemplate=e.template;break}})}calculateContainerHeight(){let e=this.el.nativeElement,i=this.contentViewChild.nativeElement,t=this.xBarViewChild.nativeElement,n=this.document.defaultView,o=n.getComputedStyle(e),s=n.getComputedStyle(t),c=G(e)-parseInt(s.height,10);o["max-height"]!="none"&&c==0&&(i.offsetHeight+parseInt(s.height,10)>parseInt(o["max-height"],10)?e.style.height=o["max-height"]:e.style.height=i.offsetHeight+parseFloat(o.paddingTop)+parseFloat(o.paddingBottom)+parseFloat(o.borderTopWidth)+parseFloat(o.borderBottomWidth)+"px")}moveBar(){let e=this.el.nativeElement,i=this.contentViewChild.nativeElement,t=this.xBarViewChild.nativeElement,n=i.scrollWidth,o=i.clientWidth,s=(e.clientHeight-t.clientHeight)*-1;this.scrollXRatio=o/n;let c=this.yBarViewChild.nativeElement,T=i.scrollHeight,E=i.clientHeight,ce=(e.clientWidth-c.clientWidth)*-1;this.scrollYRatio=E/T,this.requestAnimationFrame(()=>{if(this.scrollXRatio>=1)t.setAttribute("data-p-scrollpanel-hidden","true"),!this.$unstyled()&&d(t,"p-scrollpanel-hidden");else{t.setAttribute("data-p-scrollpanel-hidden","false"),!this.$unstyled()&&w(t,"p-scrollpanel-hidden");let b=Math.max(this.scrollXRatio*100,10),L=Math.abs(i.scrollLeft*(100-b)/(n-o));t.style.cssText="width:"+b+"%; inset-inline-start:"+L+"%;bottom:"+s+"px;"}if(this.scrollYRatio>=1)c.setAttribute("data-p-scrollpanel-hidden","true"),!this.$unstyled()&&d(c,"p-scrollpanel-hidden");else{c.setAttribute("data-p-scrollpanel-hidden","false"),!this.$unstyled()&&w(c,"p-scrollpanel-hidden");let b=Math.max(this.scrollYRatio*100,10),L=i.scrollTop*(100-b)/(T-E);c.style.cssText="height:"+b+"%; top: calc("+L+"% - "+t.clientHeight+"px); inset-inline-end:"+ce+"px;"}}),this.cd.markForCheck()}onScroll(e){this.lastScrollLeft!==e.target.scrollLeft?(this.lastScrollLeft=e.target.scrollLeft,this.orientation="horizontal"):this.lastScrollTop!==e.target.scrollTop&&(this.lastScrollTop=e.target.scrollTop,this.orientation="vertical"),this.moveBar()}onKeyDown(e){if(this.orientation==="vertical")switch(e.code){case"ArrowDown":{this.setTimer("scrollTop",this.step),e.preventDefault();break}case"ArrowUp":{this.setTimer("scrollTop",this.step*-1),e.preventDefault();break}case"ArrowLeft":case"ArrowRight":{e.preventDefault();break}default:break}else if(this.orientation==="horizontal")switch(e.code){case"ArrowRight":{this.setTimer("scrollLeft",this.step),e.preventDefault();break}case"ArrowLeft":{this.setTimer("scrollLeft",this.step*-1),e.preventDefault();break}case"ArrowDown":case"ArrowUp":{e.preventDefault();break}default:break}}onKeyUp(){this.clearTimer()}repeat(e,i){this.contentViewChild?.nativeElement&&(this.contentViewChild.nativeElement[e]+=i),this.moveBar()}setTimer(e,i){this.clearTimer(),this.timer=setTimeout(()=>{this.repeat(e,i)},40)}clearTimer(){this.timer&&clearTimeout(this.timer)}bindDocumentMouseListeners(){this.documentMouseMoveListener||(this.documentMouseMoveListener=e=>{this.onDocumentMouseMove(e)},this.document.addEventListener("mousemove",this.documentMouseMoveListener)),this.documentMouseUpListener||(this.documentMouseUpListener=e=>{this.onDocumentMouseUp(e)},this.document.addEventListener("mouseup",this.documentMouseUpListener))}unbindDocumentMouseListeners(){this.documentMouseMoveListener&&(this.document.removeEventListener("mousemove",this.documentMouseMoveListener),this.documentMouseMoveListener=null),this.documentMouseUpListener&&(document.removeEventListener("mouseup",this.documentMouseUpListener),this.documentMouseUpListener=null)}onYBarMouseDown(e){this.isYBarClicked=!0,this.yBarViewChild?.nativeElement?.focus(),this.lastPageY=e.pageY,this.yBarViewChild?.nativeElement?.setAttribute("data-p-scrollpanel-grabbed","true"),!this.$unstyled()&&d(this.yBarViewChild.nativeElement,"p-scrollpanel-grabbed"),this.document.body.setAttribute("data-p-scrollpanel-grabbed","true"),!this.$unstyled()&&d(this.document.body,"p-scrollpanel-grabbed"),this.bindDocumentMouseListeners(),e.preventDefault()}onXBarMouseDown(e){this.isXBarClicked=!0,this.xBarViewChild?.nativeElement?.focus(),this.lastPageX=e.pageX,this.xBarViewChild?.nativeElement?.setAttribute("data-p-scrollpanel-grabbed","false"),!this.$unstyled()&&d(this.xBarViewChild.nativeElement,"p-scrollpanel-grabbed"),this.document.body.setAttribute("data-p-scrollpanel-grabbed","false"),!this.$unstyled()&&d(this.document.body,"p-scrollpanel-grabbed"),this.bindDocumentMouseListeners(),e.preventDefault()}onDocumentMouseMove(e){this.isXBarClicked?this.onMouseMoveForXBar(e):this.isYBarClicked?this.onMouseMoveForYBar(e):(this.onMouseMoveForXBar(e),this.onMouseMoveForYBar(e))}onMouseMoveForXBar(e){let i=e.pageX-this.lastPageX;this.lastPageX=e.pageX,this.requestAnimationFrame(()=>{this.contentViewChild.nativeElement.scrollLeft+=i/this.scrollXRatio})}onMouseMoveForYBar(e){let i=e.pageY-this.lastPageY;this.lastPageY=e.pageY,this.requestAnimationFrame(()=>{this.contentViewChild.nativeElement.scrollTop+=i/this.scrollYRatio})}scrollTop(e){let i=this.contentViewChild.nativeElement.scrollHeight-this.contentViewChild.nativeElement.clientHeight;e=e>i?i:e>0?e:0,this.contentViewChild.nativeElement.scrollTop=e}onFocus(e){this.xBarViewChild?.nativeElement?.isSameNode(e.target)?this.orientation="horizontal":this.yBarViewChild?.nativeElement?.isSameNode(e.target)&&(this.orientation="vertical")}onBlur(){this.orientation==="horizontal"&&(this.orientation="vertical")}onDocumentMouseUp(e){this.yBarViewChild?.nativeElement?.setAttribute("data-p-scrollpanel-grabbed","false"),!this.$unstyled()&&w(this.yBarViewChild.nativeElement,"p-scrollpanel-grabbed"),this.xBarViewChild?.nativeElement?.setAttribute("data-p-scrollpanel-grabbed","false"),!this.$unstyled()&&w(this.xBarViewChild.nativeElement,"p-scrollpanel-grabbed"),this.document.body.setAttribute("data-p-scrollpanel-grabbed","false"),!this.$unstyled()&&w(this.document.body,"p-scrollpanel-grabbed"),this.unbindDocumentMouseListeners(),this.isXBarClicked=!1,this.isYBarClicked=!1}requestAnimationFrame(e){(window.requestAnimationFrame||this.timeoutFrame)(e)}unbindListeners(){this.windowResizeListener&&(this.windowResizeListener(),this.windowResizeListener=null),this.contentScrollListener&&(this.contentScrollListener(),this.contentScrollListener=null),this.mouseEnterListener&&(this.mouseEnterListener(),this.mouseEnterListener=null),this.xBarMouseDownListener&&(this.xBarMouseDownListener(),this.xBarMouseDownListener=null),this.yBarMouseDownListener&&(this.yBarMouseDownListener(),this.yBarMouseDownListener=null)}onDestroy(){this.initialized&&this.unbindListeners()}refresh(){this.moveBar()}static \u0275fac=(()=>{let e;return function(t){return(e||(e=V(r)))(t||r)}})();static \u0275cmp=P({type:r,selectors:[["p-scroll-panel"],["p-scrollPanel"],["p-scrollpanel"]],contentQueries:function(i,t,n){if(i&1&&Q(n,re,4)(n,ee,4),i&2){let o;p(o=m())&&(t.contentTemplate=o.first),p(o=m())&&(t.templates=o)}},viewQuery:function(i,t){if(i&1&&q(re,5)(de,5)(he,5),i&2){let n;p(n=m())&&(t.contentViewChild=n.first),p(n=m())&&(t.xBarViewChild=n.first),p(n=m())&&(t.yBarViewChild=n.first)}},hostVars:2,hostBindings:function(i,t){i&2&&f(t.cn(t.cx("root"),t.styleClass))},inputs:{styleClass:"styleClass",step:[2,"step","step",j]},features:[W([se,{provide:le,useExisting:r},{provide:ie,useExisting:r}]),Y([y]),x],ngContentSelectors:ue,decls:9,vars:22,consts:[["content",""],["xBar",""],["yBar",""],[3,"pBind"],[3,"mouseenter","scroll","pBind"],[4,"ngTemplateOutlet"],["tabindex","0","role","scrollbar",3,"mousedown","keydown","keyup","focus","blur","pBind"],["tabindex","0","role","scrollbar",3,"mousedown","keydown","keyup","focus","pBind"]],template:function(i,t){if(i&1){let n=U();N(),g(0,"div",3)(1,"div",4,0),M("mouseenter",function(){return l(n),a(t.moveBar())})("scroll",function(s){return l(n),a(t.onScroll(s))}),R(3,pe,1,0),z(4,me,1,0,"ng-container",5),B()(),g(5,"div",6,1),M("mousedown",function(s){return l(n),a(t.onXBarMouseDown(s))})("keydown",function(s){return l(n),a(t.onKeyDown(s))})("keyup",function(){return l(n),a(t.onKeyUp())})("focus",function(s){return l(n),a(t.onFocus(s))})("blur",function(){return l(n),a(t.onBlur())}),B(),g(7,"div",7,2),M("mousedown",function(s){return l(n),a(t.onYBarMouseDown(s))})("keydown",function(s){return l(n),a(t.onKeyDown(s))})("keyup",function(){return l(n),a(t.onKeyUp())})("focus",function(s){return l(n),a(t.onFocus(s))}),B()}i&2&&(f(t.cx("contentContainer")),u("pBind",t.ptm("contentContainer")),h(),f(t.cx("content")),u("pBind",t.ptm("content")),h(2),I(!t.contentTemplate&&!t._contentTemplate?3:-1),h(),u("ngTemplateOutlet",t.contentTemplate||t._contentTemplate),h(),f(t.cx("barX")),u("pBind",t.ptm("barX")),D("aria-orientation","horizontal")("aria-valuenow",t.lastScrollLeft)("aria-controls",t.contentId)("data-pc-group-section","bar"),h(2),f(t.cx("barY")),u("pBind",t.ptm("barY")),D("aria-orientation","vertical")("aria-valuenow",t.lastScrollTop)("aria-controls",t.contentId)("data-pc-group-section","bar"))},dependencies:[O,K,_,C,y],encapsulation:2,changeDetection:0})}return r})(),Re=(()=>{class r{static \u0275fac=function(i){return new(i||r)};static \u0275mod=X({type:r});static \u0275inj=k({imports:[be,_,C,_,C]})}return r})();export{be as a,Re as b};
